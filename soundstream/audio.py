import sounddevice as sd
import threading
import numpy as np
from soundstream.utils import better_dumps as dumps


FRAME_DELAY = 1 / 1000  # frame delay in millis


class AudioWire():
    def __init__(self, socketio, device=None):
        """Wire audio from sound card to output stream.

        :param socketio: SocketIO app object.
        :param int | str: Audio input device (numeric ID or substring). If
            none, default device is used.
        """
        self.socketio = socketio
        self.thread = None
        self.is_active = False
        self.device = device
        self.n_fft_bins = 100
        self.gain = 20  # initial gain factor
        self.block_duration = 50  # block size (ms)
        self.range_low = 100  # range low end (Hz)
        self.range_high = 2000  # range high end (Hz)
        self.max_amplitude = 255  # arbitrary maximum amplitude

        self.check_inputs()
        self.compute_fft_params()

    def check_inputs(self):
        if self.range_high <= self.range_low:
            raise Exception('High must be greater than low in range.')

    def compute_fft_params(self):
        self.sample_rate = sd.query_devices(self.device, 'input')['default_samplerate']  # noqa: E501
        self.delta_freq = (self.range_high - self.range_low) / (self.n_fft_bins - 1)  # noqa: E501
        self.fft_size = int(np.ceil(self.sample_rate / self.delta_freq))
        self.low_bin = int(np.floor(self.range_low / self.delta_freq))
        self.block_size = int(self.sample_rate * self.block_duration / 1000)

    def map_amplitude(self, val):
        """Map amplitude.

        Map amplitude value within arbitrary range: [0, self.max_amplitude].

        :param float val: Amplitude value from FFT.
        """
        return int(np.clip(val, 0, 1) * self.max_amplitude)

    def callback(self, indata, frames, time, status):
        rv_fft = None
        rv_bass_hit = None
        if status:
            print(f'[AUDIO WIRE] {status}')
        if any(indata):
            magnitude = np.abs(np.fft.rfft(indata[:, 0], n=self.fft_size))
            magnitude *= self.gain / self.fft_size
            magnitude_in_range = magnitude[self.low_bin:self.low_bin+self.n_fft_bins]  # noqa: E501
            rv_fft = [self.map_amplitude(x) for x in magnitude_in_range]
            rv_bass_hit = self.check_bass_hit(rv_fft)
        data_frame = self.pack_data_frame(rv_fft, rv_bass_hit)
        self.socketio.emit('data frame', data_frame)

    def check_bass_hit(self, fft):
        """ Check if music has a "bass hit". """
        n = 5
        threshold = 0.65 * self.max_amplitude
        if fft is None:
            return False
        bin_mean = sum(fft[:n]) / n  # sum of lowest n bins
        return bin_mean > threshold

    def start(self):
        """ Start audio wire streaming. """
        self.thread = threading.Thread(target=self.thread_function)
        self.is_active = True
        self.thread.start()

    def stop(self):
        """ Stop audio wire streaming. """
        self.is_active = False

    def wait(self):
        self.thread.join()

    def list_of_zeros(self, length):
        return np.zeros(length, dtype=np.int).tolist()

    def pack_data_frame(self, fft, bass_hit):
        is_data = fft is not None
        return dumps({
            'success': True,
            'is_data': is_data,
            'fft': fft if is_data else self.list_of_zeros(self.n_fft_bins),
            'bass_hit': bass_hit,
        })

    def thread_function(self):
        with sd.InputStream(device=self.device,
                            channels=1,
                            callback=self.callback,
                            blocksize=self.block_size,
                            samplerate=self.sample_rate):
            while self.is_active:
                self.socketio.sleep(FRAME_DELAY)

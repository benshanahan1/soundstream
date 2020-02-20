import pyaudio
import threading
import numpy as np
from misc import better_dumps as dumps


FRAME_DELAY = 10 / 1000  # frame delay in millis


class AudioWire():
    CHUNK = 32
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    def __init__(self, socketio):
        """Wire audio from sound card to output stream.

        :param socketio: SocketIO app object.
        """
        self.socketio = socketio
        self.thread = None
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)
        self.is_active = False

    def start(self, delay=0):
        """Start audio wire streaming.

        :param float delay: Start thread after ``delay`` seconds.
        """
        self.is_active = True
        self.thread = threading.Thread(target=self.thread_function)
        self.socketio.sleep(delay)
        self.thread.start()

    def stop(self):
        """ Stop audio wire streaming. """
        self.is_active = False
        self.close()

    def wait(self):
        self.thread.join()

    def thread_function(self):
        print('in thread function')
        while self.is_active:
            chunked = self.stream.read(self.CHUNK)
            chunked = np.array(list(chunked))
            deinterleaved = [chunked[idx::self.CHANNELS] for idx in range(self.CHANNELS)]  # noqa: E501
            ch1 = deinterleaved[0]
            ch2 = deinterleaved[1]
            frame = {
                'mean': [
                    np.round(np.mean(ch1)),
                    np.round(np.mean(ch2)),
                ],
                'sum': [
                    np.sum(ch1),
                    np.sum(ch2),
                ],
            }
            self.socketio.emit('data frame', dumps(frame))
            self.socketio.sleep(FRAME_DELAY)

    def close(self):
        """ Close stream and clean up. """
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print('terminate')

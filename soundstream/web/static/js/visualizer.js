const arrayOfNumber = (numToFill, nElements) => Array(nElements).fill(numToFill);

const nBins = 100;

// Soundstream object.
let soundstream = {
  socket: io.connect(),
  nBins,  // number of FFT bins
  maxAmpl: 255,  // maximum scaled FFT amplitude
  isData: false,
  bassHit: false,
  fft: arrayOfNumber(0, nBins),
};

// SocketIO handlers.
soundstream.socket.on('data frame', function(rawFrame) {
  const parsedData = JSON.parse(rawFrame);
  soundstream.bassHit = parsedData.bass_hit;
  soundstream.isData = parsedData.is_data;
  soundstream.fft = soundstream.isData ? parsedData.fft : arrayOfNumber(0, soundstream.nBins);
});

// Reload window on resize event.
window.addEventListener('resize', () => window.location.reload());

document.title = 'Soundstream | Spectro';

// drawing constants
const canvasWidth = window.innerWidth * 0.9;
const canvasHeight = window.innerHeight * 0.9;
const midHeight = canvasHeight / 2;
const weight = canvasWidth / 100;
const spacing = 2;
const backgroundColor = 'black';
const strokeColor = 'white';

let fftSmooth = arrayOfNumber(0, nBins);
let envelopeLower = arrayOfNumber(midHeight, nBins);
let envelopeUpper = arrayOfNumber(midHeight, nBins);

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  background(backgroundColor);
  stroke(strokeColor);
}

function draw() {
  background(backgroundColor);  // reset background
  strokeWeight(weight);

  for (let i = 0; i < soundstream.fft.length; i++) {
    fftSmooth[i] = (fftSmooth[i] + soundstream.fft[i]) / 2;  // moving avg for fft to smooth it a bit

    const x = (weight + spacing) * i;
    const y0 = midHeight - fftSmooth[i];
    const y1 = midHeight + fftSmooth[i];

    // Update envelopes.
    if (y0 < envelopeLower[i]) {
        envelopeLower[i] = y0;
    } else if (envelopeLower[i] < midHeight) {
        envelopeLower[i] += 2;
    }
    if (y1 > envelopeUpper[i]) {
        envelopeUpper[i] = y1;
    } else if (envelopeUpper[i] > midHeight) {
        envelopeUpper[i] -= 2;
    }

    stroke('#310642');
    line(x, envelopeLower[i], x, envelopeUpper[i]);
    stroke(255, 255 - fftSmooth[i], 255 - fftSmooth[i]);
    line(x, y0, x, y1);
  }
}

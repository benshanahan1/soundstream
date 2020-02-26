document.title = 'Soundstream | Spectro';

// drawing constants
const canvasWidth = window.innerWidth;
const canvasHeight = window.innerHeight;
const midHeight = canvasHeight / 2;
const weight = canvasWidth / 100;
const height = 5;
const spacing = 5;
const backgroundColor = 'white';

let fftSmooth = arrayOfNumber(0, nBins);
let envelopeLower = arrayOfNumber(midHeight, nBins);
let envelopeUpper = arrayOfNumber(midHeight, nBins);

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  background(backgroundColor);
  noStroke();
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

    fill('orangered');
    rect(x, envelopeLower[i] - height, weight, height);
    rect(x, envelopeUpper[i], weight, height);
    fill('darkslategray');
    rect(x, y0, weight, y1 - y0);
  }
}

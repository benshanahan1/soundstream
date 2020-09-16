document.title = "Soundstream | Strudel";

const canvasWidth = window.innerWidth * 0.9;
const canvasHeight = window.innerHeight * 0.9;

const nHistory = 100;
const nBinsShown = 40;
let fftSmooth = arrayOfNumber(0, nBinsShown);
let fftHistory = arrayOfNumber(fftSmooth.slice(0), nHistory);
const gain = 1.15;

// drawing constants
const spacing = 4;
const boxWidth = canvasWidth / nHistory;
const boxHeight = canvasHeight / nBinsShown;
const defaultBackgroundColor = "black";

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  background(defaultBackgroundColor);
  noStroke();
  frameRate(24);
}

function draw() {
  for (let i = 0; i < nBinsShown; i++) {
    fftSmooth[i] = (fftSmooth[i] + soundstream.fft[i]) / 2; // moving avg for fft to smooth it a bit
  }

  // fftHistory will act as a FIFO queue. Remove first element using slice().
  fftHistory = fftHistory.slice(1); // throw away first element
  fftHistory.push(fftSmooth.slice(0));

  for (let i = 0; i < nHistory; i++) {
    const row = fftHistory[i];
    for (let j = 0; j < nBinsShown; j++) {
      noStroke();
      fill(row[j] * gain, row[j] * gain, row[j] * gain);
      rect(
        i * boxWidth,
        j * boxHeight,
        boxWidth - spacing,
        boxHeight - spacing
      );
    }
  }
}

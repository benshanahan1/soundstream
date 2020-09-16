document.title = "Soundstream | Strudel";

const canvasWidth = window.innerWidth * 0.9;
const canvasHeight = window.innerHeight * 0.9;

const nHistory = 100;
const nBinsShown = 100;
let fftSmooth = arrayOfNumber(0, nBinsShown);
let fftHistory = arrayOfNumber(fftSmooth.slice(0), nHistory);
const gain = 1.15;

// drawing constants
const spacing = 0;
const boxWidth = canvasWidth / nHistory;
const boxHeight = canvasHeight / nBinsShown;
const defaultBackgroundColor = "black";

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  background(defaultBackgroundColor);
  noStroke();
  frameRate(30);
  colorMode(HSB);
}

function draw() {
  for (let i = 0; i < nBinsShown; i++) {
    fftSmooth[i] = (fftSmooth[i] + soundstream.fft[i]) / 2; // moving avg for fft to smooth it a bit
  }

  // fftHistory will act as a FIFO queue. Remove first element using slice().
  fftHistory.pop(); // throw away last element
  fftHistory.unshift(fftSmooth.slice(0));  // add current value to beginning

  for (let i = 0; i < nHistory; i++) {
    const row = fftHistory[i];
    for (let j = 0; j < nBinsShown; j++) {
      noStroke();
      fill(
        map(gain * row[j], 0, 200, 255, 0),
        // map(row[j], 0, 200, 255, 0),
        255,
        map(gain * row[j], 0, 200, 0, 255),
      );
      rect(
        i * boxWidth,
        canvasHeight - (j * boxHeight),
        boxWidth - spacing,
        boxHeight - spacing
      );
    }
  }
}

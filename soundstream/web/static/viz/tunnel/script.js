// set display mode from template
const DISPLAY_MODE = 'circles';
document.title = `Soundstream | ${DISPLAY_MODE}`;

// drawing constants
const canvasWidth = window.innerWidth;
const canvasHeight = window.innerHeight;
const midHeight = canvasHeight / 2;
const barWidth = canvasWidth / 100;
const backgroundColor = 'black';
const strokeColor = 'white';

let fftSmooth = arrayOfNumber(0, nBins);

function setup() {
  createCanvas(canvasWidth, canvasHeight);
  background(backgroundColor);
  stroke(strokeColor);
}

function draw() {
  noStroke();
  background(backgroundColor);  // reset background

  for (let i = soundstream.fft.length; i > 0; i--) {
    fftSmooth[i] = (fftSmooth[i] + soundstream.fft[i]) / 2;  // moving avg for fft to smooth it a bit

    const currentWidth = barWidth * i;
    const x = canvasWidth / 2 - currentWidth / 2;
    const y = canvasHeight / 2 - currentWidth / 2;

    fill(fftSmooth[i], fftSmooth[i], fftSmooth[i]);
    switch(DISPLAY_MODE) {
      case 'circles':
        circle(canvasWidth / 2, canvasHeight / 2, currentWidth);
        break;
      case 'bars':
        rect(currentWidth, 0, barWidth, canvasHeight);
        break;
      default:
        rect(x, y, currentWidth, currentWidth);
        break;
    }
  }
}

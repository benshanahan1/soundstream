# soundstream
Websocket server proof-of-concept for providing near real-time audio visualization in a browser (or other client). A demo is available at http://localhost:3000/ (once the server is configured and running).

## Install
### General Usage
Install the soundstream server directly from GitHub:
```bash
pip install git+https://github.com/benshanahan1/soundstream
```

### Development
For development, you might wanna create a virtualenv before installing requirements:
```bash
virtualenv -p python3 venv
source venv/bin/activate
```

Then, install the soundstream server from source:
```bash
pip install -e .[dev]
```

## Run
Run the server like so:
```bash
soundstream
```

**NOTE:** most operating systems you need to select a audio monitor device / loopback / stereo mix to actually record system audio (what you hear coming from the speakers). On Linux, you can do this with pulseaudio control panel (pavucontrol). Open pavucontrol, under input devices, select "Show all input devices". You should see a "Monitor of Built-in Audio..." device show up. Now go to the Recording tab. If you see nothing there, you need to run the soundstream server first. Once running, you will see an "ALSA plug-in [python3]" device. On the dropdown menu, select "Monitor of Built-in Audio..." that you saw in the Input Devices tab.

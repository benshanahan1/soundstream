# soundstream

## install
You might wanna create a virtualenv before installing requirements.
```bash
pip install -r requirements.txt
```

## run
```bash
python app.py
```

Note that on most operating systems you need to select a audio monitor device / loopback / stereo mix to actually record system audio (what you hear coming from the speakers). On Linux, you can do this with pulseaudio control panel (pavucontrol). Open pavucontrol, under input devices, select "Show all input devices". You should see a "Monitor of Built-in Audio..." device show up. Now go to the Recording tab. If you see nothing there, you need to run the soundstream server first. Once running, you will see an "ALSA plug-in [python3]" device. On the dropdown menu, select "Monitor of Built-in Audio..." that you saw in the Input Devices tab.

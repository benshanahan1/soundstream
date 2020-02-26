function onlyAudioDevices(devices) {
  return devices.filter((d) => d.kind === 'audioinput');
}

function attach(devices) {
  devices.forEach(function(device) {
    console.log(device.deviceId);
  });
  return navigator.mediaDevices.getUserMedia({
    audio: { deviceId: devices[0].deviceId }
  });
}

const handleSuccess = function(stream) {
  const context = new AudioContext();
  const source = context.createMediaStreamSource(stream);
  const processor = context.createScriptProcessor(1024, 1, 1);
  source.connect(processor);
  processor.connect(context.destination);
  processor.onaudioprocess = doSomethingWithAudioBuffer;
 };

const handleFailure = function(reason) {
  console.log(reason);
}

function doSomethingWithAudioBuffer(e) {
  const bufferArray = e.inputBuffer.getChannelData(0);
  document.body.innerHTML = Math.max(...bufferArray);
}

navigator.mediaDevices.enumerateDevices()
  .then(onlyAudioDevices)
  .then(attach)
  .then(handleSuccess, handleFailure);

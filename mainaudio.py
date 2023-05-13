<!DOCTYPE html>
<html>
  <head>
    <title>Noise Level Detection</title>
    <style>
      body {
        font-family: sans-serif;
        text-align: center;
      }
      h1 {
        margin-top: 2em;
        margin-bottom: 2em;
      }
      button {
        margin-top: 1em;
        margin-bottom: 1em;
        padding: 0.5em;
        font-size: 1em;
        font-weight: bold;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
      }
      button:hover {
        background-color: #0069d9;
      }
      #noise-level {
        margin-top: 1em;
        margin-bottom: 2em;
        padding: 0.5em;
        font-size: 2em;
        font-weight: bold;
        text-align: center;
      }
    </style>
  </head>
  <body>
    <h1>Noise Level Detection</h1>
    <button id="start-btn">Start</button>
    <button id="stop-btn">Stop</button>
    <p>Current noise level:</p>
    <textarea id="noise-level" rows="1" cols="20"></textarea>
    <script>
      const startBtn = document.getElementById('start-btn');
      const stopBtn = document.getElementById('stop-btn');
      const noiseLevelEl = document.getElementById('noise-level');
      let intervalId;
      let isStreaming = false;
      const CHUNK_SIZE = 2048;
      const SAMPLING_RATE = 44100;
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      let analyser = null;

      function startStreaming() {
        const stream = navigator.mediaDevices.getUserMedia({audio: true}).then(function(stream) {
          isStreaming = true;
          const input = audioContext.createMediaStreamSource(stream);
          analyser = audioContext.createAnalyser();
          analyser.fftSize = 2048;
          input.connect(analyser);
          const bufferLength = analyser.frequencyBinCount;
          const dataArray = new Uint8Array(bufferLength);

          intervalId = setInterval(() => {
            analyser.getByteFrequencyData(dataArray);
            const rms = calculateRMS(dataArray);
            const decibelLevel = 20 * Math.log10(rms);
            noiseLevelEl.value = decibelLevel.toFixed(2) + ' dB';
          }, 1000);
        });
      }

      function stopStreaming() {
        if (intervalId) {
          clearInterval(intervalId);
          intervalId = null;
        }
        if (analyser) {
          analyser.disconnect();
          analyser = null;
        }
        isStreaming = false;
        noiseLevelEl.value = '';
      }

      function calculateRMS(dataArray) {
        let rms = 0;
        for (let i = 0; i < dataArray.length; i++) {
          rms += dataArray[i] * dataArray[i];
        }
        rms /= dataArray.length;
        rms = Math.sqrt(rms);
        return rms;
      }

      startBtn.addEventListener('click', () => {
        if (!isStreaming) {
          startStreaming();
        }
      });

      stopBtn.addEventListener('click', () => {
        stopStreaming();
      });
    </script>
  </body>

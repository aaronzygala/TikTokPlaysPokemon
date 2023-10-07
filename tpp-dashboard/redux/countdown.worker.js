let countdown = 0;
let timerId;

self.onmessage = function (event) {
  if (event.data === 'start') {
    startCountdown();
  } else if (event.data === 'stop') {
    stopCountdown();
  } else if (event.data.type === 'initialize') {
    postMessage({ type: 'workerInitialized', worker: self });
  }
};

function startCountdown() {
  timerId = setInterval(() => {
    postMessage({ type: 'tick', countdown });
    countdown = countdown > 0 ? countdown - 1 : 0;
  }, 1000);
}

function stopCountdown() {
  clearInterval(timerId);
}

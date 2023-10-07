// src/redux/actions.js

export const initializeCountdown = (initialCountdown) => ({
    type: 'INITIALIZE_COUNTDOWN',
    payload: initialCountdown,
  });

export const tick = () => ({
    type: 'TICK',
});

export const startCountdown = () => async (dispatch) => {
    console.log("TEST")
    if (typeof Worker !== 'undefined') {
        const worker = new Worker('./countdown-worker.js');

        // Initialize the worker
        worker.postMessage({ type: 'initialize' });
        
        // Start the countdown
        worker.postMessage('start');
  
      worker.onmessage = function (event) {
        // Dispatch the countdown tick action
        dispatch(tick);
      };
  
      dispatch({
        type: 'START_COUNTDOWN',
        payload: worker,
      });
    } else {
      // Fallback for environments that do not support Web Workers
    //   dispatch(fetchInitialCountdown());
    }
  };
  
  export const stopCountdown = (worker) => {
    if (worker) {
      worker.postMessage('stop');
    }
  
    return {
      type: 'STOP_COUNTDOWN',
    };
  };
  
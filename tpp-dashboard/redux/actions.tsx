// redux/actions.js
export const initializeCountdown = (initialCountdown) => ({
    type: 'INITIALIZE_COUNTDOWN',
    payload: initialCountdown,
  });
  
  export const tick = () => ({
    type: 'TICK',
  });
  
  export const startCountdown = () => async (dispatch) => {
    // Perform any asynchronous operations if needed
  
    // Start the countdown
    const intervalId = setInterval(() => {
      dispatch(tick());
    }, 1000);
  
    // Dispatch the intervalId to store it in the Redux state
    dispatch({
      type: 'START_COUNTDOWN',
      payload: intervalId,
    });
  };
  
  export const stopCountdown = (intervalId) => {
    clearInterval(intervalId);
  
    return {
      type: 'STOP_COUNTDOWN',
    };
  };
  
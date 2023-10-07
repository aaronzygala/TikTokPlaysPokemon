// src/redux/reducer.js
const initialState = {
    countdown: 0, // or set it to the initial countdown value
    timerInitialized: false,
  };
  
// src/redux/reducer.js
const reducer = (state = initialState, action) => {
    switch (action.type) {
      case 'SET_COUNTDOWN':
        return { ...state, countdown: action.payload };
      case 'TICK':
        return {
          ...state,
          countdown: state.countdown > 0 ? state.countdown - 1 : 0,
        };
      case 'INITIALIZE_COUNTDOWN':
        return {
          ...state,
          countdown: action.payload,
        };
      case 'START_COUNTDOWN':
        return {
          ...state,
          countdownWorker: action.payload,
        };
      case 'STOP_COUNTDOWN':
        return {
          ...state,
          countdownWorker: null,
        };
      default:
        return state;
    }
  };
  
  
  export default reducer;
  
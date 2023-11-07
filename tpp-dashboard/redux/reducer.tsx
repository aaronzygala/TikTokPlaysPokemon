// redux/reducer.js
const initialState = {
    countdown: null,
    intervalId: null,
  };
  
  const reducer = (state = initialState, action) => {
    switch (action.type) {
      case 'INITIALIZE_COUNTDOWN':
        return {
          ...state,
          countdown: action.payload,
        };
  
      case 'TICK':
        return {
          ...state,
          countdown: state.countdown > 0 ? state.countdown - 1 : 0,
        };
  
      case 'START_COUNTDOWN':
        return {
          ...state,
          intervalId: action.payload,
        };
  
      case 'STOP_COUNTDOWN':
        return {
          ...state,
          intervalId: null,
        };
  
      default:
        return state;
    }
  };
  
  export default reducer;
  
// ToggleScriptTimer.js
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import axios from 'axios';
import { initializeCountdown, tick } from '../redux/actions';

const ToggleScriptTimer = () => {
  const dispatch = useDispatch();
  const countdown = useSelector((state) => state.countdown);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${String(minutes).padStart(2, '0')} : ${String(remainingSeconds).padStart(2, '0')}`;
  };

  const toggleScript = async () => {
    try {
      const response = await axios.post(`/api/restart`);
      // Handle response if needed
    } catch (error) {
      console.error("Error toggling script:", error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/constants');
        const initialCountdown = response.data.constants.TOGGLE_SCRIPT_TIMER.value * 60;
        if (countdown === null){
            dispatch(initializeCountdown(initialCountdown));
        }
      } catch (error) {
        console.error('Error fetching initial countdown:', error);
      }
    };

    // Only fetch the initial countdown when the component mounts
    fetchData();
  }, [dispatch]); // This dependency array ensures that the effect runs only on mount

  useEffect(() => {
    if (countdown !== null) {
      const intervalId = setInterval(() => {
        dispatch(tick());
      }, 1000);

      if (countdown === 0) {
        toggleScript();
        dispatch(initializeCountdown(null)); // Set to null to avoid triggering the countdown logic until the new initial countdown is fetched
        clearInterval(intervalId);
      }

      return () => clearInterval(intervalId);
    }
  }, [countdown, dispatch]);

  return (
    <div>
      {countdown !== null ? (
        <div className="">
            <div className="text-lg font-bold">{formatTime(countdown)}</div>
        </div>
      ) : (
        <p>Loading countdown...</p>
      )}
    </div>
  );
};

export default ToggleScriptTimer;

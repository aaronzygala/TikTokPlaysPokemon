// ToggleScriptTimer.js
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import axios from 'axios';
import { initializeCountdown } from '../redux/actions';

const worker = new Worker('../redux/countdown.worker.js');

const ToggleScriptTimer = () => {
  const dispatch = useDispatch();
  const countdown = useSelector((state) => state.countdown);

  useEffect(() => {
    // Initialize the worker
    worker.postMessage({ type: 'initialize' });

    // Fetch initial countdown from the API
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/constants');
        const initialCountdown = response.data.constants.TOGGLE_SCRIPT_TIMER.value * 60;
        dispatch(initializeCountdown(initialCountdown));
      } catch (error) {
        console.error('Error fetching initial countdown:', error);
      }
    };

    fetchData();
  }, [dispatch]);

  useEffect(() => {
    // Start the countdown
    worker.postMessage({ type: 'start' });

    // Return a cleanup function
    return () => {
      // Stop the countdown
      worker.postMessage({ type: 'stop' });
    };
  }, []);

  useEffect(() => {
    // Handle messages from the worker
    const handleMessage = (event) => {
      const { type, countdown } = event.data;
      if (type === 'tick') {
        // Dispatch the tick action
        dispatch({ type: 'TICK', payload: countdown });
      }
    };

    worker.addEventListener('message', handleMessage);

    // Cleanup the event listener
    return () => {
      worker.removeEventListener('message', handleMessage);
    };
  }, [dispatch]);

  return (
    <div>
      {countdown !== null ? (
        <p>Countdown: {formatTime(countdown)}</p>
      ) : (
        <p>Loading countdown...</p>
      )}
    </div>
  );
};

export default ToggleScriptTimer;

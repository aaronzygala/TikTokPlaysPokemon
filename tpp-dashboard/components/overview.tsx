import React, { useState, useEffect, useRef } from "react";
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

const COMMAND_TO_COLOR = {
  "A": "#3338739a",
  "B": "#335c77b3",
  "Up": "#339075bf",
  "Down": "#33c66eb8",
  "Left": "#33f3679f",
  "Right": "#33ff6d78",
  "Start": "#33ff8449",
  "Select": "#33ffa600",
};

const COMMAND_TO_BORDER = {
  "A": "#38739a",
  "B": "#5c77b3",
  "Up": "#9075bf",
  "Down": "#c66eb8",
  "Left": "#f3679f",
  "Right": "#ff6d78",
  "Start": "#ff8449",
  "Select": "#ffa600",
};

ChartJS.register(ArcElement, Tooltip, Legend);

export function CommandVotesDisplay() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      {
        label: 'Votes',
        data: [],
        backgroundColor: [],
        borderColor: [],
        borderWidth: 1,
      },
    ],
  });
  const [timerRemaining, setTimerRemaining] = useState(10);
  const timerRemainingRef = useRef(timerRemaining);

  const textCenter = {
    id: 'textCenter',
    beforeDraw: function(chart) {
        var width = chart.width,
            height = chart.height,
            ctx = chart.ctx;
        ctx.restore();
        var fontSize = (height / 16); // Font size in pixels
        ctx.font = fontSize + "px sans-serif"; // Use "px" for font size
        ctx.fillStyle = 'white';
    
        ctx.textBaseline = "top";
        var text1 = "Vote Timer:",
            text2 = `${timerRemainingRef.current}s`,
            textX1 = Math.round((width - ctx.measureText(text1).width) / 2),
            textX2 = Math.round((width - ctx.measureText(text2).width) / 2),

            textY1 = height / 2.5,
            textY2 = textY1 + fontSize * 1.5; // Adjust the vertical distance between the lines here
    
        ctx.fillText(text1, textX1, textY1);
        ctx.fillText(text2, textX2, textY2);
    
        ctx.save();
    }
  };
  
  const options = {
    plugins: {
      legend: {
        display: false,
        position: 'right',
      },
    },
    maintainAspectRatio: true,
    responsive: true,
  };

  useEffect(() => {
    timerRemainingRef.current = timerRemaining;
  }, [timerRemaining]);

  useEffect(() => {
    const fetchChartData = () => {
      // Fetch data from the API using fetch()
      fetch('/api/current_vote')
        .then(response => response.json())
        .then(responseData => {
          const { labels, data, timer_remaining } = responseData;
          setTimerRemaining(timer_remaining);
          setChartData({
            labels: labels,
            datasets: [
              {
                label: 'Votes',
                data: data,
                backgroundColor: labels.map((label) => COMMAND_TO_COLOR[label]),
                borderColor: labels.map((label) => COMMAND_TO_COLOR[label]),
                borderWidth: 1,
              },
            ],
          });
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    };

    // Fetch data initially
    fetchChartData();

    // Set up an interval to fetch data periodically (adjust the interval time as needed)
    const dataFetchInterval = setInterval(() => {
      fetchChartData();
    }, 1000); // Fetch data every 5 seconds, for example

    return () => {
      clearInterval(dataFetchInterval);
    };
  }, []);

  return <Doughnut data={chartData} plugins={[textCenter]} options={options} />;
}

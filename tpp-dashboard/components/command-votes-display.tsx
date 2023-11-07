import React, { useState, useEffect, useRef } from "react";
import { Doughnut } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

const COMMAND_TO_COLOR = {
  "Aa": "rgba(56, 115, 154, 0.2)",
  "Bb": "rgba(92, 119, 179, 0.2)",
  "Up": "rgba(198, 110, 184, 0.2)",
  "Down": "rgba(144, 117, 191, 0.2)",
  "Left": "rgba(243, 103, 159, 0.2)",
  "Right": "rgba(255, 109, 120, 0.2)",
  "Start": "rgba(255, 132, 73, 0.2)",
  "Select": "rgba(255, 166, 0, 0.2)",
  "Ll": "rgba(157, 242, 131, 0.2)",
  "Rr": "rgba(250, 146, 131, 0.2)",
  "Save": "rgba(197, 101, 168, 0.2)",
  "Load": "rgba(253, 42, 168, 0.2)",
};

const COMMAND_TO_BORDER = {
  "A": "rgba(56, 115, 154, 1.0)",
  "B": "rgba(92, 119, 179, 1.0)",
  "Up": "rgba(198, 110, 184, 1.0)",
  "Down": "rgba(144, 117, 191, 1.0)",
  "Left": "rgba(243, 103, 159, 1.0)",
  "Right": "rgba(255, 109, 120, 1.0)",
  "Start": "rgba(255, 132, 73, 1.0)",
  "Select": "rgba(255, 166, 0, 1.0)",
  "Ll": "rgba(157, 242, 131, 1.0)",
  "Rr": "rgba(250, 146, 131, 1.0)",
  "Save": "rgba(197, 101, 168, 1.0)",
  "Load": "rgba(253, 42, 168, 1.0)",
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
    maintainAspectRatio: false,
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
                borderColor: labels.map((label) => COMMAND_TO_BORDER[label]),
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

  return (
    <div className="h-[250px] lg:h-[650px]">
        <Doughnut data={chartData} plugins={[textCenter]} options={options} />
    </div>
  
  );
}

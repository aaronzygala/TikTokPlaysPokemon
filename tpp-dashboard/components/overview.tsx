"use client"

import React from "react"
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'react-chartjs-2';

const COMMAND_TO_COLOR = {
  "a" : "#EFA434",
  "b" : "#B4BA3B",
  "up" : "#77C669",
  "down" : "#40C9A0",
  "left" : "#49C4CB",
  "right" : "#8BB9DD",
  "start" : "#C6A9D2",
  "select" : "#EA9EB5",
}
ChartJS.register(ArcElement, Tooltip, Legend);

const data = {
  labels: ['A', 'B', 'Start', 'Select', 'Up', 'Down', 'Left', 'Right'],
  datasets: [
    {
      label: 'Votes',
      data: [12, 19, 3, 5, 2, 3, 1, 1],
      backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)',
        'rgba(159, 244, 64, 0.2)',
        'rgba(63, 159, 232, 0.2)',

      ],
      borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)',
        'rgba(159, 244, 64, 1)',
        'rgba(63, 159, 232, 1)',

      ],
      borderWidth: 1,
    },
  ],
};

const textCenter = {
  id: 'textCenter',
  beforeDatasetsDraw(chart, args, pluginOptions) {
    const {ctx, data} = chart;
    ctx.save();
    ctx.font = 'bolder 30px sans-serif';
    ctx.fillStyle = 'white';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Vote Timer: 10s', chart.getDatasetMeta(0).data[0].x,  chart.getDatasetMeta(0).data[0].y);
  }
}
const options = {
  plugins: {
    legend: {
      position: 'right',
    }
  }
};

export function CommandVotesDisplay() {
  return (
    <Doughnut data={data} plugins={[textCenter]} options={options}/>
  )
}
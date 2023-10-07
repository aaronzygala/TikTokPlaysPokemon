import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from "./ui/button"
import { XSquare, Plus } from "lucide-react"
// const express = require('express');
// const app = express();

// // Serve files from a specific directory
// app.use('/static', express.static('../../TikTokPlaysPokemon/users'));

export function ToggleModeButton(): JSX.Element {
  const [mode, setMode] = useState("Chaos");

//   useEffect(() => {

//     return () => {
//     };
//   }, []);

  const toggleMode = async () => {
    try {
      const response = await axios.post(`/api/toggle_mode`);
      var response_mode = response.data.mode
      response_mode = response_mode.charAt(0) + response_mode.substring(1).toLowerCase();

      setMode(response_mode);
    } catch (error) {
      console.error("Error toggling mode:", error);
    }
  };
  return (
    <button 
        className={`mt-5 inline-flex items-center justify-center w-24 h-12 mr-2 transition-colors 
                    duration-150  rounded-lg focus:shadow-outline 
                    ${mode == "Chaos" ? "bg-[#D10000] hover:bg-[#FF0000] shadow-[0_0_20px_3px_rgba(200,100,100,0.6)]" : "bg-[#1E429C] hover:bg-[#2551C0] shadow-[0_0_20px_3px_rgba(100,100,200,0.6)]"}
                    `}
        onClick={()=>toggleMode()}
        >
        {mode}
    </button>
    )
}

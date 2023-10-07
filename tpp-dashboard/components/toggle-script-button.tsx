import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from "./ui/button"
import { XSquare, Plus } from "lucide-react"
import { ClipLoader } from 'react-spinners';
// const express = require('express');
// const app = express();

// // Serve files from a specific directory
// app.use('/static', express.static('../../TikTokPlaysPokemon/users'));

export function ToggleScriptButton(): JSX.Element {
  const [mode, setMode] = useState("Chaos");
  const [isLoading, setIsLoading] = React.useState<boolean>(false)

//   useEffect(() => {

//     return () => {
//     };
//   }, []);

  const toggleScript = async () => {
    try {
      setIsLoading(true); // Set isLoading to true when submitting

      if (isLoading) {
          return; // Prevent double submission
      }
      const response = await axios.post(`/api/restart`);
    //   var response_mode = response.data.mode
    //   response_mode = response_mode.charAt(0) + response_mode.substring(1).toLowerCase();

    //   setMode(response_mode);
    } catch (error) {
      console.error("Error toggling script:", error);
    } finally {
        // Reset isLoading after a short delay (e.g., 2 seconds)
        setTimeout(() => {
            setIsLoading(false);
        }, 2000);
    }
  };
  return (
    <Button 
        className="mt-5 inline-flex items-center justify-center w-24 h-12 mr-2 transition-colors 
        duration-150  rounded-lg focus:shadow-outline bg-[#D10000] hover:bg-[#FF0000] shadow-[0_0_20px_3px_rgba(200,100,100,0.6)] ml-auto mr-auto text-white"
        onClick={()=>toggleScript()}
        disabled={isLoading}
    >
            {isLoading ? (
                        <ClipLoader color={'#ffffff'} size={24}/>
            ): "Restart"}
        {/* <svg fill="#000000" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" viewBox="-47.26 -47.26 567.13 567.13" width="64px" height="64px" stroke="#000000" stroke-width="0.00472615"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g> <g> <rect x="226.658" width="19.289" height="240.197"></rect> </g> </g> <g> <g> <path d="M281.18,46.56l-4.002,18.876c89.934,19.064,155.209,99.73,155.209,191.811c0,108.123-87.961,196.079-196.078,196.079 c-108.119,0-196.079-87.957-196.079-196.079c0-92.091,65.28-172.757,155.219-191.811l-4.003-18.876 C92.647,67.498,20.938,156.104,20.938,257.247c0,118.757,96.612,215.369,215.37,215.369c118.756,0,215.369-96.611,215.369-215.369 C451.677,156.114,379.973,67.507,281.18,46.56z"></path> </g> </g> </g></svg> */}
    </Button>
    )
}

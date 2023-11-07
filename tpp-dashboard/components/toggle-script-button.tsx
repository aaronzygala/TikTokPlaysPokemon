import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from "./ui/button"
import { ClipLoader } from 'react-spinners';

export function ToggleScriptButton(): JSX.Element {
  const [mode, setMode] = useState("Chaos");
  const [isLoading, setIsLoading] = React.useState<boolean>(false)


  const toggleScript = async () => {
    try {
      setIsLoading(true); // Set isLoading to true when submitting

      if (isLoading) {
          return; // Prevent double submission
      }
      const response = await axios.post(`/api/restart`);

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
        className="mt-2 items-center justify-center w-24 h-12 transition-colors 
        duration-150  rounded-lg focus:shadow-outline bg-[#D10000] hover:bg-[#FF0000] shadow-[0_0_20px_3px_rgba(200,100,100,0.6)] ml-auto mr-auto text-white"
        onClick={()=>toggleScript()}
        disabled={isLoading}
    >
            {isLoading ? (
                        <ClipLoader color={'#ffffff'} size={24}/>
            ): "Restart"}
    </Button>
    )
}

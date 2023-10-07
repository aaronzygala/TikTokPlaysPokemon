import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from "./ui/button"
import { XSquare, Plus } from "lucide-react"
import { Input } from './ui/input';
// const express = require('express');
// const app = express();

// // Serve files from a specific directory
// app.use('/static', express.static('../../TikTokPlaysPokemon/users'));

export function NameList({list}): JSX.Element {
  const [names, setNames] = useState([]);
  const [newName, setNewName] = useState('');

  useEffect(() => {
    fetchNames();
    const pollingInterval = setInterval(
      () => fetchNames(),
      5000
    );

    return () => {
      clearInterval(pollingInterval);
    };
  }, []);

  const fetchNames = async () => {
    try {
      const response = await axios.get(`/api/${list}`);
      setNames(response.data.names);
    } catch (error) {
      console.error("Error fetching recent comments:", error);
    }
  };
  const handleAddName = async () => {
    try {
      await axios.post(`/api/${list}/add`, { name: newName });
      setNewName('');
      fetchNames();
    } catch (error) {
      console.error("Error adding name:", error);
    }
  };

  const handleRemoveName = async (nameToRemove) => {
    try {
      await axios.post(`/api/${list}/remove`, { name: nameToRemove });
      fetchNames();
    } catch (error) {
      console.error("Error removing name:", error);
    }
  };
  return (
    <div className="overflow-auto h-[540px]">
      { names.map((name) => (
        <div className="flex items-end p-4 bg-slate-900 rounded-2xl border border-solid border-stone-950">
          <div className="flex items-center mt-auto mb-auto">
            <div className="ml-2">
              <p className="text-sm text-muted-foreground">
                {name}
              </p>
            </div>
          </div> 
          <Button className="ml-auto" variant="outline" size="icon" onClick={()=>handleRemoveName(name)}>
            <XSquare className="h-[1.2rem] w-[1.2rem]" />
            <span className="sr-only">Remove</span>
          </Button>    
        </div>
      ))}
        <div className="flex items-center justify-center mt-2">
            <Input
                  type="text"
                  placeholder="Add username..."
                  className="w-[200px]"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                /> 
            <Button className="ml-2 w-[3rem]" variant="outline" size="icon" onClick={()=>handleAddName()} disabled={newName===''}>
                <Plus className="h-[1.2rem] w-[1.2rem]" />
                <span className="sr-only">Add</span>
            </Button>
        </div>
      </div>
    )
}

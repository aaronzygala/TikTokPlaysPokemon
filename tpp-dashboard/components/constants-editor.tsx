import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Checkbox } from './ui/checkbox';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';

const ConstantsEditor = () => {
  const [constants, setConstants] = useState({});
  const [editedConstants, setEditedConstants] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get('/api/constants');
    //   console.log(response)
      setConstants(response.data.constants);
      setEditedConstants(response.data.constants);
    };

    fetchData();
  }, []);

  const handleInputChange = (constantName, value) => {
    setEditedConstants((prevConstants) => {
      if(editedConstants[constantName].type == "bool"){
        return {
            ...prevConstants,
            [constantName]: {
              ...prevConstants[constantName],
              value: !prevConstants[constantName].value,
            },
          };
      }
      else{
        return {
            ...prevConstants,
            [constantName]: {
              ...prevConstants[constantName],
              value: value,
            },
          };
      }
    });
  };
  

  const handleSave = async () => {
    try {
      await axios.post('/api/save-constants', {
        constants: editedConstants,
      });
      alert('Constants saved successfully!');
    } catch (error) {
      console.error('Error saving constants:', error);
      alert('Error saving constants. Please try again.');
    }
  };

  return (
    <div>
      {Object.entries(constants).map(([constantName, constantValue]) => (
        <div key={constantName} className="grid py-4">
          <Label>{constantName}:</Label>
          {constantValue.type === 'str' && (
            <Input
              type="text"
              value={editedConstants[constantName]?.value || ''}
              onChange={(e) => handleInputChange(constantName, e.target.value)}
            />
          )}
          {constantValue.type === 'int' && (
            <Input
              type="number"
              value={editedConstants[constantName]?.value || ''}
              onChange={(e) => handleInputChange(constantName, e.target.value)}
            />
          )}
          {constantValue.type === 'bool' && (
            <Checkbox
                id={constantName}
                checked={editedConstants[constantName]?.value || false}
                onClick={(e) => handleInputChange(constantName, e.target.checked)}
            />
          )}
        </div>
      ))}
      <Button onClick={handleSave}>Save</Button>
    </div>
  );
};

export default ConstantsEditor;

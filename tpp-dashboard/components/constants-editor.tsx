import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Checkbox } from './ui/checkbox';
import { Input } from './ui/input';
import { Label } from './ui/label';
import { Button } from './ui/button';
import { Card, CardHeader, CardContent, CardTitle, CardDescription } from './ui/card';

const ConstantsEditor = () => {
  const [constants, setConstants] = useState({});
  const [editedConstants, setEditedConstants] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const response = await axios.get('/api/constants');
      console.log(response)
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

  const stringConstants = Object.entries(constants).filter(
    ([constantName, constantValue]) => constantValue.type === 'str'
  );

  const intConstants = Object.entries(constants).filter(
    ([constantName, constantValue]) => constantValue.type === 'int'
  );

  const boolConstants = Object.entries(constants).filter(
    ([constantName, constantValue]) => constantValue.type === 'bool'
  );
  const renderInputByType = (constantName, constantValue) => {
    if (constantValue.type === 'str') {
      return (
        <Input
          className="mt-auto mb-auto ml-4"
          type="text"
          value={editedConstants[constantName]?.value || ''}
          onChange={(e) => handleInputChange(constantName, e.target.value)}
        />
      );
    } else if (constantValue.type === 'int') {
      return (
        <Input
          className="mt-auto mb-auto ml-4"
          type="number"
          value={editedConstants[constantName]?.value || ''}
          onChange={(e) => handleInputChange(constantName, e.target.value)}
        />
      );
    } else if (constantValue.type === 'bool') {
      return (
        <Checkbox
          className="mt-auto mb-auto ml-auto lg:ml-4"
          id={constantName}
          checked={editedConstants[constantName]?.value}
          onClick={(e) => handleInputChange(constantName, e.target.checked)}
        />
      );
    }
  };
  

  return (
    <div className="grid grid-cols-3 gap-x-4">
      <Card>
        <CardHeader>Text:</CardHeader>
        {stringConstants.map(([constantName, constantValue]) => (
          <CardContent key={constantName}>
            <div className="flex flex-col lg:flex-row">
              <p className="text-sm font-semibold">{constantName}: </p>
              {renderInputByType(constantName, constantValue)}
            </div>
          </CardContent>
        ))}
      </Card>

      <Card>
        <CardHeader>Numbers:</CardHeader>
        {intConstants.map(([constantName, constantValue]) => (
          <CardContent key={constantName}>
            <div className="flex flex-col lg:flex-row">
              <p className="text-sm font-semibold">{constantName}: </p>
              {renderInputByType(constantName, constantValue)}
            </div>
          </CardContent>
        ))}
      </Card>

      <Card>
        <CardHeader>Toggle Gifts:</CardHeader>
        {boolConstants.map(([constantName, constantValue]) => (
          <CardContent key={constantName}>
            <div className="flex flex-col lg:flex-row">
              <p className="text-sm font-semibold">{constantName}:</p>
              {renderInputByType(constantName, constantValue)}
            </div>
          </CardContent>
        ))}
      </Card>
      
      <div className="cols-1"></div>
      <Button
        className="mt-4 w-[275px] ml-auto mr-auto"
        onClick={handleSave}>
          <div className="text-lg font-semibold text-white">
          Save
          </div>
      </Button>
    </div>
  );
};

export default ConstantsEditor;

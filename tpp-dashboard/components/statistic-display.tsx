import React, { useEffect, useState } from "react"
import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "./ui/avatar"
import { Button } from "./ui/button"
import { UserPlus2, UserX2, ChevronRight, ChevronLeft } from "lucide-react"
import axios from "axios"; // Import axios for API requests
import { Card, CardTitle, CardHeader, CardContent } from "./ui/card";

export function StatisticDisplay({statName}): JSX.Element {
  const [statValue, setStatValue] = useState(0); // State to hold recent comments
  const [cardTitle, setCardTitle] = useState('');

  useEffect(() => {
    createTitle();
    fetchStatistic();
    const pollingInterval = setInterval(
      () => fetchStatistic(),
      5000
    );

    return () => {
      clearInterval(pollingInterval);
    };
  }, []);

  const fetchStatistic = async () => {
    try {
      const response = await axios.get(`/api/${statName}`);
      setStatValue(response.data.stat);
    } catch (error) {
      console.error(`Error fetching statistic ${statName}:`, error);
    }
  };

  const createTitle = () => {
      if (statName == "followers"){
        setCardTitle("Followers")
      }
      else if (statName == "comments"){
        setCardTitle("Comments")
      }
      else{
        setCardTitle("Gifts")
      }
  }
  
  return (
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-md font-medium">{cardTitle}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">+{statValue}</div>
          </CardContent>
        </Card>
    )
  }
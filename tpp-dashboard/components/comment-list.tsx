import React, { useEffect, useState } from "react"
import {
    Avatar,
    AvatarFallback,
    AvatarImage,
  } from "./ui/avatar"
import { Button } from "./ui/button"
import { UserPlus2, UserX2, ChevronRight, ChevronLeft, MoreHorizontal } from "lucide-react"
import axios from "axios"; // Import axios for API requests

import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuPortal,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu"

function UserDropdownMenu(props: {
  name: string;
  handleBan: () => void;
  handleWhitelist: () => void;
}) {
  const { name, handleBan, handleWhitelist } = props;

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" className="mr-1">
          <MoreHorizontal className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-32">
        <DropdownMenuLabel>{name}</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem onClick={handleWhitelist}>
          <UserPlus2 className="mr-2 h-4 w-4" />
          <span>Whitelist</span>
        </DropdownMenuItem>

        <DropdownMenuItem onClick={handleBan}>
          <UserX2 className="mr-2 h-4 w-4" />
          <span>Ban</span>
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export function CommentList(): JSX.Element {
  const [recentComments, setRecentComments] = useState([]); // State to hold recent comments
  const [currentPage, setCurrentPage] = useState(1);
  const [maxPages, setMaxPages] = useState(0);

  useEffect(() => {
    fetchRecentComments(currentPage);
    const pollingInterval = setInterval(
      () => fetchRecentComments(currentPage),
      5000
    );

    return () => {
      clearInterval(pollingInterval);
    };
  }, [currentPage]);

  const fetchRecentComments = async (page) => {
    try {
      const response = await axios.get(`/api/recent_comments?page=${page}`);
      setRecentComments(response.data.recentComments);
      setMaxPages(response.data.maxPages)
    } catch (error) {
      console.error("Error fetching recent comments:", error);
    }
  };
  const handleBan = async (username) => {
    try {
      console.log("banning " + username)
      await axios.post(`/api/banned/add`, { name: username });
    } catch (error) {
      console.error("Error banning user:", error);
    }
  };
  
  const handleWhitelist = async (username) => {
    try {
      console.log("whitelisting " + username)

      await axios.post(`/api/whitelist/add`, { name: username });
    } catch (error) {
      console.error("Error whitelisting user:", error);
    }
  };
  
  
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };
  return (
    <div className="overflow-auto h-[650px]">
      { recentComments.map((data, index) => (
        <div key={index} className="flex items-end p-3 bg-slate-900 rounded-2xl border border-solid border-stone-950">
            <UserDropdownMenu
              name={data.username}
              handleBan={() => handleBan(data.username)}
              handleWhitelist={() => handleWhitelist(data.username)}
            />         
            <div className="flex items-center mt-auto mb-auto">
            <Avatar className="h-9 w-9">
              <AvatarImage src={data.avatar} alt="Avatar" />
              <AvatarFallback>?</AvatarFallback>
            </Avatar>
            <div className="ml-2">
              <p className="text-sm text-muted-foreground">
                {data.username}
              </p>
            </div>
          </div>    
          <div className="ml-auto font-medium mt-auto mb-auto">{data.comment}</div>
        </div>
      ))}
          <div className="flex justify-center mt-4"> {/* Center pagination controls */}
            <Button className="mr-2" variant="outline" size="icon" onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
              <ChevronLeft className="h-[1.2rem] w-[1.2rem]" />
              <span className="sr-only">Previous Page</span>
            </Button> 
            <span className="px-4 mt-2">
              Page {currentPage} / {maxPages}
            </span>
            <Button className="mr-2" variant="outline" size="icon" onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === maxPages}>
              <ChevronRight className="h-[1.2rem] w-[1.2rem]" />
              <span className="sr-only">Next Page</span>
            </Button> 
          </div>
      </div>
    )
  }
import { Metadata } from "next"
import Image from "next/image"

import { Button } from "../components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "../components/ui/card"
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "../components/ui/tabs"
import { CommandVotesDisplay } from "../components/command-votes-display"
import { CommentList } from "../components/comment-list"
import { ModeToggle } from "@/components/ui/mode-toggle"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import {Input} from "@/components/ui/input"
import {NameList} from "@/components/user-list"
import { ToggleModeButton } from "@/components/toggle-mode-button"
import { ToggleScriptButton } from "@/components/toggle-script-button"

import { StatisticDisplay } from "@/components/statistic-display"
import ToggleScriptTimer from "@/components/toggle-script-timer"
import ConstantsEditor from "@/components/constants-editor"

export const metadata: Metadata = {
  title: "Dashboard",
  description: "Example dashboard app built using the components.",
}

function OverViewTab(){
  return(
      <div className="grid gap-4 md:grid-cols-3">

      <div className="">
        <div className = "grid grid-cols-2 gap-4 pb-4">
          <Card className="col-span-2">
            <CardHeader className="">
              <CardTitle className="text-md font-medium">Toggle Script</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-2 gap-4">
              <div className="pr-1">
                <ToggleScriptButton/>
              </div>
              <div className="ml-auto mt-auto mb-auto mr-5">
                <div className="text-white text-sm">Timer: </div>
                <ToggleScriptTimer/>
              </div>
            </CardContent>
          </Card>

        </div>
        <div className="grid grid-cols-2 gap-4">
          <Card className="">
            <CardHeader className="">
              <CardTitle className="text-sm font-medium">Toggle Mode</CardTitle>
            </CardHeader>
            <CardContent className="">
              <ToggleModeButton/>
            </CardContent>
          </Card>
          <StatisticDisplay statName={"followers"}/>
          <StatisticDisplay statName={"comments"}/>
          <StatisticDisplay statName={"gifts"}/>
        </div>
      </div>

        <Card>
          <CardHeader>
            <CardTitle>Command Votes</CardTitle>
          </CardHeader>
          <CardContent>
            <CommandVotesDisplay />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>
              <div>Recent comments</div>                  
            </CardTitle>
          </CardHeader>
          <CardContent>
            <CommentList/>
          </CardContent>
        </Card>
      </div>
  )
}

function UsersTab(){
  return(
      <div className="grid gap-4 grid-cols-3">

        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Admins</CardTitle>
          </CardHeader>
          <CardContent>
            <NameList list={"admins"}/>
          </CardContent>
        </Card>

        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Whitelist</CardTitle>
          </CardHeader>
          <CardContent>
            <NameList list={"whitelist"}/>
          </CardContent>
        </Card>
        <Card className="col-span-1">
          <CardHeader>
            <CardTitle>Banned</CardTitle>
          </CardHeader>
          <CardContent>
            <NameList list={"banned"}/>
          </CardContent>
        </Card>
    </div>
  )
}

function ConstantsTab(){
  return(
      <div className="">

        <Card className="">
          <CardHeader>
            <CardTitle>Constants</CardTitle>
          </CardHeader>
          <CardContent>
            <ConstantsEditor/>
          </CardContent>
        </Card>

    </div>
  )
}
export default function DashboardPage() {
  return (
      <div className="hidden flex-row md:flex overflow-hidden">
        <div className="flex-1 space-y-4 p-8 pt-6">
          <div className="flex items-center justify-between space-y-2">
            <h2 className="text-2xl font-bold tracking-tight">TikTok Plays Gameboy Dashboard</h2>
          </div>
          <div className="flex items-center space-x-2 hidden">
            <ToggleScriptTimer />
          </div>
          <Tabs defaultValue="overview" className="">
            <TabsList>
              <TabsTrigger value="overview">Overview</TabsTrigger>
              <TabsTrigger value="users">
                Users
              </TabsTrigger>
              <TabsTrigger value="constants">
                Constants
              </TabsTrigger>
            </TabsList>
            <TabsContent value="overview" className="space-y-4">
              <OverViewTab/>
            </TabsContent>
            <TabsContent value="users">
              <UsersTab/>
            </TabsContent>
            <TabsContent value="constants">
              <ConstantsTab/>
            </TabsContent>
          </Tabs>
        </div>
      </div>
  )
}
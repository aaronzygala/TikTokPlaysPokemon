"use client"

import * as React from "react"
import { cn } from "@/lib/utils"
import { ClipLoader } from "react-spinners"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Label } from "./ui/label"
import { useRouter } from 'next/router';

interface UserAuthFormProps extends React.HTMLAttributes<HTMLDivElement> {}

export function UserAuthForm({ className, ...props }: UserAuthFormProps) {
  const router = useRouter()
  const [isLoading, setIsLoading] = React.useState<boolean>(false)
  const [password, setPassword] = React.useState<string>("")
  const [username, setUsername] = React.useState<string>("")

  async function onSubmit(event: React.SyntheticEvent) {
    event.preventDefault();
    setIsLoading(true); // Set isLoading to true when submitting

    if (isLoading) {
      return; // Prevent double submission
    }
  
    try {
        const url = "/api/login";
        const data = {
            username: username,
            password: password
        };
        const headers = {
            "Content-Type": "application/json"
        };
    
        fetch(url, {
            method: "POST",
            headers: headers,
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.status === 200) {
                // Handle successful login
                console.log("Login successful");
                setTimeout(() => {
                    setIsLoading(false);
                    router.push("/dashboard")
                }, 500);
            } else if (response.status === 401) {
                // Handle unauthorized login
                console.error("Login failed: Unauthorized");
            } else {
                // Handle other responses like 4xx or 5xx
                console.error("Login failed: Unknown error");
        }
        })
        .catch(error => {
            // Handle network errors or exceptions
            console.error("An error occurred:", error);
        });
    } catch (error) {
        // Handle any synchronous errors within the try block
        console.error("An error occurred:", error);
    } finally {
        // Reset isLoading after a short delay (e.g., 2 seconds)
        setTimeout(() => {
            setIsLoading(false);
        }, 2000);
    }
  }    
    
  return (
    <div className={cn("grid gap-6", className)} {...props}>
      <form onSubmit={onSubmit}>
        <div className="grid gap-2">
          <div className="grid gap-1">
            <h2 className="text-3xl font-bold tracking-tight mb-4">Login</h2>

            <Label className="sr-only" htmlFor="email">
              Email
            </Label>
            <Input
              id="username"
              placeholder="Username"
              type="default"
              autoCapitalize="none"
              autoComplete="default"
              autoCorrect="off"
              disabled={isLoading}
              value={username}
              onChange={event => setUsername(event.target.value)}
            />
            <Input
              id="password"
              placeholder="Password"
              type="password"
              autoCapitalize="none"
              autoComplete="email"
              autoCorrect="off"
              disabled={isLoading}
              value={password}
              onChange={event => setPassword(event.target.value)}            />
          </div>
          <div className="justify-self-center">
            {/* <Link href="/dashboard"> */}
                <Button className="w-[100px]" disabled={isLoading} onSubmit={onSubmit}>
                    {isLoading ? (
                        <ClipLoader color={'#ffffff'} size={24}/>
                    ): "Sign In"}
                </Button>
            {/* </Link> */}
          </div>

        </div>
      </form>
    </div>
  )
}
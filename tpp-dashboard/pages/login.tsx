import { Metadata } from "next"
import { UserAuthForm } from "@/components/user-auth-form"

export const metadata: Metadata = {
  title: "Login",
  description: "Log in to your TTPP Dashboard",
}


export default function LoginPage() {
  return (
      <div className="hidden flex-col md:flex w-[350px] ml-auto mr-auto mt-80">
        <UserAuthForm/>
      </div>
  )
}
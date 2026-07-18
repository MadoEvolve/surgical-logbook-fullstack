import { useState } from "react"
import LoginForm from "./LoginForm"
import RegisterForm from "./RegisterForm"

export default function AuthPage ({setUser}){
    // set a state initiate it to login page
    const [mode, setMode]= useState("login")
    const [message, setMessage] = useState("")

    // Ternary if mode login render Loginform set the button to change state to register if clicked
    // else render RegisterForm and do exactly the opposite
    return(
        <div>
            {message && <p className="message">{message}</p>}

            {mode === "login" ? (<LoginForm switchToRegister ={()=> setMode("register")}
            setMessage={setMessage} setUser={setUser}/>)
            : (<RegisterForm switchToLogin={()=> setMode("login")}
            setMessage={setMessage} />)

            }
        </div>
    )
}
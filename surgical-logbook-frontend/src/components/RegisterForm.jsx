import { useState } from "react"
// RegisterForm component

export default function RegisterForm({switchToLogin, setMessage}){

    // userinput
    const [username,setUsername] = useState("")
    const [email,setEmail] = useState("")
    const [registration, setRegistration] = useState("")
    const [password, setPassword] = useState("")
    const [error,setError] = useState("")

    // submit form
    async function handlesubmit(event){
        event.preventDefault()
        const requestBody = {username,email,registration,password}
        // send details to api
        const response = await fetch(
            "http://127.0.0.1:8000/users/",
            {method:"POST",
             headers: {"Content-Type":"application/json"},
             body:JSON.stringify(requestBody)})
        // unpack response
        const data = await response.json()
        
        //fork
        if (response.ok) {
            setError("")
            setMessage("Account created successfully. Please login.")
            switchToLogin()
        }
        else {setError(data.detail)}
        }



    return(
        <div className="register-form">
            <h2>Create An Account</h2>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handlesubmit}>
                <label>
                    Username
                    <input type="text" name="username" required
                    value = {username} onChange={(event)=>setUsername(event.target.value)}/>
                </label>
                <label>
                    Registration
                    <input type="text" name="registration" placeholder="GMC Number" required
                    value = {registration} onChange={(event)=>setRegistration(event.target.value)}/>
                </label>
                <label>
                    email
                    <input type="email" name="email" required
                    value = {email} onChange={(event)=>setEmail(event.target.value)}/>
                </label>
                <label>
                    password
                    <input type="password" name="password" required
                    value = {password} onChange={(event)=>setPassword(event.target.value)}/>
                </label>
                <button className="primary-btn" type="submit">Create Account</button>
            </form>

            <p>
                Already a member ? {" "}
                <button className="primary-btn" type="button" onClick={switchToLogin}>
                    Login
                </button>
            </p>

        </div>
    )
}
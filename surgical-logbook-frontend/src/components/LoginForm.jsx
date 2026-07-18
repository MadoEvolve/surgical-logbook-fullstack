import { useState } from "react"
import { useNavigate } from "react-router-dom"
// LoginForm component

export default function LoginForm({switchToRegister, setMessage, setUser}) {

    const navigate = useNavigate()
    // userinput
    const [registration, setRegistration] = useState("")
    const [password, setPassword] = useState("")
    
    const [error,setError] = useState("")

    // submit form
    async function handleSubmit(event) {
        event.preventDefault()
        // api expects formdata not json
        // convert to what api expects
        const formData = new URLSearchParams()

        formData.append("username", registration)
        formData.append("password", password)
        // send login details to api end point
        const response = await fetch(
        "http://127.0.0.1:8000/authentication/login",
        {method: "POST", body: formData})

        // unpack response
        const data = await response.json()

        if (response.ok) {
        localStorage.setItem("token", data.access_token)

        const meResponse = await fetch(
            "http://127.0.0.1:8000/users/me",
            {
                headers: {
                    Authorization: `Bearer ${data.access_token}`
                }
            }
        )

        const me = await meResponse.json()
        const currentUser = me.data

        setUser(currentUser)
        localStorage.setItem("user", JSON.stringify(currentUser))

        if (currentUser.role === "admin") {
            navigate("/admin")
        } else {
            navigate("/dashboard")
        }
        }
        else {
            setMessage("")
            setError(data.detail)} 
    }
    return (

        <div className="login-form">
            <h2>Login</h2>
            {error && <p className="error">{error}</p>}
            <form onSubmit={handleSubmit}>
                <label>
                    Registration
                    <input type="text" name="registration" required 
                    value={registration} onChange={(event) => setRegistration(event.target.value)}/>
                </label>

                <label>
                    Password
                    <input type="password" name="password" required 
                    value={password} onChange={(event) => setPassword(event.target.value)}/>
                </label>

                <button className="primary-btn" type="submit">Log In</button>
            </form>
            <p>
                {/* React way of ensuring space */}
                No Account ? {" "}
                <button className="primary-btn" type="button" onClick={switchToRegister}>
                    Create Account
                </button>
            </p>
        </div>
    )
}

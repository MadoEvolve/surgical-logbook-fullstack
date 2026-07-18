
import { useEffect, useState } from "react"

export default function SettingsPage() {
    const [user, setUser] = useState(null)

    const [username, setUsername] = useState("")
    const [registration, setRegistration] = useState("")
    const [email, setEmail] = useState("")
    const [password, setPassword] = useState("")

    const [success, setSuccess] = useState("")
    const [error, setError] = useState("")
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchUser()
    }, [])

    async function fetchUser() {
        const token = localStorage.getItem("token")

        const response = await fetch("http://127.0.0.1:8000/users/me", {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })

        const data = await response.json()

        if (response.ok) {
            setUser(data.data)
            setUsername(data.data.username)
            setRegistration(data.data.registration)
            setEmail(data.data.email)
        } else {
            setError(data.detail || "Unable to load user.")
        }

        setLoading(false)
    }

    async function handleSubmit(e) {
        e.preventDefault()

        setSuccess("")
        setError("")

        const token = localStorage.getItem("token")

        const response = await fetch(
            `http://127.0.0.1:8000/users/${user.id}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`
                },
                body: JSON.stringify({
                    username,
                    registration,
                    email,
                    password
                })
            }
        )

        const data = await response.json()

        if (response.ok) {
            setSuccess("Settings updated successfully.")
            setPassword("")
            setUser(data.data)
        } else {
            setError(data.detail || "Update failed.")
        }
    }

    if (loading) {
        return <p>Loading...</p>
    }

    return (
        <div className="page-form">
            <h2>Account Settings</h2>

            {success && <p style={{ color: "green" }}>{success}</p>}
            {error && <p className="error">{error}</p>}

            <form onSubmit={handleSubmit}>
                <label>
                    Username
                    <input value={username}
                        onChange={(e) => setUsername(e.target.value)}/>
                </label>

                <label>
                    Registration
                    <input value={registration}
                        onChange={(e) => setRegistration(e.target.value)}/>
                </label>

                <label>
                    Email
                    <input type="email" value={email}
                        onChange={(e) => setEmail(e.target.value)}/>
                </label>

                <label>
                    New Password
                    <input type="password" value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Leave blank to keep current password"/>
                </label>

                <button className="primary-btn" type="submit">
                    Save Changes
                </button>
            </form>
        </div>
    )
}
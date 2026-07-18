
import { useEffect } from "react"
import { Navigate } from "react-router-dom"

export default function Logout({ setUser }) {

    useEffect(() => {
        localStorage.removeItem("token")
        localStorage.removeItem("user")
        setUser(null)
    }, [setUser])

    return <Navigate to="/" replace />
}
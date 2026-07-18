import "./App.css"
import { useState } from "react"
import { Routes, Route } from "react-router-dom"
import HomePage from "./components/HomePage"
import Navbar from "./components/Navbar"
import AuthPage from "./components/AuthPage"
import ProtectedRoute from "./components/ProtectedRoute"
import AdminRoute from "./components/AdminRoute"
import LogForm from "./components/LogForm"
import Dashboard from "./components/Dashboard"
import LogsPage from "./components/LogsPage"
import SettingsPage from "./components/SettingsPage"
import Logout from "./components/Logout"
import AdminDashboard from "./components/AdminDashboard"
import ProceduresPage from "./components/ProceduresPage"
import HospitalsPage from "./components/HospitalsPage"
import UsersPage from "./components/UsersPage"
import SearchLogs from "./components/SearchLogs"

export default function App() {
    const [user, setUser] = useState(() => {
    const saved = localStorage.getItem("user")
    return saved ? JSON.parse(saved) : null})

    return (
        <>
            <Navbar user={user} />

            <Routes>
                <Route path="/" element={<HomePage />} />

                <Route path="/login" element={<AuthPage setUser={setUser} />} />

                <Route path="/dashboard" element={<ProtectedRoute><Dashboard user={user}/></ProtectedRoute>} />
                <Route path="/add-log" element={<ProtectedRoute><LogForm mode="create" /></ProtectedRoute>} />

                <Route path="/logs" element={<ProtectedRoute><LogsPage/></ProtectedRoute>} />

                <Route path="/settings" element={<ProtectedRoute><SettingsPage/></ProtectedRoute>} />

                <Route path="/logout" element={<Logout setUser={setUser}/>}/>
                <Route path="/admin" element={<AdminRoute><AdminDashboard user={user}/></AdminRoute>} />
                <Route path="/procedures" element={<AdminRoute><ProceduresPage/></AdminRoute>} />
                <Route path="/hospitals" element={<AdminRoute><HospitalsPage/></AdminRoute>} />
                <Route path="/users" element={<AdminRoute><UsersPage/></AdminRoute>} />
                <Route path="/all-logs" element={<AdminRoute><SearchLogs/></AdminRoute>} />
            </Routes>
        </>
    )
}


import { useState, useEffect } from "react"

export default function AdminDashboard({user}) {

    const token = localStorage.getItem("token")
    const [stats, setStats] = useState(null)


    async function fetchStats() {
        const response = await fetch(
            "http://127.0.0.1:8000/stats/admin",
            {
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            }
        )

        const data = await response.json()
        setStats(data.data)
    }

    useEffect(() => {
        fetchStats()
    }, [])

    if (!user || !stats) return <p>Loading Dashboard...</p>
    return (

    <div className="dashboard">
        <h2>System Overview</h2>
        <strong>Welcome, {user.username}.</strong>

        <div className="card-grid">
            <div className="card">
                <h3>Total Users</h3>
                <p>{stats.total_users}</p>
            </div>

            <div className="card">
                <h3>Active Users</h3>
                <p>{stats.active_users}</p>
            </div>

            <div className="card">
                <h3>Total Logs</h3>
                <p>{stats.total_logs}</p>
            </div>
        </div>

        <h3>Hospital Activity</h3>

        <table className="table-data">
            <thead>
                <tr>
                    <th>Hospital</th>
                    <th>Specialty</th>
                    <th>Logs</th>
                </tr>
            </thead>

            <tbody>
                {stats.hospital_specialty_stats.map((item) => (
                    <tr key={`${item.hospital}-${item.specialty}`}>
                        <td>{item.hospital}</td>
                        <td>{item.specialty}</td>
                        <td>{item.logs}</td>
                    </tr>
                ))}
            </tbody>
        </table>
    </div>
)
}
import { useState, useEffect } from "react"




export default function Dashboard({user}) {

    const token = localStorage.getItem("token")
    const [stats, setStats] = useState(null)


    async function fetchStats() {
        const response = await fetch(
            "http://127.0.0.1:8000/stats/me",
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
            <h2>Welcome Dr {user.username} 👋</h2> 

            <h3>Total Logs: {stats.total_logs}</h3>

            <h3>Specialty Breakdown</h3>
            <div className="card-grid">
                {Object.entries(stats.specialty_breakdown).map(([k, v]) => (
                    <div key={k} className="card">
                        <h4>{k}</h4>
                        <p>{v} logs</p>
                    </div>
                ))}
            </div>

            <h3>Role Breakdown</h3>
            <div className="card-grid">
                {Object.entries(stats.role_breakdown).map(([k, v]) => (
                    <div key={k} className="card">
                        <h4>{k}</h4>
                        <p>{v} cases</p>
                    </div>
                ))}
            </div>
        </div>
    )
}
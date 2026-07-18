import { Link } from "react-router-dom"

const guestLinks = [
    { label: "Login", to: "/login" }
]

const userLinks = [
    { label: "Dashboard", to: "/dashboard" },
    { label: "My Logs", to: "/logs" },
    { label: "Add Log", to: "/add-log" },
    { label: "Settings", to: "/settings" },
    { label: "Logout", to: "/logout" }
]

const adminLinks = [
    { label: "Admin Dashboard", to: "/admin" },
    { label: "Procedures", to: "/procedures" },
    { label: "Hospitals", to: "/hospitals" },
    { label: "Users", to: "/users" },
    { label: "All Logs", to: "/all-logs" },
    { label: "Logout", to: "/logout" }
]
export default function Navbar({ user }) {

    let links
    if (!user)
    links = guestLinks

    else if (user.role === "admin")
        links = adminLinks

    else
        links = userLinks

    return (
        <nav className="navbar">

            <Link to="/" style={{ textDecoration: "none" }}>
                <h1>Surgical Logbook</h1>
            </Link>

            <ul className="nav-links">
                {links.map(link => (
                    <li key={link.label}>
                        <Link to={link.to}>
                            {link.label}
                        </Link>
                    </li>
                ))}
            </ul>
        </nav>
    )
}
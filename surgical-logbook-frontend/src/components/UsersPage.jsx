import { useState, useEffect } from "react"

export default function UsersPage(){

    const [users,setUsers] = useState([])
    const [deleteUser, setDeleteUser] = useState(null)
    const [error, setError] = useState("")
    // pagination
    const PAGE_SIZE = 20
    const [page, setPage] = useState(1)
    const totalPages = Math.ceil(users.length / PAGE_SIZE)
    const start = (page - 1) * PAGE_SIZE
    const end = start + PAGE_SIZE
    const visibleUsers = users.slice(start, end)

    async function fetchUsers(){
        const token = localStorage.getItem("token")
        const response = await fetch(
        "http://127.0.0.1:8000/users/summary",
        {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })

        if (response.ok) {
            const data = await response.json()
            setUsers(data.data)
            setDeleteUser(null)
            setError("")
    }else{
        const data = await response.json()
        setError(data.detail)}
    }

    useEffect(()=> {fetchUsers()},[])

    async function handleDelete() {
        const token = localStorage.getItem("token")
        const response = await fetch(
        `http://127.0.0.1:8000/users/${deleteUser.id}`,
        {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
        
    if (response.ok) {
        setUsers(prev => prev.filter(u => u.id !== deleteUser.id))
        setDeleteUser(null)
        setError("")
    }else{
        const data = await response.json()
        setError(data.detail)}
    }
    
    return (
        <>
            <div className="procedure-list">
                <h2>All Users</h2>
                <table className="table-data">
                    <thead>
                        <tr>
                        <th>Username</th>
                        <th>Registration</th>
                        <th>Email</th>
                        <th>Role</th>
                        <th>Total Logs</th>
                        <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {visibleUsers.map(u=>
                            <tr key={u.id}>
                                <td>{u.username}</td>
                                <td>{u.registration}</td>
                                <td>{u.email}</td>
                                <td>{u.role}</td>
                                <td>{u.total_logs}</td>
                                {/* DELETE ICON */}
                                <td onClick={(e) => {
                                    setError("")
                                    setDeleteUser(u)
                                }}>
                                🗑️
                            </td>
                            </tr>
                        )}
                    </tbody>
                </table>
                <div className="pagination">
                <button onClick={() => setPage(p => p - 1)}
                    disabled={page === 1}>
                    Previous
                </button>

                <span>
                    Page {page} of {totalPages || 1}
                </span>

                <button onClick={() => setPage(p => p + 1)}
                    disabled={page === totalPages || totalPages === 0}>
                    Next
                </button>
            </div>
            </div>
            {/* DELETE CONFIRM MODAL */}
        
            {deleteUser && (
                <div className="modal-backdrop" onClick={() => {
                    setDeleteUser(null)
                     setError("")}}>
                    <div className="modal danger" onClick={(e) => e.stopPropagation()}>
                        <h3>Confirm Delete</h3>
                        {error && <p className="error">{error}</p>}
                        <p>Are you sure you want to delete:</p>

                        <p>
                            <strong>{deleteUser.registration}</strong>
                        </p>

                        <div style={{ display: "flex", gap: "10px" }}>
                            <button onClick={() => {
                                setDeleteUser(null)
                                setError("")}}>
                                Cancel
                            </button>

                            <button className="danger-btn" onClick={handleDelete}>
                                Delete
                            </button>
                        </div>
                    </div>
                </div>)}
        </>
    )
}
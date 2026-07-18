import { useState, useEffect } from "react"
import LogForm from "./LogForm"

export default function LogsPage() {
    const [logs, setLogs] = useState(null)
    const [selectedLog, setSelectedLog] = useState(null)
    const [isEditing, setIsEditing] = useState(false)
    const [selectedNotes, setSelectedNotes] = useState(null)
    const [deleteLog, setDeleteLog] = useState(null)
    const [offset, setOffset] = useState(0)
    const [total, setTotal] = useState(0)
    const PAGE_SIZE = 10

    async function fetchLogs() {
        const token = localStorage.getItem("token")

        const response = await fetch(`http://127.0.0.1:8000/logs/me?offset=${offset}&limit=${PAGE_SIZE}`,
        {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })

        const data = await response.json()
        setLogs(data.data.result)
        setTotal(data.data.total)
        
    }

    useEffect(() => {
        fetchLogs()
    }, [offset])

    if (!logs) return <p>Loading Profile...</p>

    // handle delete log
    async function handleDelete() {
    const token = localStorage.getItem("token")

    const response = await fetch(
        `http://127.0.0.1:8000/logs/${deleteLog.id}`,
        {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        }
    )

    if (response.ok) {
        setLogs(prev => prev.filter(log => log.id !== deleteLog.id))
        setTotal(prev => prev - 1)
        setDeleteLog(null)
    }
    
    }
    // update log table instantly
    function handleLogUpdate(updatedLog) {
    setLogs(prev =>
        prev.map(l => l.id === updatedLog.id ? updatedLog : l))

    setSelectedLog(null)
    setIsEditing(false)
}
    return (
        <div className="page-container">

            {/* TABLE */}
            <table className="table-data">
                <thead>
                    <tr>
                        <th>Procedure</th>
                        <th>Hospital</th>
                        <th>Role</th>
                        <th>Notes</th>
                        <th></th>
                    </tr>
                </thead>

                <tbody>
                    {logs.map(log => (
                        <tr
                            key={log.id}
                            onClick={() => setSelectedLog(log)}
                            style={{ cursor: "pointer" }}
                        >
                            <td>{log.procedure_name}</td>
                            <td>{log.hospital_name}</td>
                            <td>{log.role}</td>

                            {/* NOTES ICON */}
                            <td
                                onClick={(e) => {
                                    e.stopPropagation()
                                    setSelectedNotes(log.notes)
                                }}
                            >
                                {log.notes ? "📝" : "—"}
                            </td>

                            {/* DELETE ICON */}
                            <td
                                onClick={(e) => {
                                    e.stopPropagation()
                                    setDeleteLog(log)
                                }}
                            >
                                🗑️
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="pagination">
                <button
                    onClick={() => setOffset(prev => Math.max(prev - PAGE_SIZE, 0))}
                    disabled={offset === 0}
                >
                    ← Previous
                </button>

                <span>
                    {offset / PAGE_SIZE + 1} / {Math.ceil(total / PAGE_SIZE)}
                </span>

                <button
                    onClick={() => setOffset(prev => prev + PAGE_SIZE)}
                    disabled={offset + PAGE_SIZE >= total}
                >
                    Next →
                </button>
            </div>

            {/* LOG DETAIL MODAL */}
            {selectedLog && (
            <div className="modal-backdrop"
                onClick={() => {setSelectedLog(null); setIsEditing(false)}}>
            <div className="modal"
                onClick={(e) => e.stopPropagation()}>
            
            {/* if not editing else */}
            {!isEditing ? (
                <>
                    <h3>{selectedLog.procedure_name}</h3>
                    <p>{selectedLog.hospital_name}</p>
                    <p>{selectedLog.role}</p>

                    <button onClick={() => setIsEditing(true)}>
                        Edit
                    </button>

                    <button onClick={() => {setSelectedLog(null); setIsEditing(false)}}>
                        Close
                    </button>
                </>) : (
                <>
                    <LogForm mode="edit" log={selectedLog} onSuccess={handleLogUpdate}/>

                    <button onClick={() => setIsEditing(false)}>
                        Cancel
                    </button>
                </>)}
                </div>
                </div>
            )}


            {/* NOTES MODAL */}
            {selectedNotes && (
                <div className="modal-backdrop" onClick={() => setSelectedNotes(null)}>
                    <div className="modal" onClick={(e) => e.stopPropagation()}>
                        <h3>Notes</h3>
                        <p>{selectedNotes || "No notes recorded"}</p>

                        <button onClick={() => setSelectedNotes(null)}>
                            Close
                        </button>
                    </div>
                </div>
            )}


            {/* DELETE CONFIRM MODAL */}
            {deleteLog && (
                <div className="modal-backdrop" onClick={() => setDeleteLog(null)}>
                    <div className="modal danger" onClick={(e) => e.stopPropagation()}>
                        <h3>Confirm Delete</h3>

                        <p>Are you sure you want to delete:</p>

                        <p>
                            <strong>{deleteLog.procedure_name}</strong>
                        </p>

                        <div style={{ display: "flex", gap: "10px" }}>
                            <button onClick={() => setDeleteLog(null)}>
                                Cancel
                            </button>

                            <button className="danger-btn" onClick={handleDelete}>
                                Delete
                            </button>
                        </div>
                    </div>
                </div>
            )}

        </div>
    )
}
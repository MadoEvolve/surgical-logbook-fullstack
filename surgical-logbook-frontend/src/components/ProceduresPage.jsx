import { useState, useEffect } from "react"
import ProcedureForm from "./ProcedureForm"


export default function ProceduresPage(){
    // read
    const [procedures, setProcedures] = useState([])
    const [specialty, setSpecialty] = useState("")
    const specialties = [...new Set(procedures.map(p => p.specialty))]
    const filteredProcedures = procedures.filter(procedure=>procedure.specialty === specialty)
    // create update delete
    const [selectedProcedure, setSelectedProcedure]= useState(null)
    const [deleteProcedure, setDeleteProcedure] = useState(null)
    const [showCreateForm, setShowCreateForm] = useState(false)
    // pagination
    const PAGE_SIZE = 20
    const [page, setPage] = useState(1)
    const totalPages = Math.ceil(filteredProcedures.length / PAGE_SIZE)
    const start = (page - 1) * PAGE_SIZE
    const end = start + PAGE_SIZE

    const visibleProcedures = filteredProcedures.slice(start, end)
    const [error, setError] = useState("")

    async function fetchProcedures() {
        const response = await fetch("http://127.0.0.1:8000/procedures/")
        const data = await response.json()
        setProcedures(data.data)
    }

    useEffect(() => {
    fetchProcedures()
    }, [])


    async function handleDelete() {
        const token = localStorage.getItem("token")
        const response = await fetch(
        `http://127.0.0.1:8000/procedures/${deleteProcedure.id}`,
        {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
    
    if (response.ok) {
        setProcedures(prev => prev.filter(p => p.id !== deleteProcedure.id))
        setDeleteProcedure(null)
        setError("")
    }else{
        const data = await response.json()
        setError(data.detail)}
}   


    return (
        <>
        <div className="page-container">
            <h2>Procedures Per Specialty</h2>
            <button className="primary-btn"
                onClick={() => setShowCreateForm(true)}>
                + Add Procedure
            </button>
            <select value={specialty}
            onChange={(e) => {setSpecialty(e.target.value)
                setPage(1)}}>
                <option value="">Select specialty</option>
                {specialties.map(s => {
                const count = procedures.filter(p => p.specialty === s).length

                return (
                <option key={s} value={s}>
                    {s} ({count})
                </option>
                )
                })}
            </select>
            {/* Table if Specialty selected */}
            {specialty ? (
                <>
                <table className="table-data">
                    <thead>
                        <tr>
                            <th>Procedure Name</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {visibleProcedures.map(p=> (
                            <tr key={p.id}
                            onClick={() => setSelectedProcedure(p)}
                            style={{ cursor: "pointer" }}>
                                <td>{p.name}</td>
                                {/* DELETE ICON */}
                            <td onClick={(e) => {
                                    e.stopPropagation()
                                    setDeleteProcedure(p)
                                    setError("")
                                }}
                            >
                                🗑️
                            </td>
                            </tr>
                        )
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
            </>
            ): (<p>Choose A Specialty ...</p>)}
                </div>
        
        {/* DELETE CONFIRM MODAL */}
        
            {deleteProcedure && (
                <div className="modal-backdrop" onClick={() => setDeleteProcedure(null)}>
                    <div className="modal danger" onClick={(e) => e.stopPropagation()}>
                        <h3>Confirm Delete</h3>
                        {error && <p className="error">{error}</p>}
                        <p>Are you sure you want to delete:</p>

                        <p>
                            <strong>{deleteProcedure.name}</strong>
                        </p>

                        <div style={{ display: "flex", gap: "10px" }}>
                            <button onClick={() => {
                                setDeleteProcedure(null)
                                setError("")}}>
                                Cancel
                            </button>

                            <button className="danger-btn" onClick={handleDelete}>
                                Delete
                            </button>
                        </div>
                    </div>
                </div>)}
        {/* Edit procedure */}
        {selectedProcedure && (
        <div className="modal-backdrop"
            onClick={() => setSelectedProcedure(null)}>
            <div className="modal"
                onClick={(e) => e.stopPropagation()}>
                <ProcedureForm mode="edit" selectedProcedure={selectedProcedure}
                    onSuccess={() => {
                        fetchProcedures()
                        setSelectedProcedure(null)
                    }}
                />
            </div>
        </div>
        )}
        
        {/* create procedure */}
        {showCreateForm && (
        <div className="modal-backdrop"
         onClick={() => setShowCreateForm(false)}>
            <div className="modal"
                onClick={(e) => e.stopPropagation()}>
                <ProcedureForm mode="create"
                    onSuccess={() => {
                        fetchProcedures()
                        setShowCreateForm(false)
                    }}
                />
            </div>
        </div>
    )}
        </>)
}
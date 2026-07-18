import { useState, useEffect } from "react"
import HospitalForm from "./HospitalForm"


export default function HospitalsPage(){
    // read
    const [hospitals, setHospitals] = useState([])
    const [location, setLocation] = useState("")
    const locations = [...new Set(hospitals.map(h => h.location))]
    const filteredHospitals = hospitals.filter(hospital=>hospital.location === location)
    // create update delete
    const [selectedHospital, setSelectedHospital]= useState(null)
    const [deleteHospital, setDeleteHospital] = useState(null)
    const [showCreateForm, setShowCreateForm] = useState(false)
    // pagination
    const PAGE_SIZE = 20
    const [page, setPage] = useState(1)
    const totalPages = Math.ceil(filteredHospitals.length / PAGE_SIZE)
    const start = (page - 1) * PAGE_SIZE
    const end = start + PAGE_SIZE

    const visibleHospitals = filteredHospitals.slice(start, end)
    const [error, setError] = useState("")

    async function fetchHospitals() {
        const response = await fetch("http://127.0.0.1:8000/hospitals/")
        const data = await response.json()
        setHospitals(data.data)
    }

    useEffect(() => {
    fetchHospitals()
    }, [])


    async function handleDelete() {
        const token = localStorage.getItem("token")
        const response = await fetch(
        `http://127.0.0.1:8000/hospitals/${deleteHospital.id}`,
        {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
        
    if (response.ok) {
        setHospitals(prev => prev.filter(h => h.id !== deleteHospital.id))
        setDeleteHospital(null)
        setError("")
    }else{
        const data = await response.json()
        setError(data.detail)}
}   


    return (
        <>
        <div className="procedures-list">
            <h2>Hospitals per Location</h2>
            <button className="primary-btn"
                onClick={() => setShowCreateForm(true)}>
                + Add Hospital
            </button>
            <select value={location}
            onChange={(e) => {setLocation(e.target.value)
                setPage(1)}}>
                <option value="">Select Location</option>
                {locations.map(l => {
                const count = hospitals.filter(h => h.location === l).length

                return (
                <option key={l} value={l}>
                    {l} ({count})
                </option>
                )
                })}
            </select>
            {/* Table if Specialty selected */}
            {location ? (
                <>
                <table className="table-data">
                    <thead>
                        <tr>
                            <th>Hospital Name</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {visibleHospitals.map(h=> (
                            <tr key={h.id}
                            onClick={() => setSelectedHospital(h)}
                            style={{ cursor: "pointer" }}>
                                <td>{h.name}</td>
                                {/* DELETE ICON */}
                            <td onClick={(e) => {
                                    e.stopPropagation()
                                    setError("")
                                    setDeleteHospital(h)
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
            ): (<p>Choose A Location ...</p>)}
                </div>
        
        {/* DELETE CONFIRM MODAL */}
        
            {deleteHospital && (
                <div className="modal-backdrop" onClick={() => {
                    setDeleteHospital(null)
                     setError("")}}>
                    <div className="modal danger" onClick={(e) => e.stopPropagation()}>
                        <h3>Confirm Delete</h3>
                        {error && <p className="error">{error}</p>}
                        <p>Are you sure you want to delete:</p>

                        <p>
                            <strong>{deleteHospital.name}</strong>
                        </p>

                        <div style={{ display: "flex", gap: "10px" }}>
                            <button onClick={() => {
                                setDeleteHospital(null)
                                setError("")}}>
                                Cancel
                            </button>

                            <button className="danger-btn" onClick={handleDelete}>
                                Delete
                            </button>
                        </div>
                    </div>
                </div>)}
        {/* Edit Hospital */}
        {selectedHospital&& (
        <div className="modal-backdrop"
            onClick={() => setSelectedHospital(null)}>
            <div className="modal"
                onClick={(e) => e.stopPropagation()}>
                <HospitalForm mode="edit" selectedHospital={selectedHospital}
                    onSuccess={() => {
                        fetchHospitals()
                        setSelectedHospital(null)
                    }}
                />
            </div>
        </div>
        )}
        
        {/* create Hospital*/}
        {showCreateForm && (
        <div className="modal-backdrop"
         onClick={() => setShowCreateForm(false)}>
            <div className="modal"
                onClick={(e) => e.stopPropagation()}>
                <HospitalForm mode="create"
                    onSuccess={() => {
                        fetchHospitals()
                        setShowCreateForm(false)
                    }}
                />
            </div>
        </div>
    )}
        </>)
}
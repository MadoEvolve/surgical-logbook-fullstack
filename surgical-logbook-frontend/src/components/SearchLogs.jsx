import { useState, useEffect } from "react"

export default function SearchLogs(){
    // procedures per specialty
    const [procedures, setProcedures] = useState([])
    const [specialty, setSpecialty] = useState("")
    const [procedureId, setProcedureId] = useState("")

    const specialties = [...new Set(procedures.map(p => p.specialty))]
    const filteredProcedures = procedures.filter(p => p.specialty === specialty)

    // hospitals per location
    const [hospitals, setHospitals] = useState([])
    const [location, setLocation] = useState("")
    const [hospitalId, setHospitalId] = useState("")

    const locations = [...new Set(hospitals.map(h => h.location))]
    const filteredHospitals = hospitals.filter(h => h.location === location)

    // user
    const [users, setUsers] = useState([])
    const [userId, setUserId] = useState("")
    // date from, dat to
    const [fromDate, setFromDate] = useState("")
    const [toDate, setToDate] = useState("")
    
    // query results
    const [searchResults, setSearchResults] = useState([])
    const [error, setError] = useState("")
    // fetch procedures & hospitals
    async function fetchProcedures() {
        const response = await fetch("http://127.0.0.1:8000/procedures/")
        const data = await response.json()
        setProcedures(data.data)
    }

    async function fetchHospitals(){
        const response = await fetch("http://127.0.0.1:8000/hospitals/")
        const data = await response.json()
        setHospitals(data.data)
    }

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
            
        }else{
            const data = await response.json()
            setError(data.detail)
        }}
   
    useEffect(() => {fetchProcedures(); fetchHospitals(); fetchUsers()}, [])

    async function handleSearch(event){

        event.preventDefault()
        setError("")
        // grab search criteria if inserted
        const params = new URLSearchParams()
        if (userId != null && userId !== "") {params.append("user_id", userId)}
        if (procedureId != null && procedureId !== "") {
            params.append("procedure_id", procedureId)
        } else if (specialty) {
            params.append("specialty", specialty)
        }

        if (hospitalId != null && hospitalId !== "") {
            params.append("hospital_id", hospitalId)
        } else if (location) {
            params.append("location", location)
        }

        if (fromDate !== "") params.append("start_date", fromDate)
        if (toDate !== "") params.append("end_date", toDate)

        // fetch search results
        const token = localStorage.getItem("token")
        const response = await fetch(
        `http://127.0.0.1:8000/logs?${params}`,
        {
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })

        
        if (response.ok){
            const data = await response.json()
            setSearchResults(data.data.result)
        }else{
        const data = await response.json()
        setError(data.detail)}
    }
        return (
        <>
        <div className="page-form">
            <h2>Search Logs</h2>

            <form onSubmit={handleSearch}>

            {/* User */}
            <select value={userId}
                onChange={(e) => setUserId(e.target.value)}>
                <option value="">All Users</option>
                {users.map(user => (
                    <option key={user.id} value={user.id}>
                        {user.username} {user.registration}
                    </option>
                ))}
            </select>

            {/* Location */}
            <select value={location}
                onChange={(e) => {
                    setLocation(e.target.value)
                    setHospitalId("")
                }}>
                <option value="">All Locations</option>
                {locations.map(loc => (
                    <option key={loc} value={loc}>
                        {loc}
                    </option>
                ))}
            </select>

            {/* Hospital */}
            <select value={hospitalId} disabled={!location}
                onChange={(e) => setHospitalId(e.target.value)}>
                <option value="">All Hospitals</option>
                {filteredHospitals.map(hospital => (
                    <option key={hospital.id} value={hospital.id}>
                        {hospital.name}
                    </option>
                ))}
            </select>

            {/* Specialty */}
            <select value={specialty}
                onChange={(e) => {
                    setSpecialty(e.target.value)
                    setProcedureId("")
                }}>
                <option value="">All Specialties</option>
                {specialties.map(spec => (
                    <option key={spec} value={spec}>
                        {spec}
                    </option>
                ))}
            </select>

            {/* Procedure */}
            <select value={procedureId} disabled={!specialty}
                onChange={(e) => setProcedureId(e.target.value)}>
                <option value="">All Procedures</option>

                {filteredProcedures.map(procedure => (
                    <option key={procedure.id} value={procedure.id}>
                        {procedure.name}
                    </option>
                ))}
            </select>

            {/* Date From */}
            <input type="date" value={fromDate}
                onChange={(e) => setFromDate(e.target.value)}/>

            {/* Date To */}
            <input type="date" value={toDate}
                onChange={(e) => setToDate(e.target.value)}/>

            <button className="primary-btn" type="submit">
                Search
            </button>

        </form>
    </div>
    {searchResults.length === 0 && (<p>No matching records.</p>)}

    {searchResults.length > 0 && (
        <div className="page-container">
    <table className="table-data">
        <thead>
            <tr>
                <th>User</th>
                <th>Procedure</th>
                <th>Hospital</th>
                <th>Role</th>
                <th>Date</th>
                <th>Entry Clock</th>
                
            </tr>
        </thead>

        <tbody>
            {searchResults.map(log => (
                <tr key={log.id}>
                    <td>{log.username}</td>
                    <td>{log.procedure_name}</td>
                    <td>{log.hospital_name}</td>
                    <td>{log.role}</td>
                    <td>{log.procedure_date || "-"}</td>
                    <td>{log.log_clock}</td>
                </tr>
            ))}
        </tbody>
    </table>
    </div>
)}
    </>
      )
}
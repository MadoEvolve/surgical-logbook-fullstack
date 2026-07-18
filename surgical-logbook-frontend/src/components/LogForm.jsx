import { useState, useEffect } from "react"

// LogForm for create and update
export default function LogForm({mode = "create", log= null, onSuccess}){
    // Procedure per specialty
    const [procedures, setProcedures] = useState([])
    const [procedureId, setProcedureId]= useState("")
    const [specialty, setSpecialty] = useState("")
    const filteredProcedures = procedures.filter(procedure=>procedure.specialty === specialty)

    // Hospital per location
    const [hospitals, setHospitals] = useState([])
    const [hospitalId, setHospitalId]= useState("")
    const [location, setLocation] = useState("")
    const filteredHospitals = hospitals.filter(hospital => hospital.location === location)

    // hardcoding Roleenum
    const roles = ["performed","observed","assistant","supervised","training"]
    const [role, setRole] = useState("")
    //optional fields notes and procedureDate
    const [notes, setNotes] = useState("")
    const [procedureDate, setProcedureDate] = useState("")
    // error
    const [error,setError] = useState("")
    const [message,setMessage] = useState("")

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
    // use effect 
    useEffect(() => {fetchProcedures()
        fetchHospitals()}, [])

    useEffect(() => {
    if (mode === "edit" && log) {
        // finding specialty and location in procedures and hospitals list
        
        const procedure =procedures.find(p => Number(p.id) === Number(log.procedure_id))
        const hospital =hospitals.find(h => Number(h.id) === Number(log.hospital_id))
        // crashes if empty lists (procedures,hospitals)
        // react way just go back untill it's not empty
        if (!procedure || !hospital) return
        
        setSpecialty(procedure.specialty)
        setLocation(hospital.location)

        setProcedureId(log.procedure_id)
        setHospitalId(log.hospital_id)
        setRole(log.role)
        setNotes(log.notes || "")
        setProcedureDate(log.procedure_date || "")
    }
    }, [log, mode, procedures, hospitals])

    const specialties = [... new Set(procedures.map(procedure => procedure.specialty))]
    const locations = [... new Set(hospitals.map(hospital => hospital.location))]

    async function handleSubmit(event) {
    event.preventDefault()
    const token = localStorage.getItem("token")

    const payload = {
        procedure_id: Number(procedureId),
        hospital_id: Number(hospitalId),
        role,
        notes,
        procedure_date: procedureDate || null
    }

    if (mode === "create") {
        const response = await fetch("http://127.0.0.1:8000/logs/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        })

        const data = await response.json()
        if (response.ok) {
            setMessage("Operation logged successfully")
        } else {
            setError(data.detail)
        }
    } else {
        const response = await fetch(
            `http://127.0.0.1:8000/logs/${log.id}`,
            {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(payload)
            })

        const data = await response.json()
        if (response.ok) {
        setMessage("Log updated successfully")
        onSuccess?.(data.data)
           
        }
    }}

    return(
        <div className="page-form">
            {message && <p className="success">{message}</p>}
            <h2>Add Operation</h2>
            {error && <p className="error">{error}</p>}

            <form onSubmit={handleSubmit}>
                {/* choose specialty */}
                <select value={specialty} onChange={(e) => {
                    setSpecialty(e.target.value)
                    setProcedureId("")}}>
                    <option value="">Select Specialty</option>
                    {specialties.map(spec => (
                        <option key={spec} value={spec}>
                        {spec}
                    </option>))}
                </select>
                {/* choose procedure name but send id value only if specialty selected */}
                <select disabled={!specialty} value={procedureId}
                    onChange={(e)=> setProcedureId(e.target.value)} required>
                    <option value="">Select Procedure</option>
                    {filteredProcedures.map(procedure =>
                        <option key={procedure.id} value={procedure.id}>
                            {procedure.name}
                        </option>
                    )}
                </select>
                {/* choose location */}
                <select value= {location} onChange= {(e)=>{
                    setLocation(e.target.value)
                    setHospitalId("")}}>
                        <option value="">Select Location</option>
                        {locations.map(loc =>(
                            <option key={loc} value={loc}>
                                {loc}
                            </option>))}
                </select>
                {/* choose hospital name but send id value only if location is selected */}
                <select disabled={!location} value={hospitalId}
                    onChange={(e)=> setHospitalId(e.target.value)} required>
                    <option value="">Select Hospital</option>
                    {filteredHospitals.map(hospital=>
                        <option key={hospital.id} value={hospital.id}>
                            {hospital.name}
                        </option>
                    )}
                </select>
                <select value={role} onChange={(e)=>setRole(e.target.value)} required>
                    <option value="">Role</option>
                    {roles.map(role=>
                        <option key ={role} value={role}>
                            {role}
                        </option>)}
                </select>
                <textarea value={notes} onChange={(e) => setNotes(e.target.value)}
                    placeholder="Operative notes (optional)"/>
                <input type="date" value={procedureDate}
                onChange={(e) => setProcedureDate(e.target.value)}/>
                <button className="primary-btn" type="submit">
                    {mode === "create"? "Add Record" : "Update record"}
                </button>
            </form>
        </div>
    )
}


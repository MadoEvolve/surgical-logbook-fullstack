import { useState, useEffect } from "react"

export default function HospitalForm({mode = "create", selectedHospital= null, onSuccess}){

    const [error, setError] = useState("")
    const emptyHospital = {id:null, name:"", location:""}
    const [hospital, setHospital] = useState(emptyHospital)

    function handleChange(e) {
    const { name, value } = e.target

    setHospital(prev => ({
        ...prev,
        [name]: value
    }))}

    useEffect(() => {
    if (mode === "edit" && selectedHospital) {
        setHospital(selectedHospital)
    } else {
        setHospital(emptyHospital)
    }}, [mode, selectedHospital])

    async function handleSubmit(event){
        event.preventDefault()
        const token = localStorage.getItem("token")

        const payload ={
            name: hospital.name,
            location: hospital.location
        }

        if (mode === "create") {
        const response = await fetch("http://127.0.0.1:8000/hospitals/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(payload)
        })

        const data = await response.json()
        if (response.ok) {
            onSuccess?.()
        } else {
            setError(data.detail)
        }
    } else {
        const response = await fetch(
            `http://127.0.0.1:8000/hospitals/${hospital.id}`,
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
        onSuccess?.()  
        }else {
            setError(data.detail)
        }
    }}
        


    return(
        <div className="page-form">
            {error && <p>{error}</p>}
            <form onSubmit={handleSubmit}>
                <input name="name" value={hospital.name} required
                onChange={handleChange}/>

                <input name="location" value={hospital.location} required
                onChange={handleChange}/>

                <button type="submit">
                    {mode === "create"? "Add Hospital" : "Update Hospital"}
                </button>
            </form>
        </div>
    )
}
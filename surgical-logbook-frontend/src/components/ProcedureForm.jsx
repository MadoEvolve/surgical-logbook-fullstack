import { useState, useEffect } from "react"

export default function ProcedureForm({mode = "create", selectedProcedure= null, onSuccess}){

    const [error, setError] = useState("")
    const [procedure, setProcedure] = useState({
    id: null,
    name: "",
    specialty: ""
})

    function handleChange(e) {
    const { name, value } = e.target

    setProcedure(prev => ({
        ...prev,
        [name]: value
    }))}

    useEffect(() => {
    if (mode === "edit" && selectedProcedure) {
        setProcedure(selectedProcedure)
    } else {
        setProcedure({
            id: null,
            name: "",
            specialty: ""
        })
    }}, [mode, selectedProcedure])

    async function handleSubmit(event){
        event.preventDefault()
        const token = localStorage.getItem("token")

        const payload ={
            name: procedure.name,
            specialty: procedure.specialty
        }

        if (mode === "create") {
        const response = await fetch("http://127.0.0.1:8000/procedures/", {
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
            `http://127.0.0.1:8000/procedures/${procedure.id}`,
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
                <input name="name" value={procedure.name} required
                onChange={handleChange}/>

                <input name="specialty" value={procedure.specialty} required
                onChange={handleChange}/>

                <button type="submit">
                    {mode === "create"? "Add Procedure" : "Update Procedure"}
                </button>
            </form>
        </div>
    )
}
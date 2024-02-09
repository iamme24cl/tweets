import axios from "axios";

const login = async (email, pwd) => {
    try {
        const resp = await  axios.post("http://localhost:5000/login", {email, pwd})
        localStorage.setItem("token", resp.data.token)
        return {"success": true}
    } catch (error) {
        return {"success": false, "error": error}
    }
}

export default login;
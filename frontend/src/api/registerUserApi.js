import axios from "axios";

const registerUser = async (email, username, pwd) => {
    try {
        await axios.post("http://localhost:5000/register", { email, username, pwd });
        return {"success": true}
    } catch (error) {
        console.log(error)
        return {"success": false, "error": error}
    }
}

export default registerUser;
import React, { useState } from "react";
import axios from "axios";
import Alert from "./Alert";
import registerUser from "../api/registerUserApi";

function Register() {
    const [email, setEmail] = useState('');
    const [pwd, setPwd] = useState('');
    const [username, setUsername] = useState('');
    const [err, setErr] = useState('');
    const [register, setRegister] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();
        registerUser(email, username, pwd).then((resp) => {
            console.log(resp)
            if (resp.success === true) {
                setRegister(true)
                window.location = "/login"
            } else {
                console.log(resp.error)
                setErr(resp.error.response.data.error)
            }
        })
    }     

    return (
        <div className="w3-card-4" style={{ margin: "2rem" }}>
            <div className="w3-container w3-blue w3-center w3-xlarge">
                REGISTER
            </div>
            <div className="w3-container">
                {err.length > 0 && (
                    <Alert 
                        message={`Check your inputs and try again! (${err})`}
                    />
                )}
                <form onSubmit={handleSubmit}>
                    <p>
                        <label>Email</label>
                        <input
                            type="email"
                            className="w3-input w3-border"
                            value={email}
                            onChange={e => setEmail(e.target.value)}
                        />
                    </p>
                    <p>
                        <label>Username</label>
                        <input
                            type="text"
                            className="w3-input w3-border"
                            value={username}
                            onChange={e => setUsername(e.target.value)}
                        />
                    </p>
                    <p>
                        <label>Password</label>
                        <input
                            type="text"
                            className="w3-input w3-border"
                            value={pwd}
                            onChange={e => setPwd(e.target.value)}
                        />
                    </p>
                    <p>
                        <button type="submit" className="w3-button w3-blue">
                            Register
                        </button>
                        {register && <p>You're registered!</p>}
                    </p>
                </form>
            </div>
        </div>
    );
}

export default Register;
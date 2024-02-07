import React, { useState } from "react";
import axios from "axios";
import Alert from "./Alert";

function Login() {
    const [email, setEmail] = useState('');
    const [pwd, setPwd] = useState('');
    const [err, setErr] = useState('');
    const [isLoggedIn, setIsLoggedIn] = useState(false);


    const handleSubmit = (event)  => {
        event.preventDefault();
        axios
            .post("http://localhost:5000/login", {
                email: email,
                pwd: pwd,
            })
            .then(() => {
                setIsLoggedIn(true)
                window.location = "/mainpage"
            })
            .catch((error) => {
                setErr(error.response.data.error)
            });
    };

    return (
        <div className="w3-card-4" style={{ margin: "2rem" }} onClick={() => setErr('')}>
            <div className="w3-container w3-blue w3-center w3-xlarge">
                LOGIN
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
                            Login
                        </button>
                        {isLoggedIn && <p>Successfully logged in!</p>}
                    </p>
                </form>
            </div>
        </div>
    );
}

export default Login;


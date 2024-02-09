import React from "react";
import Home from "./Home";
import MainPage from "./MainPage";
import Navbar from "./Navbar";
import Login from "./Login";
import Register from "./Register";
import { verifyToken } from "../helper/helper";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

function App() {

    return (
        <React.Fragment>
            <Navbar />
            <Router>
                <Routes>
                    <Route path="/" exact element={verifyToken() ? <MainPage /> : <Home />} />
                    <Route path="/login" exact element={<Login />} />
                    <Route path="/register" exact element={<Register />} />
                </Routes>
            </Router>
        </React.Fragment>
    );
}

export default App;


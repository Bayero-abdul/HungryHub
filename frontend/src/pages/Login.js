import React from 'react';
import { useRef, useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { FontcAwesomeIcon } from "@fortawesome/react-fontawesome";
import { useAuth } from '../hooks/useAuth';

// import axios from './api/axios';
// const REGISTER_URL = '/api/v1/users';

const Login = () => {
    const { setAuth } = useAuth();

    const navigate = useNavigate();
    const location = useLocation();
    const from = location.state?.from?.pathname || "/";

    const emailRef = useRef();
    const errRef = useRef();

    const [email, setEmail] = useState('');
    const [pwd, setPwd] = useState('');
    const [errMsg, setErrMsg] = useState('');

    useEffect(() => {
        emailRef.current.focus();
    }, [])

    useEffect(() => {
        setErrMsg('');
    }, [email, pwd])

    const handleSubmit = async (e) => {
        e.preventDefault();
 
        try {
            let headers = new Headers();
            headers.append('Content-Type', 'application/json');
            headers.append('Accept', 'application/json');
            headers.append('Origin','http://localhost:5001');
    
            const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
                method: 'POST',
                headers: headers,
                body: JSON.stringify({ email: email, password: pwd })
            });

            if (response.status === 200) {
                const data = await response.json();
                console.log(data);
                sessionStorage.setItem("Token", data.access_token);
                const access_token = sessionStorage.getItem("Token");
    
                setAuth({ user: email, pwd, access_token});
                setEmail('');
                setPwd('');
                navigate(from, { replace: true});
            }

            if (response.status === 401) {
                setErrMsg('Unauthorized');
            } else if (err.response?.status === 400) {
                setErrMsg('Invalid Email or Password');
            }
            errRef.current?.focus();
        } catch (err) {
            setErrMsg('No Server Response');
            errRef.current?.focus();
        }
    }

    return (
        <section>
            <p ref={errRef} className={errMsg ? "errmsg" : "offscreen"} aria-live="assertive">{errMsg}</p>
            <h3>Login</h3>
            <form onSubmit={handleSubmit}>
                <label htmlFor="email">
                    Email:
                </label>
                <input
                    type="email"
                    id="email"
                    ref={emailRef} // Assuming you have an emailRef for focusing
                    autoComplete="off"
                    onChange={(e) => setEmail(e.target.value)}
                    value={email}
                    required
                />

                <label htmlFor="password">
                    Password:
                </label>
                <input
                    type="password"
                    id="password"
                    onChange={(e) => setPwd(e.target.value)}
                    value={pwd}
                    required
                />

                <button>Login</button>
            </form>
            <p>
                Not registered yet?<br />
                <span className="line">
                <Link to="/register">Sign Up</Link>
                </span>
            </p>
        </section>         
    )
}

export default Login;
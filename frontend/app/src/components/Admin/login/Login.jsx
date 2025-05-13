import React from 'react';
import './Login.css';

const Login = () => {
    return (
        <div className="login-wrapper">
            <div className="login-card">
            {/* <h2 className='text-white'>Admin Panel</h2> */}
                <div className="login-body">
                    <div className="login-logo-wrapper">
                        <img src="/login.png" alt="Login" className="login-logo" />
                    </div>
                    {/* <h2 className="login-heading">Sign in to your account</h2> */}
                    <form className='my-3'>
                        <div className="form-group">
                            <input type="email" className="form-control" placeholder="Email" required />
                        </div>
                        <div className="form-group">
                            <input type="password" className="form-control" placeholder="Password" required />
                        </div>
                        <div className="text-center">
                            <button type="submit" className="login-button w-50">Log in</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;

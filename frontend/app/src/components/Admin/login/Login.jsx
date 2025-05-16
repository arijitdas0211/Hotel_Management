import { useState } from 'react';
import './Login.css';
import { useNavigate } from 'react-router-dom';


const Login = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    // const [users, setUsers] = useState([]);


    const handleLogin = async (e) => {
        e.preventDefault();

        const user = {
            username, password
        };

        try {
            const response = await fetch("http://localhost:8000/api/admin/login/", {
                method: "POST",
                credentials: "include",
                headers: {
                    'Content-type': 'application/json',
                },
                body: JSON.stringify(user),
            });

            if (response.ok) {
                navigate('/admin/dashboard');
                console.log("Login Successful.");
            } else {
                console.log("Error in login.")
            }

            setUsername('');
            setPassword('');

        } catch (err) {
            console.log(err);
        }
    };


    // useEffect(() => {
    //     fetchUsers();
    // }, [])

    // const fetchUsers = async () => {
    //     try {
    //         const response = await fetch("http://127.0.0.1:8000/api/admin/login/");
    //         const data = await response.json();
    //         setUsers(data);
    //     } catch (error) {
    //         console.log(error);
    //     }
    // }

    return (
        <div className="login-wrapper">
            <div className="login-card">
                {/* <h2 className='text-white'>Admin Panel</h2> */}
                <div className="login-body">
                    <div className="login-logo-wrapper">
                        <img src="/admin_staff.png" alt="Login" className="login-logo" />
                    </div>
                    <h2 className="login-heading text-black fs-4">Admin or Staff Login</h2>
                    <hr />
                    <form className='mt-3 mb-2'>
                        <h2 className="login-heading fs-6 text-danger fw-normal">*You can use username or email or phone as username*</h2>
                        <div className="form-floating mb-3">
                            <input type="text" className="form-control" value={username} onChange={(e) => setUsername(e.target.value)} id="floatingInput" placeholder="" />
                            <label htmlFor="floatingInput">Username</label>
                        </div>
                        <div className="form-floating">
                            <input type="password" className="form-control" value={password} onChange={(e) => setPassword(e.target.value)} id="floatingPassword" placeholder="" />
                            <label htmlFor="floatingPassword">Password</label>
                        </div>
                        <div className="mt-4">
                            <button type="submit" onClick={handleLogin} className="login-button me-auto">
                                LOGIN <i className="fa-solid fa-arrow-right-to-bracket" />
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    );
};

export default Login;

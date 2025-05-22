import { useNavigate } from "react-router-dom";

const Login = () => {
    const navigate = useNavigate();
    const userLogin = (e)=> {
        e.preventDefault();
        navigate('/admin/dashboard');
    }

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
                            <input type="text" className="form-control form_control" value="" onChange="" id="floatingInput" placeholder="" />
                            <label htmlFor="floatingInput">Username</label>
                        </div>
                        <div className="form-floating">
                            <input type="password" className="form-control form_control" value="" onChange="" id="floatingPassword" placeholder="" />
                            <label htmlFor="floatingPassword">Password</label>
                        </div>
                        <div className="mt-4">
                            <button type="submit" onClick={userLogin} className="login-button me-auto">
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

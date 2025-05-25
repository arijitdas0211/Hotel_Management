import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Swal from "sweetalert2";
import api from "../../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../../constants";

const Login = () => {
  useEffect(() => {
    localStorage.clear();
  }, []);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  //   const [error, setError] = useState("");

  const navigate = useNavigate();
  const userLogin = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      const errorMsg = "<h3>Authentication Failed!</h3>";
      await Swal.fire({
        icon: "error",
        title: errorMsg,
        text: "Username and Password are required to Login.",
        showConfirmButton: true,
        confirmButtonText: "OK",
        confirmButtonColor: "crimson",
      });
      return;
    }

    try {
      const response = await api.post(
        "http://127.0.0.1:8000/api/admin/login/",
        {
          username: username,
          password: password,
        }
      );

      if (response.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, response.data.access);
        localStorage.setItem(REFRESH_TOKEN, response.data.refresh);
        console.log("Login successful.");
        navigate("/admin/dashboard");
      }
    } catch (error) {
      let errorMessage = "Login failed. Please try again!";

      // Check if it's an AxiosError and has a response
      if (error.response) {
        const data = error.response.data;

        if (typeof data === "string") {
          errorMessage = data;
        } else if (data.detail) {
          errorMessage = data.detail;
        } else {
          // Handle field errors
          const messages = [];
          for (const key in data) {
            if (Array.isArray(data[key])) {
              messages.push(`${key.toUpperCase()}: ${data[key].join(" ")}`);
            } else {
              messages.push(`${key.toUpperCase()}: ${data[key]}`);
            }
          }
          errorMessage = messages.join("\n");
        }
      } else if (error.request) {
        // Request made but no response received
        errorMessage = "No response from server. Please check your connection.";
      } else {
        // Something else happened
        errorMessage = "Unexpected error: " + error.message;
      }

      //   setError(errorMessage);

      await Swal.fire({
        icon: "error",
        title: "Login Error",
        text: errorMessage,
        showConfirmButton: true,
        confirmButtonText: "OK",
        confirmButtonColor: "crimson",
      });
    }
  };

  return (
    <div className="login-wrapper">
      <div className="login-card">
        {/* <h2 className='text-white'>Admin Panel</h2> */}
        <div className="login-body">
          <div className="login-logo-wrapper">
            <img src="/admin_staff.png" alt="Login" className="login-logo" />
          </div>
          <h2 className="login-heading text-black fs-4">
            Admin or Staff Login
          </h2>
          <hr />
          <form className="mt-3 mb-2">
            <h2 className="login-heading fs-6 text-danger fw-normal">
              *You can use username or email or phone as username*
            </h2>
            <div className="form-floating mb-3">
              <input
                type="text"
                className="form-control form_control"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                id="floatingInput"
                placeholder=""
              />
              <label htmlFor="floatingInput">Username</label>
            </div>
            <div className="form-floating">
              <input
                type="password"
                className="form-control form_control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                id="floatingPassword"
                placeholder=""
              />
              <label htmlFor="floatingPassword">Password</label>
            </div>
            <div className="mt-4">
              <button
                type="submit"
                onClick={userLogin}
                className="login-button me-auto"
              >
                LOGIN <i className="fa-solid fa-arrow-right-to-bracket" />
              </button>
            </div>
          </form>
          {/* <div className="error my-3">
                        {error && <p className="text-danger">{error}</p>}
                    </div> */}
        </div>
      </div>
    </div>
  );
};

export default Login;

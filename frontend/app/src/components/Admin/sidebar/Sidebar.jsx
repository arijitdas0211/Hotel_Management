import { useState } from "react";
import "./Sidebar.css";
import { Link, useNavigate } from "react-router-dom";
import Dashboard from "../dashboard_cards/Card";


export default function Sidebar() {
    const navigate = useNavigate();
    const [isCollapsed, setIsCollapsed] = useState(() => window.innerWidth <= 992);

    const toggleSidebar = () => {
        setIsCollapsed(!isCollapsed);
    }

    const handleLogout = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch("http://localhost:8000/api/admin/logout/", {
                method: 'POST',
                credentials: "include",
            });

            if (response.ok) {
                console.log("User logged out.");
                navigate("/admin/login");
            } else {
                console.log("Logout failed: ", response.status);
            }
        } catch (error) {
            console.log(error);
        }
    };


    return (
        <>
            <div className="container-fluid">
                <div className={`sidebar shadow ${isCollapsed ? 'collapsed' : ''}`}>
                    <div className="sidebar_header m-auto text-center pt-4 pb-2">
                        <h1 className={`sidebar_title fs-4 ${isCollapsed ? 'collapsed' : ''}`}>
                            Hello! Superuser
                        </h1>
                    </div>
                    <hr />
                    <div className="sidebar_body">
                        <ul className="sidebar_menu">
                            <li className="sidebar_item active">
                                <Link to="/admin/dashboard" className="sidebar_link">
                                    <i className="fa-solid fa-chart-line" /> &nbsp;
                                    <span>Dashboard</span>
                                </Link>
                            </li>
                            <li className="sidebar_item">
                                <a href="#menu2" className="sidebar_link">
                                    <i className="fa-solid fa-users-between-lines" /> &nbsp;
                                    <span>Staff Type</span>
                                </a>
                            </li>
                            <li className="sidebar_item">
                                <a href="#menu3" className="sidebar_link">
                                    <i className="fa-solid fa-users" /> &nbsp;
                                    <span>Staff</span>
                                </a>
                            </li>
                            <li className="sidebar_item">
                                <a href="#menu4" className="sidebar_link">
                                    <i className="fa-brands fa-uncharted" /> &nbsp;
                                    <span>Table</span>
                                </a>
                            </li>
                            <li className="sidebar_item">
                                <a href="#menu5" className="sidebar_link">
                                    <i className="fa-solid fa-list" /> &nbsp;
                                    <span>Menu Category</span>
                                </a>
                            </li>
                            <li className="sidebar_item">
                                <a href="#menu5" className="sidebar_link">
                                    <i className="fa-solid fa-utensils" /> &nbsp;
                                    <span>Menu</span>
                                </a>
                            </li>
                            <li className="sidebar_item">
                                <a href="#menu5" className="sidebar_link">
                                    <i className="fa-solid fa-file-invoice" /> &nbsp;
                                    <span>Billing</span>
                                </a>
                            </li>
                            <li className="sidebar_item">
                                <a href="#menu5" className="sidebar_link">
                                    <i className="fa-regular fa-comments" /> &nbsp;
                                    <span>User Feedbacks</span>
                                </a>
                            </li>
                            <li className="sidebar_item">
                                <Link onClick={handleLogout} className="sidebar_link">
                                    <i className="fa-solid fa-arrow-right-from-bracket" /> &nbsp;
                                    <span>Logout</span>
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>

                <div className="main_container">
                    <div className="toggleDiv">
                        <button className="btn btn-primary toggleBtn" onClick={toggleSidebar}>
                            <i className="fa-solid fa-bars" />
                        </button>
                    </div>

                    <div className="row">
                        <div className="main_title bg-white shadow-sm p-3 w-100 col-12 col-lg-12 col-md-12 col-sm-12">
                            <h2 className="fw-normal">Dashboard</h2>
                            <nav aria-label="breadcrumb">
                                <ol className="breadcrumb">
                                    <li className="breadcrumb-item"><a className="text_primary" href="#home">Home</a></li>
                                    <li className="breadcrumb-item active" aria-current="page">Dashboard</li>
                                </ol>
                            </nav>
                        </div>
                        <Dashboard />
                        <div className="main_footer col-12 col-lg-12 col-md-12 col-sm-12 shadow position-absolute bottom-0 p-2 text-white w-100 m-0">
                            <div className="footer_text text-center">
                                &copy; {new Date().getFullYear()} Hotel Management Application | Admin Panel
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}

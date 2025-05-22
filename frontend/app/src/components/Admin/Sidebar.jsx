import { useState } from "react";
import { Link, useLocation } from "react-router-dom";

export default function Sidebar() {
  // const [activeLink, setActiveLink] = useState();
  const location = useLocation();

  const menuItems = [
    { label: "Dashboard", icon: "fa-chart-line", path: "/admin/dashboard" },
    { label: "Staff Type", icon: "fa-users-between-lines", path: "/admin/staff-type" },
    { label: "Staff", icon: "fa-users", path: "/admin/staff" },
    { label: "Table", icon: "fa-brands fa-uncharted", path: "/admin/table" },
    { label: "Menu Category", icon: "fa-list", path: "/admin/menu-category" },
    { label: "Menu", icon: "fa-utensils", path: "/admin/menu" },
    { label: "Booking", icon: "fa-calendar-days", path: "/admin/bookings" },
    { label: "Order", icon: "fa-clipboard", path: "/admin/orders" },
    { label: "Billing", icon: "fa-file-invoice", path: "/admin/billing" },
    { label: "User Feedbacks", icon: "fa-comments", path: "/admin/userfeedback" },
    { label: "Logout", icon: "fa-arrow-right-from-bracket", path: "/admin/login" },
  ];

  const [isCollapsed, setIsCollapsed] = useState(
    () => window.innerWidth <= 992
  );

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };
  
  return (
    <>
      <div className={`sidebar shadow ${isCollapsed ? "collapsed" : ""}`}>
        <div className="sidebar_header m-auto text-center pt-4 pb-4">
          <h1 className={`sidebar_title text-white fs-2 ${isCollapsed ? "collapsed" : ""}`} style={{ fontFamily: '"Poetsen One", sans-serif' }}>
            Hola!
          </h1>
        </div>
        <hr className="mt-0" />
        <div className="sidebar_body">
          <ul className="sidebar_menu">
            {menuItems.map((item, index) => (
              
              <li key={index} className={`sidebar_item ${location.pathname === item.path ? 'active' : ''}`}>
                <Link to={item.path} className="sidebar_link">
                  <i className={`fa-solid ${item.icon}`} /> &nbsp;
                  <span>{item.label}</span>
                </Link>
              </li>
            
            ))}
          </ul>
        </div>
      </div>

      <div className="main_container pb-0">
        <div className="toggleDiv position-fixed">
          <button className="btn btn-primary toggleBtn shadow" onClick={toggleSidebar}>
            <i className="fa-solid fa-bars" />
          </button>
        </div>

        {/* <div className="row px-3">
          <div className="bg-white shadow-sm py-3 px-5 w-100 col-12 col-lg-12 col-md-12 col-sm-12">
            <h2 className="fw-normal">Dashboard</h2>
            <nav aria-label="breadcrumb">
              <ol className="breadcrumb">
                <li className="breadcrumb-item">
                  <Link className="text_primary" to="/admin/dashboard">
                    Home
                  </Link>
                </li>
                <li className="breadcrumb-item active" aria-current="page">
                  Dashboard
                </li>
              </ol>
            </nav>
          </div>
        </div> */}
      </div>
    </>
  );
}

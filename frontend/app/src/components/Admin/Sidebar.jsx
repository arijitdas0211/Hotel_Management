import { useState } from "react";
import { Link } from "react-router-dom";

export default function Sidebar() {
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
            <li className={`sidebar_item active`}>
              <Link to="/admin/dashboard" className="sidebar_link">
                <i className="fa-solid fa-chart-line" /> &nbsp;
                <span>Dashboard</span>
              </Link>
            </li>
            <li className={`sidebar_item`}>
              <Link to="/admin/staff-type" className="sidebar_link">
                <i className="fa-solid fa-users-between-lines" /> &nbsp;
                <span>Staff Type</span>
              </Link>
            </li>
            <li className={`sidebar_item`}>
              <Link to="/admin/staff" className="sidebar_link">
                <i className="fa-solid fa-users" /> &nbsp;
                <span>Staff</span>
              </Link>
            </li>
            <li className={`sidebar_item`}>
              <Link to="/admin/table" className="sidebar_link">
                <i className="fa-brands fa-uncharted" /> &nbsp;
                <span>Table</span>
              </Link>
            </li>
            <li className={`sidebar_item`}>
              <Link to="/admin/menu-category" className="sidebar_link">
                <i className="fa-solid fa-list" /> &nbsp;
                <span>Menu Category</span>
              </Link>
            </li>
            <li className={`sidebar_item`}>
              <Link to="/admin/menu" className="sidebar_link">
                <i className="fa-solid fa-utensils" /> &nbsp;
                <span>Menu</span>
              </Link>
            </li>
            <li className={`sidebar_item`}>
              <Link to="/admin/billing" className="sidebar_link">
                <i className="fa-solid fa-file-invoice" /> &nbsp;
                <span>Billing</span>
              </Link>
            </li>
            <li className={`sidebar_item`}>
              <Link to="/admin/userfeedback" className="sidebar_link">
                <i className="fa-regular fa-comments" /> &nbsp;
                <span>User Feedbacks</span>
              </Link>
            </li>
            <li className={`sidebar_item`}>
              <Link to="/admin/login" className="sidebar_link">
                <i className="fa-solid fa-arrow-right-from-bracket" /> &nbsp;
                <span>Logout</span>
              </Link>
            </li>
          </ul>
        </div>
      </div>

      <div className="main_container pb-0">
        <div className="toggleDiv position-fixed">
          <button className="btn btn-primary toggleBtn" onClick={toggleSidebar}>
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

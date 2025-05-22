import "./Admin.css";
import Sidebar from "../../components/Admin/Sidebar";
import Footer from "../../components/Admin/Footer";
import { Outlet } from "react-router-dom";

export default function Admin() {
  return (
    <>
      <Sidebar />
        <main className="main_container" style={{ paddingTop: 0, paddingBottom: 0 }}>
          <Outlet />
        </main>
      <Footer />
    </>
  );
}

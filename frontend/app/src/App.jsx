// src/App.jsx
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Admin from "./pages/Admin/Admin";
import Home from "./pages/Users/Home";
import Login from "./components/Admin/Login";
import Dashboard from "./components/Admin/Dashboard";
import StaffTypeForm from "./components/Admin/StaffTypeForm";
import Staff from "./components/Admin/Staff";
import Table from "./components/Admin/Table";
import MenuCategory from "./components/Admin/MenuCategory";
import Menu from "./components/Admin/Menu";
import Bookings from "./components/Admin/Bookings";
import Orders from "./components/Admin/Orders";
import Billing from "./components/Admin/Billing";
import Userfeedback from "./components/Admin/Userfeedback";

function App() {
  
  return (
    <BrowserRouter>
      <Routes>
        {/* User routes */}
        <Route index path="/" element={<Home />} />

        {/* User routes */}
        {/* Admin login */}
        <Route path="/admin/login" element={<Login />} />
        <Route path="/admin" element={<Admin />}>
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="staff-type" element={<StaffTypeForm />} />
          <Route path="staff" element={<Staff />} />
          <Route path="table" element={<Table />} />
          <Route path="menu-category" element={<MenuCategory />} />
          <Route path="menu" element={<Menu />} />
          <Route path="bookings" element={<Bookings />} />
          <Route path="orders" element={<Orders />} />
          <Route path="billing" element={<Billing />} />
          <Route path="userfeedback" element={<Userfeedback />} />
        </Route>
        {/* Admin login */}
      </Routes>
    </BrowserRouter>
  );
}

export default App;

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
import ProtectedRoute from "./components/Admin/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* User routes */}
        <Route index path="/" element={<Home />} />

        {/* User routes */}
        {/* Admin login */}
        <Route path="/admin/login" element={<Login />} />
        {/* Admin login */}
        
        <Route path="/admin" element={<Admin />}>
          <Route path="dashboard" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="staff-type" element={<ProtectedRoute><StaffTypeForm /></ProtectedRoute>} />
          <Route path="staff" element={<ProtectedRoute><Staff /></ProtectedRoute>} />
          <Route path="table" element={<Table />} />
          <Route path="menu-category" element={<MenuCategory />} />
          <Route path="menu" element={<Menu />} />
          <Route path="bookings" element={<Bookings />} />
          <Route path="orders" element={<Orders />} />
          <Route path="billing" element={<Billing />} />
          <Route path="userfeedback" element={<Userfeedback />} />
        </Route>
        
      </Routes>
    </BrowserRouter>
  );
}

export default App;

import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Admin from './pages/Admin/Admin';
import Home from './pages/Users/Home';
import Login from './components/Admin/login/Login';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route index path='/' element={<Home />}></Route>
          <Route index path='/admin/dashboard' element={<Admin />}></Route>
          <Route index path='/admin/login' element={<Login />}></Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App

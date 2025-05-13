import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Sidebar from './components/admin/sidebar/Sidebar';

function App() {
  return (
    <>
      <BrowserRouter>
        <Routes>
          <Route index path='/' element={<Sidebar />}></Route>
          <Route index path='/admin' element={<Sidebar />}></Route>
        </Routes>
      </BrowserRouter>
    </>
  )
}

export default App

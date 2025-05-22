import Loader from "./Loader";
import DataTable from "datatables.net-react";
import DT from "datatables.net-bs5";
import "datatables.net-select-dt";
import "datatables.net-responsive-dt";
import { useState } from "react";
import MultiSelectDropdown from "./MultiSelectDropdown";

export default function Orders() {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const selectOptions = ['Paneer Kabab', 'Pulao', 'Paneer 65', 'Navratna Korma'];

  DataTable.use(DT);

  const options = {
    paging: true,
    responsive: true,
  };

  const datetime = new Date();

  // <Loader />

  return (
    <>
      <div className="action_container bg-white shadow-sm">
        <div
          className="card border-0 p-3"
          style={{ borderRadius: 0, cursor: "default" }}
        >
          <div className="card-header p-3">
            <h4 className="card-title">Manage Orders</h4>
          </div>
          <div className="card-body container">
            <form className="row align-items-center">
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">
                  Select items *
                </label>
                <MultiSelectDropdown
                    options={selectOptions}
                    selectedOptions={selectedOptions}
                    setSelectedOptions={setSelectedOptions}
                    placeholder="Choose menu"
                  />
              </div>
              
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">Select Booking *</label>
                <select className="form-select">
                  <option value="bookID (Customer_name)">bookID (Customer_name)</option>
                </select>
              </div>

              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">Status *</label>
                <select className="form-select">
                  <option value="progress">Progress</option>
                  <option value="completed">Completed</option>
                </select>
              </div>

              <div className="col-12 text-center mt-3">
                <button
                  type="submit"
                  className="myBtn btn btn-primary bg_primary text-white shadow-sm"
                >
                  Save Order
                </button>
              </div>
            </form>
          </div>
          <hr />
          <div className="card-body container mb-3">
            <DataTable className="table table-striped" options={options}>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Menu Name</th>
                  <th>Price(₹)</th>
                  <th>Type</th>
                  <th>Category</th>
                  <th>Status</th>
                  <th>Created by</th>
                  <th>Created at</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="fw-medium">1</td>
                  <td>Paneer Masala</td>
                  <td>260</td>
                  
                  <td>
                    <span className="badge text-bg-success">Veg</span>
                  </td>
                  <td>Indian Main Course</td>
                  <td>
                    <span className="badge text-bg-success">Active</span>
                  </td>
                  <td>Arijit</td>
                  <td>
                    {datetime.getDate()}-{datetime.getMonth()}-
                    {datetime.getFullYear()} | {datetime.getHours()}:
                    {datetime.getMinutes()}:{datetime.getSeconds()}
                  </td>
                  <td>
                    <button className="btn btn-primary bg_primary btn-sm">
                      <i className="fa-regular fa-pen-to-square" />
                    </button>
                    &nbsp; &nbsp;
                    <button className="btn btn-danger bg_danger btn-sm">
                      <i className="fa-regular fa-trash-can" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </DataTable>
          </div>
        </div>
      </div>
    </>
  );
}

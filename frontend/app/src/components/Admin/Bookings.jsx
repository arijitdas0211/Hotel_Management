import Loader from "./Loader";
import DataTable from "datatables.net-react";
import DT from "datatables.net-bs5";
import "datatables.net-select-dt";
import "datatables.net-responsive-dt";

export default function Bookings() {
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
            <h4 className="card-title">Manage Bookings</h4>
          </div>
          <div className="card-body container">
            <form className="row align-items-center">
              <div className="col-12 col-md-3 col-lg-3 mb-3">
                <label htmlFor="bookDate" className="form-label fw-medium">
                  Booking Date *
                </label>
                <input
                  type="date"
                  className="form-control"
                  id="bookDate"
                  placeholder="i.e. Paneer Masala"
                />
              </div>
              <div className="col-12 col-md-3 col-lg-3 mb-3">
                <label htmlFor="bookTime" className="form-label fw-medium">
                  Booking Time *
                </label>
                <input
                  type="time"
                  className="form-control"
                  id="bookTime"
                  placeholder="i.e. Paneer Masala"
                />
              </div>
              <div className="col-12 col-md-2 col-lg-2 mb-3">
                <label htmlFor="totalPeople" className="form-label fw-medium">
                  Total People *
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="totalPeople"
                  placeholder="i.e. 5"
                />
              </div>              
              <div className="col-12 col-md-2 col-lg-2 mb-3">
                <label className="form-label fw-medium">Table *</label>
                <select className="form-select">
                  <option>-- Select table --</option>
                  <option value="101">101 - 4 person</option>
                  <option value="102">102 - 3 person</option>
                  <option value="103">103 - 8 person</option>
                  <option value="104">104 - 2 person</option>
                  <option value="105">105 - 6 person</option>
                </select>
              </div>
              <div className="col-12 col-md-2 col-lg-2 mb-3">
                <label className="form-label fw-medium">Food type *</label>
                <select className="form-select">
                  <option>-- Food type --</option>
                  <option defaultValue="veg">Veg</option>
                  <option value="nonveg">Non-veg</option>
                  <option value="both">Both</option>
                </select>
              </div>

              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label htmlFor="customerName" className="form-label fw-medium">
                  Customer Name *
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="customerName"
                  placeholder="i.e. John Doe"
                />
              </div>

              <div className="col-12 col-md-2 col-lg-2 mb-3">
                <label className="form-label fw-medium">Assigned to *</label>
                <select className="form-select">
                  <option>-- Select Staff --</option>
                  <option value="Adhir">Adhir</option>
                  <option value="Sameer">Sameer</option>
                </select>
              </div>
              
              <div className="col-12 col-md-2 col-lg-2 mb-3">
                <label className="form-label fw-medium">Status</label>
                <select className="form-select">
                  <option defaultValue="Confirmed">Confirmed</option>
                  <option defaultValue="completed">Completed</option>
                  <option defaultValue="progress">In-Progress</option>
                  <option defaultValue="cancelled">Cancelled</option>
                </select>
              </div>
              <div className="col-12 text-center mt-3">
                <button
                  type="submit"
                  className="myBtn btn btn-primary bg_primary text-white shadow-sm"
                >
                  Create Booking
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
                  <th>Customer Name</th>
                  <th>Booking Date</th>
                  <th>Booking Time</th>
                  <th>Total People</th>
                  <th>Table</th>
                  <th>Food type</th>
                  <th>Assigned to</th>
                  <th>Status</th>
                  <th>Created by</th>
                  <th>Created at</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="fw-medium">1</td>
                  <td>Sarbani</td>
                  <td>
                    {datetime.getDate()}-{datetime.getMonth()}-
                    {datetime.getFullYear()}
                  </td>
                  <td>
                    {datetime.getHours()}:
                    {datetime.getMinutes()}:{datetime.getSeconds()}
                  </td>
                  <td>6</td>
                  <td>105</td>
                  <td>
                    <span className="badge text-bg-success">Veg</span>
                  </td>
                  <td>Rishav</td>
                  <td>
                    <span className="badge text-bg-success">Active</span>
                  </td>
                  <td>
                    <span className="badge text-bg-info">Customer</span>
                  </td>
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

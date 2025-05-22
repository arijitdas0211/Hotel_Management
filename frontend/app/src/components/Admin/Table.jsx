import DataTable from "datatables.net-react";
import DT from "datatables.net-bs5";
import "datatables.net-select-dt";
import "datatables.net-responsive-dt";
import Loader from "./Loader";

export default function Table() {
  DataTable.use(DT);
  const options = {
    paging: true,
    responsive: true,
  };
  
  return (
    <>
      {/* <Loader /> */}
      <div className="action_container bg-white shadow-sm">
        <div
          className="card border-0 p-3"
          style={{ borderRadius: 0, cursor: "default" }}
        >
          <div className="card-header p-3">
            <h4 className="card-title">Manage Table</h4>
          </div>
          <div className="card-body container">
            <form className="row align-items-center">
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label htmlFor="tableNumber" className="form-label fw-medium">
                  Table Number *
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="tableNumber"
                  placeholder="i.e. 101"
                />
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label htmlFor="capacity" className="form-label fw-medium">
                  Capacity (Number of people) *
                </label>
                <input
                  type="email"
                  className="form-control"
                  id="capacity"
                  placeholder="i.e. 5"
                />
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">
                  Table status *
                </label>
                <select className="form-select" aria-label="Table status">
                  <option>-- Select table status --</option>
                  <option defaultValue="free">Free</option>
                  <option value="reserved">Reserved</option>
                </select>
              </div>
              <div className="col-12 text-center">
                <button
                  type="submit"
                  className="myBtn btn btn-primary bg_primary text-white shadow-sm"
                >
                  Add table
                </button>
              </div>
            </form>
          </div>
          <hr />
          <div className="card-body container mb-3">
            {/* {loading ? (
              <div className="container my-4">
                <Watch
                  visible={loading}
                  height="80"
                  width="80"
                  radius="48"
                  color="#4fa94d"
                  ariaLabel="watch-loading"
                />
              </div>
            ) : ( */}
              <DataTable className="table table-striped" options={options}>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Table Number</th>
                    <th>Capacity</th>
                    <th>Status</th>
                    <th>Created by</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="fw-medium">1</td>
                    <td>101</td>
                    <td>5 people</td>
                    <td>Free</td>
                    <td>Arijit</td>
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
            {/* )} */}
          </div>
        </div>
      </div>
    </>
  );
}

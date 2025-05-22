import DataTable from 'datatables.net-react';
import DT from 'datatables.net-bs5';
import 'datatables.net-select-dt';
import 'datatables.net-responsive-dt';
import Loader from './Loader';


export default function MenuCategory() {
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
            <h4 className="card-title">Manage Menu Category</h4>
          </div>
          <div className="card-body container">
            <form className="row align-items-center">
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label htmlFor="categoryName" className="form-label fw-medium">
                  Menu Category Name *
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="categoryName"
                  placeholder="i.e. Starter Indian"
                />
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">
                  Food type *
                </label>
                <select className="form-select" aria-label="Table status">
                  <option>-- Select food type --</option>
                  <option defaultValue="veg">Veg</option>
                  <option value="nonveg">Non-veg</option>
                  <option value="both">Both</option>
                </select>
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">
                  Status
                </label>
                <select className="form-select" aria-label="Table status">
                  <option defaultValue="True">Enabled</option>
                  <option value="False">Disabled</option>
                </select>
              </div>
              <div className="col-12 text-center mt-3">
                <button
                  type="submit"
                  className="myBtn btn btn-primary bg_primary text-white shadow-sm"
                >
                  Add menu category
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
                    <th>Category Name</th>
                    <th>Food type</th>
                    <th>Status</th>
                    <th>Created at</th>
                    <th>Created by</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td className="fw-medium">1</td>
                    <td>Starter Indian</td>
                    <td>Both</td>
                    <td>
                      <span className="badge text-bg-success">Active</span>
                    </td>
                    <td>Arijit</td>
                    <td>{datetime.getDate()}-{datetime.getMonth()}-{datetime.getFullYear()} | {datetime.getHours()}:{datetime.getMinutes()}:{datetime.getSeconds()}</td>
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
                  <tr>
                    <td className="fw-medium">2</td>
                    <td>Italian</td>
                    <td>Veg</td>
                    <td>
                      <span className="badge text-bg-danger">In-active</span>
                    </td>
                    <td>Arohi</td>
                    <td>{datetime.getDate()}-{datetime.getMonth()}-{datetime.getFullYear()} | {datetime.getHours()}:{datetime.getMinutes()}:{datetime.getSeconds()}</td>
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
  )
}

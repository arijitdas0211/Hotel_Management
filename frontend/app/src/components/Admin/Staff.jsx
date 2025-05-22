import DataTable from 'datatables.net-react';
import DT from 'datatables.net-bs5';
import 'datatables.net-select-dt';
import 'datatables.net-responsive-dt';
import Loader from './Loader';


export default function Staff() {
  DataTable.use(DT);
  const options = {
    paging: true,
    responsive: true,
  }
  return (
    <>
      {/* <Loader /> */}
      <div className="action_container bg-white shadow-sm">
        <div className="card border-0 p-3" style={{ borderRadius: 0, cursor: "default" }}>
          <div className="card-header p-3">
            <h4 className="card-title">Manage Staff</h4>
          </div>
          <div className="card-body container">
            <form className="row align-items-center">
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label htmlFor="staffName" className="form-label fw-medium">Full Name *</label>
                <input type="text" className="form-control" id="staffName" placeholder="i.e. John Doe" />
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label htmlFor="staffEmail" className="form-label fw-medium">Email id (Optional)</label>
                <input type="email" className="form-control" id="staffEmail" placeholder="i.e. john@gmail.com" />
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label htmlFor="staffContact" className="form-label fw-medium">Contact No. *</label>
                <input type="text" className="form-control" id="staffContact" placeholder="i.e. 9876543201" />
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">Staff type *</label>
                <select className="form-select" aria-label="Select staff type">
                  <option defaultValue={true}>-- Select staff type --</option>
                  <option value="Manager">Manager</option>
                  <option value="Chef">Chef</option>
                  <option value="Waiter">Waiter</option>
                </select>
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">Access Privilege *</label>
                <select className="form-select" aria-label="Select staff type">
                  <option defaultValue={true}>-- Select privilege --</option>
                  <option value="superuser">Superuser</option>
                  <option value="staff">Staff</option>
                </select>
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label htmlFor="staffPass" className="form-label fw-medium">Password *</label>
                <input type="password" className="form-control" id="staffPass" placeholder="Password" />
              </div>
              <div className="col-12 text-center">
                <button type="submit" className="myBtn btn btn-primary bg_primary text-white shadow-sm">Add Staff</button>
              </div>
            </form>
          </div>
          <hr />
          <div className="card-body container mb-3">
            <DataTable className="table table-striped" options={options}>
              <thead>
                  <tr>
                      <th>#</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Contact No</th>
                      <th>Staff type</th>
                      <th>Access Privilege</th>
                      <th>Created by</th>
                      <th>Actions</th>
                  </tr>
              </thead>
              <tbody>
                  <tr>
                      <td className='fw-medium'>1</td>
                      <td>Ritika</td>
                      <td>None</td>
                      <td>9876540123</td>
                      <td>Chef</td>
                      <td>
                        <span className="badge text-bg-success">Staff</span>
                      </td>
                      <td>Arijit</td>
                      <td>
                        <button className='btn btn-primary bg_primary btn-sm'>
                          <i className="fa-regular fa-pen-to-square" />
                        </button>
                        &nbsp;
                        &nbsp;
                        <button className='btn btn-danger bg_danger btn-sm'>
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
  )
}

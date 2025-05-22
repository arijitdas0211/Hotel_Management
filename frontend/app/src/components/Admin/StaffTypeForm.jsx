import DataTable from 'datatables.net-react';
import DT from 'datatables.net-bs5';
import 'datatables.net-select-dt';
import 'datatables.net-responsive-dt';


export default function StaffTypeForm() {
  DataTable.use(DT);
  const options = {
    paging: true,
    responsive: true,
  }
  return (
    <>
      <div className="action_container bg-white shadow-sm">
        <div className="card border-0 p-3" style={{ borderRadius: 0, cursor: "default" }}>
          <h4 className="card-header bg-white p-3">Manage Staff type</h4>
          <div className="card-body container">
            <form className="row align-items-center">
              <div className="col-12 col-md-2 col-lg-2">
                <label htmlFor="staffType" className="form-label fw-medium">Enter Staff type</label>
              </div>
              <div className="col-12 col-md-4 col-lg-4">
                <input
                  type="text"
                  className="form-control staff_type_input"
                  id="staffType"
                  placeholder="i.e. Manager"
                />
              </div>
              <div className="col-12 col-md-3 col-lg-3">
                <button type="submit" className="btn btn-primary bg_primary text-white shadow-sm w-50">ADD</button>
              </div>
            </form>
          </div>
          <hr />
          <div className="card-body container mb-3">
            <DataTable className="table table-striped" options={options}>
              <thead>
                  <tr>
                      <th>#</th>
                      <th>Staff type</th>
                      <th>Created by</th>
                      <th>Actions</th>
                  </tr>
              </thead>
              <tbody>
                  <tr>
                      <td className='fw-medium'>1</td>
                      <td>Chef</td>
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
  );
}
 
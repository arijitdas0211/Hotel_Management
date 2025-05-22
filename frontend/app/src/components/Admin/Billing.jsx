import Loader from "./Loader";
import DataTable from "datatables.net-react";
import DT from "datatables.net-bs5";
import "datatables.net-select-dt";
import "datatables.net-responsive-dt";
import html2pdf from "html2pdf.js";

export default function Billing() {
  DataTable.use(DT);

  const options = {
    paging: true,
    responsive: true,
  };

  const datetime = new Date().toLocaleString().split(",");
  const date = datetime[0];
  const time = datetime[1];

  const generatePDF = (e) => {
    e.preventDefault();

    const element = document.getElementById("bill");

    const opt = {
      margin: 0.5,
      filename: `Bill_${new Date().toISOString()}.pdf`,
      image: { type: "jpeg", quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "letter", orientation: "portrait" },
    };

    html2pdf().set(opt).from(element).save();
  };

  // <Loader />

  return (
    <>
      <div className="action_container bg-white shadow-sm">
        <div
          className="card border-0 p-3"
          style={{ borderRadius: 0, cursor: "default" }}
        >
          <div className="card-header p-3">
            <h4 className="card-title">Manage Billing</h4>
          </div>
          <div className="card-body container">
            <form className="align-items-center">
              <div className="bill row" id="bill">
                <div className="card-header bg-secondary-subtle text-black p-3 mb-3">
                  <h5 className="card-title text-center">ABC Restaurant</h5>
                </div>
                <div className="col-6 mb-3">
                  <span className="text-start fw-bold">
                    Order id: #1278956412
                  </span>
                </div>
                <div className="col-6 mb-3 text-end">
                  <span className="h6">Date: </span>
                  {date}
                  <br />
                  <span className="h6">Time: </span>
                  {time}
                </div>
                <div className="col-12">
                  <table className="table table-responsive">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">Item(s)</th>
                        <th scope="col">Price(₹)</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <th scope="row">1</th>
                        <td>Chicken Biryani</td>
                        <td>260</td>
                      </tr>
                      <tr>
                        <th scope="row">2</th>
                        <td>Chicken Reshmi</td>
                        <td>300</td>
                      </tr>
                    </tbody>
                  </table>
                  <div className="text-end border-2 border-bottom border-black p-3">
                    <span className="fw-bold">Total: ₹560.00</span>
                  </div>
                </div>
              </div>
              <div className="col-12 text-center mt-3">
                <button
                  type="submit"
                  className="myBtn btn btn-primary bg_primary text-white shadow-sm"
                  onClick={generatePDF}
                >
                  Generate Bill
                </button>
                &nbsp;&nbsp;
                <button
                  type="submit"
                  className="myBtn btn btn-dark text-white shadow-sm"
                >
                  Save
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
                    {new Date().getDate()}-{new Date().getMonth()}-
                    {new Date().getFullYear()} | {new Date().getHours()}:
                    {new Date().getMinutes()}:{new Date().getSeconds()}
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

import DataTable from "datatables.net-react";
import DT from "datatables.net-bs5";
import "datatables.net-select-dt";
import "datatables.net-responsive-dt";
import Loader from "./Loader";
import { useEffect, useState } from "react";
import Swal from "sweetalert2";
import api from "../../api";
import { ACCESS_TOKEN } from "../../constants";

export default function StaffTypeForm() {
  DataTable.use(DT);
  const options = {
    paging: true,
    responsive: true,
  };

  const [staffType, setStaffType] = useState("");
  // const [creator, setCreator] = useState("");
  const [staffTypes, setStaffTypes] = useState([]);

  const accessToken = localStorage.getItem(ACCESS_TOKEN);
  const fetchStaffTypes = async () => {
    try {
      const response = await api.get("/api/admin/stafftype/", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setStaffTypes(response.data.data);

      console.log(response.data.data);
    } catch (err) {
      console.error("Failed to fetch staff types", err);
    }
  };

  useEffect(() => {
    fetchStaffTypes();
  }, [accessToken]);

  const handleStaffType = async (e) => {
    e.preventDefault();
    if (!staffType) {
      await Swal.fire({
        icon: "error",
        title: "Staff type cannot be empty.",
        text: "Please enter staff type.",
        confirmButtonText: "OK",
        confirmButtonColor: "crimson",
      });
      return;
    }

    try {
      const response = await api.post(
        "/api/admin/stafftype/",
        { staffType: staffType.trim() },
        {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );

      if (response.status === 201) {
        await Swal.fire({
          icon: "success",
          title: "Staff type added successfully.",
          text: "Please check the staff type list.",
          confirmButtonText: "OK",
          confirmButtonColor: "#28a745",
        });

        setStaffType(""); // clear input after success
        await fetchStaffTypes(); // <--- refetch updated list here
      }
    } catch (error) {
      const msg = JSON.stringify(error?.response?.data);
      await Swal.fire({
        icon: "error",
        title: "Failed to create staff type",
        text: msg,
        confirmButtonText: "OK",
        confirmButtonColor: "crimson",
      });
    }
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
            <h4 className="card-title">Manage Staff type</h4>
          </div>
          <div className="card-body container">
            <div className="row align-items-center">
              <div className="col-12 col-md-2 col-lg-2">
                <label htmlFor="staffType" className="form-label fw-medium">
                  Enter Staff type:{" "}
                </label>
              </div>
              <div className="col-12 col-md-4 col-lg-4">
                <input
                  type="text"
                  className="form-control staff_type_input"
                  id="staffType"
                  placeholder="i.e. Manager"
                  value={staffType}
                  onChange={(e) => setStaffType(e.target.value)}
                />
              </div>
              <div className="col-12 col-md-3 col-lg-3">
                <button
                  type="submit"
                  onClick={handleStaffType}
                  className="btn btn-primary bg_primary text-white shadow-sm w-50"
                >
                  Add staff type
                </button>
              </div>
            </div>
          </div>
          <hr />
          <div className="card-body container mb-3">
            {staffTypes.length > 0 ? (
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
                  {staffTypes.map((item, index) => (
                    <tr key={index}>
                      <td className="fw-medium">{index + 1}</td>
                      <td>{item.staffType}</td>
                      <td>{item.created_by}</td>
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
                  ))}
                </tbody>
              </DataTable>
            ) : (
              <p>Loading staff types...</p>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

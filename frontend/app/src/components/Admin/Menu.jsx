import Loader from "./Loader";
import DataTable from "datatables.net-react";
import DT from "datatables.net-bs5";
import "datatables.net-select-dt";
import "datatables.net-responsive-dt";
import { useState, useEffect, useRef } from "react";

export default function Menu() {
  const [imgUrl, setImgUrl] = useState(null);
  const fileInputRef = useRef(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    const maxSize = 2 * 1024 * 1024;

    if (file.size <= maxSize) {
      const imageUrl = URL.createObjectURL(file);
      setImgUrl(imageUrl);
    } else {
      alert("Please upload an image smaller than 2 MB");
      
      if (imgUrl) URL.revokeObjectURL(imgUrl);
      setImgUrl(null);
      e.target.value = "";
    }
  };

  const removeImg = (e) => {
    e.preventDefault();
    if (imgUrl) {
      URL.revokeObjectURL(imgUrl);
      setImgUrl(null);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  useEffect(() => {
    return () => {
      if (imgUrl) URL.revokeObjectURL(imgUrl);
    };
  }, [imgUrl]);

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
            <h4 className="card-title">Manage Menu</h4>
          </div>
          <div className="card-body container">
            <form className="row align-items-center">
              <div className="col-12 col-md-3 col-lg-3 mb-3">
                <label htmlFor="menuName" className="form-label fw-medium">
                  Menu Name *
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="menuName"
                  placeholder="i.e. Paneer Masala"
                />
              </div>
              <div className="col-12 col-md-3 col-lg-3 mb-3">
                <label htmlFor="menuPrice" className="form-label fw-medium">
                  Price(₹) *
                </label>
                <input
                  type="text"
                  className="form-control"
                  id="menuPrice"
                  placeholder="i.e. 200"
                />
              </div>
              <div className="col-12 col-md-3 col-lg-3 mb-3">
                <label htmlFor="menuImage" className="form-label fw-medium">
                  Image *
                </label>
                <input
                  type="file"
                  className="form-control"
                  id="menuImage"
                  accept="image/*"
                  onChange={handleImageChange}
                  ref={fileInputRef}
                />
              </div>
              {imgUrl ? (
                <div className="col-12 col-md-3 col-lg-3 mb-3 position-relative">
                  <img
                    src={imgUrl}
                    className="img-thumbnail"
                    alt="Menu Preview"
                    style={{ maxHeight: "150px", maxWidth: "250px" }}
                  />
                  <button
                    type="button"
                    title="Remove"
                    className="btn-close position-absolute top-0 start-10 m-1"
                    onClick={removeImg}
                    aria-label="Remove image"
                  />
                </div>
              ) : (
                <div className="col-12 col-md-3 col-lg-3 mb-3">
                  <span className="h6 text-danger border border-1 border-danger text-center p-3 d-block" style={{maxWidth: "150px"}}>
                    Please upload image to preview
                  </span>
                </div>
              )}
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">Food type *</label>
                <select className="form-select">
                  <option>-- Select food type --</option>
                  <option defaultValue="veg">Veg</option>
                  <option value="nonveg">Non-veg</option>
                  <option value="both">Both</option>
                </select>
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">Food category *</label>
                <select className="form-select">
                  <option>-- Select category --</option>
                  <option defaultValue="Indian Starter">Indian Starter</option>
                  <option value="Italian">Italian</option>
                  <option value="Dessert">Dessert</option>
                </select>
              </div>
              <div className="col-12 col-md-4 col-lg-4 mb-3">
                <label className="form-label fw-medium">Status</label>
                <select className="form-select">
                  <option defaultValue="True">Enabled</option>
                  <option value="False">Disabled</option>
                </select>
              </div>
              <div className="col-12 text-center mt-3">
                <button
                  type="submit"
                  className="myBtn btn btn-primary bg_primary text-white shadow-sm"
                >
                  Add Menu
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
                  <th>Image</th>
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
                    <div className="border border-1 border-secondary text-center">
                      <img src="/img/paneer_masala.png" classname="img-thumbnail" alt="Menu Preview" style={{maxWidth:'120px', maxHeight: "100px"}} />
                    </div>
                  </td>
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

import React from 'react';
import "./Card.css";

export default function Dashboard() {
    return (
        <div className="main_body row mt-2">
            {/* Card 1 */}
            <div className="col-md-6 col-xl-3 col-lg-3 col-sm-6 mb-4">
                <div className="card bg_primary shadow border-0 p-3 d-flex flex-row align-items-center justify-content-between">
                    <div className="icon_circle">
                        <i className="card_icon fa-solid fa-users text-white" />
                    </div>
                    <div className="text-end">
                        <h4 className="text_about text-white">Total Users</h4>
                        <p className="total_count text-white">100</p>
                    </div>
                </div>
            </div>

            {/* Card 2 */}
            <div className="col-md-6 col-xl-3 col-lg-3 col-sm-6 mb-4">
                <div className="card bg_success shadow border-0 p-3 d-flex flex-row align-items-center justify-content-between">
                    <div className="icon_circle">
                        <i className="card_icon fa-solid fa-book text-white" />
                    </div>
                    <div className="text-end">
                        <h4 className="text_about text-white">Bookings</h4>
                        <p className="total_count text-white">250</p>
                    </div>
                </div>
            </div>

            {/* Card 3 */}
            <div className="col-md-6 col-xl-3 col-lg-3 col-sm-6 mb-4">
                <div className="card bg_warning shadow border-0 p-3 d-flex flex-row align-items-center justify-content-between">
                    <div className="icon_circle">
                        <i className="card_icon fa-solid fa-hand-holding-dollar text-white" />
                    </div>
                    <div className="text-end">
                        <h4 className="text_about text-white">Revenue</h4>
                        <p className="total_count text-white">&#8377; 5,000</p>
                    </div>
                </div>
            </div>

            {/* Card 4 */}
            <div className="col-md-6 col-xl-3 col-lg-3 col-sm-6 mb-4">
                <div className="card bg_danger shadow border-0 p-3 d-flex flex-row align-items-center justify-content-between">
                    <div className="icon_circle">
                        <i className="card_icon fa-solid fa-comments text-white" />
                    </div>
                    <div className="text-end">
                        <h4 className="text_about text-white">Feedbacks</h4>
                        <p className="total_count text-white">38</p>
                    </div>
                </div>
            </div>
        </div>
    );
}

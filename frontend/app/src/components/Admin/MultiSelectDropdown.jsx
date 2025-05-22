import React, { useState, useRef, useEffect } from "react";
import "../../pages/Admin/Admin.css";

const MultiSelectDropdown = ({
  options,
  selectedOptions,
  setSelectedOptions,
  placeholder = "Select options",
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const dropdownRef = useRef(null);

  const toggleDropdown = () => setIsOpen(!isOpen);

  const handleOptionClick = (option) => {
    if (selectedOptions.includes(option)) {
      setSelectedOptions(selectedOptions.filter((item) => item !== option));
    } else {
      setSelectedOptions([...selectedOptions, option]);
    }
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const filteredOptions = options.filter((option) =>
    option.toLowerCase().includes(searchTerm.toLowerCase())
  );

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="multi-select-dropdown" ref={dropdownRef}>
      <div
        className="form-control dropdown-toggle d-flex justify-content-between align-items-center"
        onClick={toggleDropdown}
      >
        <span>
          {selectedOptions.length > 0
            ? selectedOptions.join(", ")
            : placeholder}
        </span>
        <span className="toggle-icon">
          {/* Replace with any icon you like */}
          <i
            className={`fa-solid ${isOpen ? "fa-angle-up" : "fa-angle-down"}`}
          ></i>
        </span>
      </div>
      {isOpen && (
        <div className="dropdown-menu show w-100 p-2">
          <input
            type="text"
            className="form-control mb-2"
            placeholder="Search..."
            value={searchTerm}
            onChange={handleSearchChange}
          />
          <div className="options-list">
            {filteredOptions.map((option, index) => (
              <div
                key={index}
                className={`dropdown-item ${
                  selectedOptions.includes(option) ? "active" : ""
                }`}
                onClick={() => handleOptionClick(option)}
              >
                <input
                  type="checkbox"
                  checked={selectedOptions.includes(option)}
                  readOnly
                  className="form-check-input me-2"
                />
                {option}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MultiSelectDropdown;

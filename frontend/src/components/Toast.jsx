import React from "react";

export default function Toast({ message, show, onClose, type = "success" }) {
  if (!show) return null;
  return (
    <div className={`fixed top-6 right-6 z-50 px-6 py-4 rounded-lg shadow-lg text-white text-base font-semibold transition-all duration-300 animate-fade-in-out ${type === "success" ? "bg-green-600" : "bg-red-600"}`}>
      {message}
      <button className="ml-4 text-white/80 hover:text-white font-bold" onClick={onClose}>&times;</button>
    </div>
  );
}

import React from "react";

// Función para mostrar toast programáticamente
const showToast = (message, type = "success") => {
  // Crear contenedor si no existe
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'fixed top-4 right-4 z-50 space-y-2';
    document.body.appendChild(toastContainer);
  }

  // Crear elemento de toast
  const toastElement = document.createElement('div');
  toastElement.className = `px-6 py-4 rounded-lg shadow-lg text-white text-sm font-medium transition-all duration-300 transform translate-x-full opacity-0 ${
    type === "success" ? "bg-green-600" : "bg-red-600"
  }`;
  toastElement.textContent = message;

  toastContainer.appendChild(toastElement);

  // Animar entrada
  setTimeout(() => {
    toastElement.classList.remove('translate-x-full', 'opacity-0');
  }, 10);

  // Animar salida y remover
  setTimeout(() => {
    toastElement.classList.add('translate-x-full', 'opacity-0');
    setTimeout(() => {
      if (toastContainer && toastContainer.contains(toastElement)) {
        toastContainer.removeChild(toastElement);
      }
    }, 300);
  }, 3000);
};

// Componente React para uso tradicional
export default function Toast({ message, show, onClose, type = "success" }) {
  if (!show) return null;
  return (
    <div className={`fixed top-6 right-6 z-50 px-6 py-4 rounded-lg shadow-lg text-white text-base font-semibold transition-all duration-300 animate-fade-in-out ${type === "success" ? "bg-green-600" : "bg-red-600"}`}>
      {message}
      <button className="ml-4 text-white/80 hover:text-white font-bold" onClick={onClose}>&times;</button>
    </div>
  );
}

// Métodos estáticos para uso programático
Toast.success = (message) => showToast(message, "success");
Toast.error = (message) => showToast(message, "error");

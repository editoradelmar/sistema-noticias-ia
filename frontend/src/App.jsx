import ChatIA from './components/ChatIA';

import React, { useState } from "react";
import Header from "./components/Header";
import Login from "./components/Login";
import Register from "./components/Register";
import ProyectosList from "./components/ProyectosList";
import ProyectoDetalle from "./components/ProyectoDetalle";
import Maestros from "./components/Maestros";
import NoticiasList from "./components/NoticiasList";
// import NoticiaForm from "./components/NoticiaForm";
import NoticiaGeneracionVista from "./NoticiaGeneracionVista";
import Footer from './components/Footer';

import { useAuth } from "./context/AuthContext";
import Toast from "./components/Toast";

export default function App() {
	const { user } = useAuth();
	const [vista, setVista] = useState("noticias");
	const [proyectoSeleccionado, setProyectoSeleccionado] = useState(null);
	const [showRegister, setShowRegister] = useState(false);
	const [toast, setToast] = useState({ show: false, message: "" });

	if (!user) {
		return showRegister ? (
			<Register onSwitchToLogin={() => setShowRegister(false)} />
		) : (
			<Login onSwitchToRegister={() => setShowRegister(true)} />
		);
	}

	return (
		<div className="min-h-screen bg-slate-100 dark:bg-slate-900 flex flex-col">
			<Header vista={vista} setVista={setVista} />
			<main className="flex-1 max-w-7xl mx-auto w-full px-4 py-8">
				{vista === "proyectos" && (
					<ProyectosList />
				)}
				{vista === "detalle" && proyectoSeleccionado && (
					<ProyectoDetalle
						proyecto={proyectoSeleccionado}
						onClose={() => setVista("proyectos")}
						onEditar={setProyectoSeleccionado}
						onActualizar={() => setVista("proyectos")}
					/>
				)}
				{vista === "maestros" && <Maestros />}
				{vista === "noticias" && <>
					<NoticiasList />
					<Toast message={toast.message} show={toast.show} onClose={() => setToast({ show: false, message: "" })} />
				</>}
				{vista === "crear" && (
					<NoticiaGeneracionVista
						onVolverLista={() => {
							setVista("noticias");
							setTimeout(() => setToast({ show: true, message: "¡Noticias publicadas exitosamente!" }), 100);
							setTimeout(() => setToast({ show: false, message: "" }), 1800);
						}}
					/>
				)}
				{vista === "chat" && <ChatIA />}
			</main>
			<Footer />
		</div>
	);
}

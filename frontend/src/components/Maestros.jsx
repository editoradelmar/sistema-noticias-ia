import { useState } from 'react';
import LLMMaestroList from './LLMMaestroList';
import PromptsList from './PromptsList';
import EstilosList from './EstilosList';
import SeccionesList from './SeccionesList';
import SalidasList from './SalidasList';

const Maestros = () => {
  const [activeTab, setActiveTab] = useState('llms');

  const tabs = [
    { id: 'llms', label: 'Modelos LLM', icon: '🤖' },
    { id: 'prompts', label: 'Prompts', icon: '📝' },
    { id: 'estilos', label: 'Estilos', icon: '🎨' },
    { id: 'secciones', label: 'Secciones', icon: '📂' },
    { id: 'salidas', label: 'Salidas', icon: '📤' }
  ];

  const renderContent = () => {
    switch (activeTab) {
      case 'llms':
        return <LLMMaestroList />;
      case 'prompts':
        return <PromptsList />;
      case 'estilos':
        return <EstilosList />;
      case 'secciones':
        return <SeccionesList />;
      case 'salidas':
        return <SalidasList />;
      default:
        return <LLMMaestroList />;
    }
  };

  return (
    <div className="min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-slate-900 dark:text-slate-100 mb-2">
            ⚙️ Sistema de Maestros
          </h1>
          <p className="text-slate-600 dark:text-slate-400">
            Gestiona modelos LLM, prompts, estilos y canales de publicación
          </p>
        </div>

        {/* Tabs Navigation - responsivo con scroll en móvil */}
        <div className="mb-6 border-b border-slate-700">
          <nav
            className="flex gap-2 sm:gap-4 overflow-x-auto no-scrollbar"
            aria-label="Tabs"
            style={{ WebkitOverflowScrolling: 'touch' }}
          >
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`
                  flex-shrink-0 px-4 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap
                  ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-400'
                      : 'border-transparent text-slate-400 hover:text-slate-300 hover:border-slate-600'
                  }
                `}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content - render the active list directly so each list controls its own panel */}
        <div>
          {renderContent()}
        </div>
      </div>
    </div>
  );
};

export default Maestros;

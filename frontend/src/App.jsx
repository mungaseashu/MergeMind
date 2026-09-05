import { useState, useEffect } from 'react';
import axios from 'axios';
import { Database, Search, Folder, File, Code, Box, Activity, CheckCircle, AlertTriangle, Loader2 } from 'lucide-react';

const API_BASE = 'http://localhost:8000/api/brain';

import { Routes, Route } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import ProjectSetupPage from './pages/ProjectSetupPage';
import DashboardLayout from './pages/DashboardLayout';
import DashboardHome from './pages/DashboardHome';
import AddDocPage from './pages/AddDocPage';
import ArchitecturePage from './pages/ArchitecturePage';

function App() {
  return (
    <Routes>
      {/* Old BrainBuilder route is preserved but maybe deprecated soon */}
      <Route path="/legacy" element={<BrainBuilder />} />
      
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<LoginPage />} />
      <Route path="/setup" element={<ProjectSetupPage />} />
      
      <Route path="/dashboard" element={<DashboardLayout />}>
        <Route index element={<DashboardHome />} />
        <Route path="add-doc" element={<AddDocPage />} />
        <Route path="architecture" element={<ArchitecturePage />} />
      </Route>
      
      {/* Redirect root to dashboard for now */}
      <Route path="/" element={<DashboardLayout />}>
        <Route index element={<DashboardHome />} />
      </Route>
    </Routes>
  );
}

function BrainBuilder() {
  const [repoUrl, setRepoUrl] = useState('https://github.com/tiangolo/fastapi');
  const [jobId, setJobId] = useState(null);
  const [status, setStatus] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    let interval;
    if (jobId && (!status || (status.status !== 'COMPLETED' && status.status !== 'FAILED'))) {
      interval = setInterval(async () => {
        try {
          const res = await axios.get(`${API_BASE}/status/${jobId}`);
          setStatus(res.data);
        } catch (err) {
          console.error(err);
        }
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [jobId, status]);

  const handleBuild = async () => {
    setError(null);
    setStatus(null);
    try {
      const res = await axios.post(`${API_BASE}/index`, { repository_url: repoUrl });
      setJobId(res.data.job_id);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to start indexing');
    }
  };

  return (
    <div className="min-h-screen p-8 max-w-4xl mx-auto">
      <header className="mb-12 text-center border-b pb-8">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 flex items-center justify-center gap-3">
          <Database className="w-10 h-10 text-indigo-600" />
          MERGEMIND CODEBASE BRAIN
        </h1>
        <p className="mt-4 text-gray-500 text-lg">Stage 1: Deterministic Knowledge Graph Extraction</p>
      </header>

      <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8 mb-8">
        <h2 className="text-xl font-semibold mb-6">GitHub Repository</h2>
        <div className="flex gap-4">
          <input 
            type="text" 
            className="flex-1 px-4 py-3 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:bg-white transition-colors"
            placeholder="https://github.com/user/project"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
          />
          <button 
            onClick={handleBuild}
            disabled={!repoUrl || (status && status.status !== 'COMPLETED' && status.status !== 'FAILED')}
            className="px-8 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            Build Brain
          </button>
        </div>
        {error && <p className="mt-4 text-red-500 text-sm">{error}</p>}
      </div>

      {status && (
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-xl font-semibold">Indexing Status</h2>
            <div className="flex items-center gap-2 px-3 py-1 bg-gray-100 rounded-full text-sm font-medium">
              {status.status === 'COMPLETED' && <CheckCircle className="w-4 h-4 text-green-500" />}
              {status.status === 'FAILED' && <AlertTriangle className="w-4 h-4 text-red-500" />}
              {status.status !== 'COMPLETED' && status.status !== 'FAILED' && <Loader2 className="w-4 h-4 text-indigo-500 animate-spin" />}
              {status.status}
            </div>
          </div>

          <div className="mb-8">
            <div className="flex justify-between text-sm text-gray-500 mb-2">
              <span>Progress</span>
              <span>{status.progress}%</span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-3">
              <div 
                className={`h-3 rounded-full transition-all duration-500 ${status.status === 'FAILED' ? 'bg-red-500' : 'bg-indigo-600'}`}
                style={{ width: `${status.progress}%` }}
              ></div>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <StatCard icon={Folder} label="Discovered" value={status.files_discovered} />
            <StatCard icon={File} label="Processed" value={status.files_processed} />
            <StatCard icon={Box} label="Nodes" value={status.nodes_created} />
            <StatCard icon={Activity} label="Relationships" value={status.relationships_created} />
          </div>

          {status.errors && status.errors.length > 0 && (
            <div className="mt-8 p-4 bg-red-50 border border-red-100 rounded-lg">
              <h3 className="text-sm font-semibold text-red-800 flex items-center gap-2 mb-2">
                <AlertTriangle className="w-4 h-4" /> Errors ({status.errors.length})
              </h3>
              <ul className="text-sm text-red-600 space-y-1">
                {status.errors.slice(0, 5).map((err, i) => (
                  <li key={i}>{typeof err === 'string' ? err : `${err.file}: ${err.error}`}</li>
                ))}
                {status.errors.length > 5 && <li>...and {status.errors.length - 5} more</li>}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function StatCard({ icon: Icon, label, value }) {
  return (
    <div className="p-4 border border-gray-100 rounded-xl bg-gray-50/50">
      <div className="flex items-center gap-2 text-gray-500 mb-2">
        <Icon className="w-4 h-4" />
        <span className="text-sm font-medium">{label}</span>
      </div>
      <p className="text-2xl font-bold text-gray-900">{value}</p>
    </div>
  );
}

export default App;

import { useEffect, useState } from 'react';
import { Calendar, CheckCircle2, Clock, AlertCircle, CircleDashed, Loader2, CheckCircle, TriangleAlert } from 'lucide-react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

const BRAIN_API = 'http://localhost:8000/api/brain';

export default function DashboardHome() {
  const { user } = useAuth();

  // ── Indexing job polling ─────────────────────────────────────────────────
  const [jobStatus, setJobStatus] = useState(null);
  const [jobId] = useState(() => localStorage.getItem('mm_job_id'));
  const [repoUrl] = useState(() => localStorage.getItem('mm_repo_url') || '');

  useEffect(() => {
    if (!jobId) return;
    let interval;
    const poll = async () => {
      try {
        const res = await axios.get(`${BRAIN_API}/status/${jobId}`);
        setJobStatus(res.data);
        if (res.data.status === 'COMPLETED' || res.data.status === 'FAILED') {
          clearInterval(interval);
        }
      } catch {
        clearInterval(interval);
      }
    };
    poll();
    interval = setInterval(poll, 2000);
    return () => clearInterval(interval);
  }, [jobId]);

  // ── Static stats ─────────────────────────────────────────────────────────
  const stats = [
    { label: 'Total Requests', value: 42, trend: '+12 this week', icon: CircleDashed, color: 'text-gray-500' },
    { label: 'Active PRs', value: 18, trend: '4 need review', icon: Clock, color: 'text-blue-500' },
    { label: 'High Priority', value: 5, trend: '-2 since yesterday', icon: AlertCircle, color: 'text-orange-500' },
    { label: 'Low Priority', value: 13, trend: '+5 this week', icon: CheckCircle2, color: 'text-green-500' },
  ];

  const activePRs = [
    { id: 1, title: 'Implement new auth flow', author: 'Amélie Laurent', priority: 'High', status: 'In review', time: '2h ago' },
    { id: 2, title: 'Fix navigation bug on mobile', author: 'Floyd Miles', priority: 'High', status: 'In progress', time: '4h ago' },
    { id: 3, title: 'Update dependency packages', author: 'Guy Hawkins', priority: 'Low', status: 'Pending', time: '1d ago' },
    { id: 4, title: 'Refactor state management', author: 'Kristin Watson', priority: 'Low', status: 'In review', time: '1d ago' },
    { id: 5, title: 'Add unit tests for API client', author: 'Amélie Laurent', priority: 'Low', status: 'In progress', time: '2d ago' },
  ];

  const today = new Date().toLocaleDateString('en-US', { day: 'numeric', month: 'long', year: 'numeric' });
  const firstName = user?.username?.split(' ')[0] || 'there';

  return (
    <div className="p-8 lg:p-12">
      {/* Header */}
      <div className="flex justify-between items-start mb-10">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Hello, {firstName} 👋
          </h1>
          <p className="text-gray-500 dark:text-gray-400">
            Here's the current status of your pull requests.
          </p>
        </div>
        <div className="hidden sm:flex items-center gap-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-full px-4 py-2 shadow-sm">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{today}</span>
          <Calendar className="w-4 h-4 text-gray-400" />
        </div>
      </div>

      {/* Indexing job status card */}
      {jobId && jobStatus && (
        <div className={`mb-8 rounded-2xl border p-6 ${
          jobStatus.status === 'COMPLETED'
            ? 'bg-green-50 border-green-200 dark:bg-green-900/10 dark:border-green-800'
            : jobStatus.status === 'FAILED'
            ? 'bg-red-50 border-red-200 dark:bg-red-900/10 dark:border-red-800'
            : 'bg-indigo-50 border-indigo-200 dark:bg-indigo-900/10 dark:border-indigo-800'
        }`}>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              {jobStatus.status === 'COMPLETED' && <CheckCircle className="w-5 h-5 text-green-500" />}
              {jobStatus.status === 'FAILED' && <TriangleAlert className="w-5 h-5 text-red-500" />}
              {jobStatus.status !== 'COMPLETED' && jobStatus.status !== 'FAILED' && (
                <Loader2 className="w-5 h-5 text-indigo-500 animate-spin" />
              )}
              <div>
                <p className="font-semibold text-gray-900 dark:text-white text-sm">
                  {jobStatus.status === 'COMPLETED' ? 'Indexing complete' :
                   jobStatus.status === 'FAILED' ? 'Indexing failed' :
                   'Indexing in progress…'}
                </p>
                <p className="text-xs text-gray-500 truncate max-w-xs">{repoUrl}</p>
              </div>
            </div>
            <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">{jobStatus.progress ?? 0}%</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                jobStatus.status === 'FAILED' ? 'bg-red-500' : 'bg-indigo-600'
              }`}
              style={{ width: `${jobStatus.progress ?? 0}%` }}
            />
          </div>
          <div className="flex gap-6 mt-4 text-xs text-gray-600 dark:text-gray-400">
            <span>🗂 {jobStatus.files_discovered ?? 0} discovered</span>
            <span>✅ {jobStatus.files_processed ?? 0} processed</span>
            <span>🔵 {jobStatus.nodes_created ?? 0} nodes</span>
            <span>🔗 {jobStatus.relationships_created ?? 0} relationships</span>
          </div>
        </div>
      )}

      {/* Stats row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {stats.map((stat, idx) => (
          <div key={idx} className="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl p-6 shadow-sm flex flex-col">
            <div className="flex justify-between items-start mb-4">
              <div className={`p-3 rounded-xl bg-gray-50 dark:bg-gray-900 ${stat.color}`}>
                <stat.icon className="w-6 h-6" />
              </div>
              <span className="text-3xl font-bold text-gray-900 dark:text-white">{stat.value}</span>
            </div>
            <h3 className="text-gray-500 dark:text-gray-400 font-medium mb-1">{stat.label}</h3>
            <p className="text-xs text-gray-400 dark:text-gray-500">{stat.trend}</p>
          </div>
        ))}
      </div>

      {/* Active PRs table */}
      <div>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Active Pull Requests</h2>
          <button className="text-sm font-medium text-indigo-600 hover:text-indigo-700 dark:text-indigo-400">
            View all
          </button>
        </div>

        <div className="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden shadow-sm">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-gray-100 dark:border-gray-700">
                  <th className="py-4 px-6 text-sm font-semibold text-gray-500 dark:text-gray-400">PR Title</th>
                  <th className="py-4 px-6 text-sm font-semibold text-gray-500 dark:text-gray-400">Priority</th>
                  <th className="py-4 px-6 text-sm font-semibold text-gray-500 dark:text-gray-400">Status</th>
                  <th className="py-4 px-6 text-sm font-semibold text-gray-500 dark:text-gray-400">Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                {activePRs.map((pr) => (
                  <tr key={pr.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
                    <td className="py-4 px-6">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-full bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center text-indigo-600 dark:text-indigo-400 font-bold text-xs">
                          {pr.author.charAt(0)}
                        </div>
                        <div>
                          <p className="font-medium text-gray-900 dark:text-white text-sm">{pr.title}</p>
                          <p className="text-xs text-gray-500">{pr.author}</p>
                        </div>
                      </div>
                    </td>
                    <td className="py-4 px-6">
                      <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
                        pr.priority === 'High'
                          ? 'bg-orange-50 text-orange-700 dark:bg-orange-900/20 dark:text-orange-400'
                          : 'bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400'
                      }`}>
                        <div className={`w-1.5 h-1.5 rounded-full ${pr.priority === 'High' ? 'bg-orange-500' : 'bg-green-500'}`} />
                        {pr.priority}
                      </span>
                    </td>
                    <td className="py-4 px-6">
                      <span className="text-sm text-gray-600 dark:text-gray-300 font-medium">{pr.status}</span>
                    </td>
                    <td className="py-4 px-6 text-sm text-gray-500">{pr.time}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}

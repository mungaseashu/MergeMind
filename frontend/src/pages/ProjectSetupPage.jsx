import { useState } from 'react';
import { ArrowRight, Key, Folder, Loader2, AlertCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BRAIN_API = 'http://localhost:8000/api/brain';

export default function ProjectSetupPage() {
  const [projectName, setProjectName] = useState('');
  const [repoUrl, setRepoUrl] = useState('');
  const [githubToken, setGithubToken] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await axios.post(`${BRAIN_API}/index`, {
        project_name: projectName,
        repository_url: repoUrl,
        github_token: githubToken,
      });
      // Store job_id so DashboardHome can poll it
      localStorage.setItem('mm_job_id', res.data.job_id);
      localStorage.setItem('mm_repo_url', repoUrl);
      localStorage.setItem('mm_project_name', projectName);
      navigate('/dashboard');
    } catch (err) {
      const msg = err.response?.data?.detail;
      setError(msg || 'Failed to start indexing. Check the repository URL and try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 flex flex-col items-center justify-center p-4">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-[40%] -right-[10%] w-[70%] h-[70%] rounded-full bg-gradient-to-br from-indigo-100 to-transparent dark:from-indigo-900/20 blur-3xl" />
        <div className="absolute -bottom-[40%] -left-[10%] w-[70%] h-[70%] rounded-full bg-gradient-to-tr from-yellow-100 to-transparent dark:from-yellow-900/20 blur-3xl" />
      </div>

      <div className="relative w-full max-w-xl bg-white dark:bg-gray-900 rounded-3xl shadow-2xl p-8 sm:p-12 border border-gray-100 dark:border-gray-800">

        <div className="text-center mb-10">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-indigo-50 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400 mb-6 shadow-sm">
            <Folder className="w-8 h-8" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-3">Connect your project</h1>
          <p className="text-gray-500 dark:text-gray-400">
            Enter a public GitHub repository URL to begin building the codebase brain.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 ml-1">
              Project Name
            </label>
            <div className="relative">
              <input
                id="project-name"
                type="text"
                required
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                placeholder="My Awesome Project"
                className="w-full bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-2xl px-6 py-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:text-white transition-all shadow-sm"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 ml-1">
              GitHub Repository URL
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
                <Folder className="w-5 h-5" />
              </div>
              <input
                id="repo-url"
                type="url"
                required
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
                placeholder="https://github.com/user/repository"
                className="w-full bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-2xl pl-12 pr-6 py-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:text-white transition-all shadow-sm"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2 ml-1">
              GitHub Access Token <span className="text-gray-400 font-normal">(optional)</span>
            </label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-400">
                <Key className="w-5 h-5" />
              </div>
              <input
                id="access-token"
                type="password"
                value={githubToken}
                onChange={(e) => setGithubToken(e.target.value)}
                placeholder="ghp_xxxxxxxxxxxxxxxxxxxx"
                className="w-full bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-2xl pl-12 pr-6 py-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:text-white transition-all shadow-sm"
              />
            </div>
            <p className="mt-2 text-xs text-gray-500 dark:text-gray-400 ml-1">
              Needed for private repositories. Requires <code>repo</code> and <code>read:org</code> scopes.
            </p>
          </div>

          {error && (
            <div className="flex items-start gap-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-400 text-sm rounded-2xl px-5 py-4">
              <AlertCircle className="w-4 h-4 mt-0.5 shrink-0" />
              {error}
            </div>
          )}

          <button
            id="setup-submit"
            type="submit"
            disabled={loading || !repoUrl}
            className="w-full flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-60 text-white font-medium rounded-2xl px-6 py-4 transition-all shadow-lg hover:shadow-indigo-500/30 mt-4"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Starting indexing…
              </>
            ) : (
              <>
                Continue to Dashboard
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </form>

      </div>
    </div>
  );
}

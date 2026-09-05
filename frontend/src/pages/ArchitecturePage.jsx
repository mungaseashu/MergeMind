import { Layers } from 'lucide-react';

export default function ArchitecturePage() {
  return (
    <div className="p-8 lg:p-12 h-full flex flex-col">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Repository Architecture</h1>
      <p className="text-gray-500 dark:text-gray-400 mb-12">Visual representation of the GitHub repository structure.</p>
      
      <div className="flex-1 border border-gray-200 dark:border-gray-700 rounded-3xl p-12 flex flex-col items-center justify-center text-center bg-white dark:bg-gray-800 shadow-sm relative overflow-hidden">
        <div className="absolute inset-0 bg-gray-50/50 dark:bg-gray-900/50 flex items-center justify-center pointer-events-none" style={{ backgroundImage: 'radial-gradient(#e5e7eb 1px, transparent 1px)', backgroundSize: '24px 24px' }}>
        </div>
        <div className="relative z-10 flex flex-col items-center">
            <Layers className="w-16 h-16 text-gray-400 mb-6" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Architecture Graph Generation</h2>
            <p className="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
            The knowledge graph for the current repository is being rendered. Once indexing is complete, the full node and edge visualization will appear here.
            </p>
        </div>
      </div>
    </div>
  );
}

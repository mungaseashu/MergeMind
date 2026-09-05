import { UploadCloud } from 'lucide-react';

export default function AddDocPage() {
  return (
    <div className="p-8 lg:p-12">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Add Documentation</h1>
      <p className="text-gray-500 dark:text-gray-400 mb-12">Upload a PDF to enrich the MergeMind knowledge graph.</p>
      
      <div className="border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-3xl p-12 flex flex-col items-center justify-center text-center bg-gray-50/50 dark:bg-gray-800/20 max-w-3xl">
        <div className="w-20 h-20 bg-indigo-100 dark:bg-indigo-900/50 rounded-full flex items-center justify-center mb-6">
          <UploadCloud className="w-10 h-10 text-indigo-600 dark:text-indigo-400" />
        </div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-2">Click to upload or drag and drop</h2>
        <p className="text-gray-500 dark:text-gray-400 mb-8 max-w-sm">
          PDF documents up to 50MB are supported. The contents will be processed and added to your project's brain.
        </p>
        <button className="bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl px-8 py-4 transition-all shadow-lg hover:shadow-indigo-500/30">
          Select PDF File
        </button>
      </div>
    </div>
  );
}

import { Outlet, NavLink } from 'react-router-dom';
import { FilePlus, GitMerge, Layers, LogOut, Settings, HelpCircle } from 'lucide-react';

export default function DashboardLayout() {
  const navItems = [
    { name: 'Pull Requests', path: '/dashboard', icon: GitMerge, exact: true },
    { name: 'Add Doc', path: '/dashboard/add-doc', icon: FilePlus },
    { name: 'Architecture', path: '/dashboard/architecture', icon: Layers },
  ];

  return (
    <div className="min-h-screen bg-[#f3f4f6] dark:bg-gray-950 p-4 sm:p-6 lg:p-8 flex items-center justify-center">
      <div className="w-full max-w-[1400px] h-[90vh] min-h-[700px] bg-white dark:bg-gray-900 rounded-[2.5rem] shadow-xl flex overflow-hidden border border-gray-100 dark:border-gray-800">
        
        {/* Sidebar */}
        <div className="w-64 border-r border-gray-100 dark:border-gray-800 p-8 flex flex-col justify-between flex-shrink-0">
          <div>
            <div className="flex items-center gap-3 mb-12">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
                <div className="w-4 h-4 rounded-full border-2 border-white"></div>
              </div>
              <span className="font-bold text-xl text-gray-900 dark:text-white">MergeMind</span>
            </div>

            <nav className="space-y-2">
              {navItems.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.path}
                  end={item.exact}
                  className={({ isActive }) =>
                    `flex items-center gap-4 px-4 py-3 rounded-xl transition-all font-medium ${
                      isActive 
                        ? 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white' 
                        : 'text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white hover:bg-gray-50 dark:hover:bg-gray-800/50'
                    }`
                  }
                >
                  <item.icon className="w-5 h-5" />
                  {item.name}
                </NavLink>
              ))}
            </nav>
          </div>

          <div className="space-y-2">
             <div className="p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-2xl mb-6">
                <h4 className="font-semibold text-indigo-900 dark:text-indigo-100 text-sm mb-1">Upgrade to Pro</h4>
                <p className="text-xs text-indigo-700 dark:text-indigo-300 mb-3">Get advanced insights</p>
                <button className="w-full bg-indigo-200 dark:bg-indigo-600 text-indigo-900 dark:text-white text-xs font-semibold py-2 rounded-lg hover:bg-indigo-300 dark:hover:bg-indigo-500 transition-colors">
                  Upgrade
                </button>
             </div>
             
             <a href="#" className="flex items-center gap-4 px-4 py-3 rounded-xl text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-all font-medium">
                <HelpCircle className="w-5 h-5" />
                Help & Info
             </a>
             <a href="/login" className="flex items-center gap-4 px-4 py-3 rounded-xl text-gray-500 hover:text-gray-900 dark:text-gray-400 dark:hover:text-white transition-all font-medium">
                <LogOut className="w-5 h-5" />
                Log out
             </a>
          </div>
        </div>

        {/* Main Content Area */}
        <div className="flex-1 overflow-y-auto bg-white dark:bg-gray-900 relative">
          <div className="absolute top-0 right-0 w-[50%] h-[50%] bg-gradient-to-bl from-indigo-50 to-transparent dark:from-indigo-900/10 pointer-events-none" />
          <Outlet />
        </div>

      </div>
    </div>
  );
}

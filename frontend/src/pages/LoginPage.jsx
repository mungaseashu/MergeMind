import { Eye, EyeOff } from 'lucide-react';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/setup');
  };

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-950 flex items-center justify-center p-4 sm:p-8">
      <div className="max-w-6xl w-full bg-gradient-to-br from-[#f8f5ea] to-white dark:from-gray-900 dark:to-gray-900 rounded-3xl shadow-2xl overflow-hidden flex flex-col lg:flex-row h-[800px] max-h-[90vh]">
        
        {/* Left Side: Form */}
        <div className="w-full lg:w-1/2 p-8 sm:p-12 lg:p-16 flex flex-col justify-between">
          <div>
            <div className="inline-block border border-gray-300 dark:border-gray-700 rounded-full px-6 py-2 mb-12">
              <span className="font-semibold text-gray-800 dark:text-gray-200">MergeMind</span>
            </div>

            <div className="mb-10 text-center lg:text-left">
              <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Create an account</h1>
              <p className="text-gray-500 dark:text-gray-400">Sign up and get 30 day free trial</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6 max-w-md mx-auto lg:mx-0">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Full name</label>
                <input 
                  type="text" 
                  placeholder="Amélie Laurent"
                  className="w-full bg-white/60 dark:bg-gray-800/60 border border-gray-200 dark:border-gray-700 rounded-full px-6 py-4 focus:outline-none focus:ring-2 focus:ring-[#fbd455] dark:text-white transition-all shadow-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Email</label>
                <input 
                  type="email" 
                  placeholder="amelielaurent7622@gmail.com"
                  className="w-full bg-white/60 dark:bg-gray-800/60 border border-gray-200 dark:border-gray-700 rounded-full px-6 py-4 focus:outline-none focus:ring-2 focus:ring-[#fbd455] dark:text-white transition-all shadow-sm"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Password</label>
                <div className="relative">
                  <input 
                    type={showPassword ? "text" : "password"} 
                    placeholder="****************"
                    className="w-full bg-white/60 dark:bg-gray-800/60 border border-gray-200 dark:border-gray-700 rounded-full px-6 py-4 focus:outline-none focus:ring-2 focus:ring-[#fbd455] dark:text-white transition-all shadow-sm pr-12"
                  />
                  <button 
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-6 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              <button 
                type="submit" 
                className="w-full bg-[#fbd455] hover:bg-[#f2c73d] text-gray-900 font-semibold rounded-full px-6 py-4 transition-colors shadow-md mt-4"
              >
                Submit
              </button>

              <div className="flex gap-4 mt-6">
                <button type="button" className="flex-1 flex items-center justify-center gap-2 bg-transparent border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-200 rounded-full px-6 py-3 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                   <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor"><path d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.17 2.31-.93 3.57-.84 1.51.15 2.67.75 3.4 1.83-2.92 1.8-2.43 5.48.54 6.64-1.03 2.1-1.92 3.66-2.59 4.54zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"/></svg>
                  Apple
                </button>
                <button type="button" className="flex-1 flex items-center justify-center gap-2 bg-transparent border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-200 rounded-full px-6 py-3 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors">
                  <svg viewBox="0 0 24 24" className="w-5 h-5" fill="currentColor"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/></svg>
                  Google
                </button>
              </div>
            </form>
          </div>
          
          <div className="flex justify-between items-center text-sm text-gray-500 dark:text-gray-400 mt-12 lg:mt-0 max-w-md mx-auto lg:mx-0 w-full">
            <p>Have any account? <Link to="/login" className="text-gray-900 dark:text-white underline hover:no-underline font-medium">Sign in</Link></p>
            <a href="#" className="underline hover:no-underline">Terms & Conditions</a>
          </div>
        </div>

        {/* Right Side: Image with glassmorphism overlays */}
        <div className="hidden lg:block lg:w-1/2 relative p-4 pl-0">
          <div className="h-full w-full rounded-2xl overflow-hidden relative">
            <img 
              src="/login-bg.jpg" 
              alt="Office collaboration" 
              className="w-full h-full object-cover"
            />
            {/* Overlay Gradient for readability */}
            <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>

            {/* Glassmorphism Floating Card 1 (Top Left) */}
            <div className="absolute top-12 left-12 bg-[#fbd455] text-gray-900 rounded-xl p-4 shadow-xl backdrop-blur-md animate-fade-in-up">
              <p className="font-semibold text-sm">Task Review With Team</p>
              <p className="text-xs opacity-80">09:30am-10:00am</p>
              <div className="absolute top-3 right-3 w-2 h-2 rounded-full bg-gray-900"></div>
            </div>

            {/* Glassmorphism Floating Card 2 (Bottom Left - Calendar) */}
            <div className="absolute bottom-32 left-12 bg-white/20 dark:bg-gray-900/40 backdrop-blur-xl border border-white/30 rounded-2xl p-6 text-white shadow-2xl">
              <div className="flex justify-between items-center text-sm mb-4 gap-6">
                 <div className="flex flex-col items-center"><span className="opacity-70 text-xs">Sun</span><span className="font-semibold text-lg">22</span></div>
                 <div className="flex flex-col items-center"><span className="opacity-70 text-xs">Mon</span><span className="font-semibold text-lg">23</span></div>
                 <div className="flex flex-col items-center"><span className="opacity-70 text-xs">Tue</span><span className="font-semibold text-lg">24</span></div>
                 <div className="flex flex-col items-center relative"><span className="opacity-70 text-xs text-[#fbd455]">Wed</span><span className="font-semibold text-lg text-[#fbd455]">25</span>
                    <div className="absolute -top-2 w-1 h-1 rounded-full bg-[#fbd455]"></div>
                 </div>
                 <div className="flex flex-col items-center"><span className="opacity-70 text-xs">Thu</span><span className="font-semibold text-lg">26</span></div>
                 <div className="flex flex-col items-center"><span className="opacity-70 text-xs">Fri</span><span className="font-semibold text-lg">27</span></div>
                 <div className="flex flex-col items-center"><span className="opacity-70 text-xs">Sat</span><span className="font-semibold text-lg">28</span></div>
              </div>
            </div>

             {/* Glassmorphism Floating Card 3 (Bottom Center - Meeting) */}
             <div className="absolute bottom-12 left-1/2 -translate-x-1/2 bg-white dark:bg-gray-800 rounded-xl p-5 shadow-2xl min-w-[240px]">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <p className="font-semibold text-sm text-gray-900 dark:text-white">Daily Meeting</p>
                  <p className="text-xs text-gray-500">12:00pm-01:00pm</p>
                </div>
                <div className="w-2 h-2 rounded-full bg-[#fbd455]"></div>
              </div>
              <div className="flex -space-x-2">
                {[1,2,3,4].map((i) => (
                  <img key={i} className="inline-block h-8 w-8 rounded-full ring-2 ring-white dark:ring-gray-800" src={`https://i.pravatar.cc/100?img=${i+10}`} alt=""/>
                ))}
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}

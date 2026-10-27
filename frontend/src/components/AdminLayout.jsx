import React from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ShieldCheck, User, LogOut, LayoutDashboard, Users, FileCheck, 
  CreditCard, Home, Menu
} from 'lucide-react';

export const AdminLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/admin/dashboard', icon: LayoutDashboard },
    { name: 'Members', path: '/admin/members', icon: Users },
    { name: 'Chit Plans', path: '/admin/plans', icon: ShieldCheck },
    { name: 'Payments', path: '/admin/payments', icon: CreditCard },
    { name: 'Pronotes', path: '/admin/pronotes', icon: FileCheck },
  ];

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans relative">
      <div className="flex-1 flex flex-col h-full w-full overflow-hidden">
        {/* Top Nav */}
        <nav className="bg-white/90 backdrop-blur-md border-b border-slate-200 px-4 sm:px-6 py-3.5 flex items-center justify-between z-50 shadow-sm shrink-0 sticky top-0 relative">
          
          <div className="flex items-center gap-2 sm:gap-3">
            {/* Hoverable Menu Option */}
            <div className="group relative flex items-center py-2 -ml-2 pr-2">
              <div className="p-2 rounded-xl hover:bg-slate-100 cursor-pointer text-slate-700 transition-colors">
                <Menu className="w-6 h-6" />
              </div>
              
              {/* Dropdown Side Nav */}
              <div className="absolute top-full left-0 w-64 bg-slate-900 border border-slate-800 shadow-2xl rounded-2xl opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all transform origin-top-left translate-y-2 group-hover:translate-y-0 z-50 overflow-hidden text-slate-300">
                <div className="p-4 border-b border-slate-800 flex items-center gap-2 bg-slate-950 text-white">
                  <ShieldCheck className="w-6 h-6 text-amber-500" />
                  <span className="font-bold text-lg tracking-tight">Admin Menu</span>
                </div>
                <div className="p-2 space-y-1">
                  {navItems.map(item => {
                    const isActive = location.pathname.startsWith(item.path);
                    const Icon = item.icon;
                    return (
                      <Link key={item.path} to={item.path} className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-semibold text-sm ${isActive ? 'bg-corpBlue text-white shadow-md' : 'hover:bg-slate-800 hover:text-white'}`}>
                        <Icon className="w-5 h-5" />
                        {item.name}
                      </Link>
                    );
                  })}
                </div>
              </div>
            </div>

            <ShieldCheck className="w-7 h-7 text-amber-500 hidden sm:block" />
            <span className="font-bold text-lg sm:text-xl tracking-tight text-slate-900 flex items-center gap-2">
               SecureChit
            </span>
            <span className="px-2 py-0.5 rounded-full text-[9px] sm:text-[10px] font-extrabold bg-amber-500/10 text-amber-700 border border-amber-300/30 uppercase tracking-wider hidden md:inline-block">
               ADMIN PORTAL
            </span>
          </div>
          
          <div className="flex items-center gap-2 sm:gap-3">
            <button 
              onClick={() => navigate('/')}
              className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-corpBlue transition-all bg-slate-50 hover:bg-blue-50 px-4 py-2 rounded-xl border border-slate-200 shadow-sm"
            >
              <Home className="w-4 h-4" /> <span className="hidden sm:inline">Public Site</span>
            </button>
            
            <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
              <div className="hidden md:block text-right">
                <span className="block text-xs font-bold text-slate-900 leading-tight">{user?.name}</span>
                <span className="text-[10px] text-slate-400 font-medium">System Administrator</span>
              </div>
              <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-slate-900 text-amber-400 shadow-md">
                <User className="w-5 h-5" />
              </div>
            </div>
            
            <button onClick={handleLogout} className="flex items-center gap-1 text-xs sm:text-sm text-slate-500 hover:text-red-500 transition-colors bg-slate-50 hover:bg-red-50 px-4 py-2 rounded-xl border border-slate-200 ml-2">
              <LogOut className="w-4 h-4" /> <span className="hidden lg:inline">Logout</span>
            </button>
          </div>
        </nav>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto relative bg-slate-50/50">
          {children}
        </main>
      </div>
    </div>
  );
};

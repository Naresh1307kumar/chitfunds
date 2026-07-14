import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, LogOut, User, Bell, FileCheck, Users, HelpCircle, CreditCard, ChevronRight, CheckCircle2, AlertCircle, Home } from 'lucide-react';
import api from '../../services/api';

const MemberDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await api.get('/api/v1/member/notifications/');
        setNotifications(res.data);
      } catch (err) {
        console.error('Failed to load notifications');
      }
    };
    fetchNotifications();
  }, []);

  const handleMarkAsRead = async (id) => {
    try {
      await api.put(`/api/v1/member/notifications/${id}/read`);
      setNotifications(notifications.map(n => n.id === id ? { ...n, is_read: true } : n));
    } catch (err) {
      console.error('Failed to mark notification as read');
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const menuItems = [
    {
      title: "KYC Documents",
      desc: "Complete your KYC to activate your account features.",
      action: "Upload / View →",
      path: "/member/kyc",
      icon: FileCheck,
      color: "from-blue-500 to-indigo-600"
    },
    {
      title: "Guarantor Details",
      desc: "Add guarantor details required for plan joining.",
      action: "Add / View →",
      path: "/member/guarantor",
      icon: Users,
      color: "from-purple-500 to-pink-600"
    },
    {
      title: "Explore Schemes",
      desc: "Explore and join high-yield monthly savings plans.",
      action: "View & Join →",
      path: "/member/plans",
      icon: HelpCircle,
      color: "from-amber-500 to-orange-600"
    },
    {
      title: "My Dues & Payments",
      desc: "Track your installments and make manual payments.",
      action: "Pay Now →",
      path: "/member/payments",
      icon: CreditCard,
      color: "from-emerald-500 to-teal-600"
    }
  ];

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-800 relative overflow-hidden font-sans">
      {/* Background glow effects */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-blue-500/5 rounded-full blur-[100px] pointer-events-none z-0"></div>
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-indigo-500/5 rounded-full blur-[100px] pointer-events-none z-0"></div>

      {/* Navbar */}
      <nav className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between relative z-10 shadow-sm">
        <div className="flex items-center gap-3">
          <ShieldCheck className="w-8 h-8 text-corpBlue" />
          <span className="font-bold text-xl tracking-tight text-slate-900">SecureChit</span>
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-600 border border-blue-200">MEMBER</span>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => navigate('/')}
            className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-corpBlue transition-colors bg-slate-50 hover:bg-blue-50 px-4 py-2 rounded-xl border border-slate-200"
          >
            <Home className="w-4 h-4" /> Home
          </button>
          <Bell className="w-5 h-5 text-slate-500 hover:text-slate-900 cursor-pointer transition-colors" />
          <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
            <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-slate-100 text-corpBlue border border-slate-200">
              <User className="w-5 h-5" />
            </div>
            <div className="hidden md:block text-left">
              <span className="block text-sm font-semibold text-slate-900 leading-tight">{user?.name}</span>
              <span className="text-[11px] text-slate-500">ID: PM-{user?.id || '0042'}</span>
            </div>
          </div>
          <button onClick={handleLogout} className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-red-500 transition-colors bg-slate-50 hover:bg-red-50 px-4 py-2 rounded-xl border border-slate-200">
            <LogOut className="w-4 h-4" /> Logout
          </button>
        </div>
      </nav>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-10 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          
          {/* Main Actions Column */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white border border-slate-200/80 rounded-3xl p-8 shadow-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 rounded-full blur-3xl"></div>
              <h1 className="text-3xl md:text-4xl font-bold text-slate-900 tracking-tight">Welcome, {user?.name}! 👋</h1>
              <p className="text-slate-500 mt-2">Manage your savings, pay installments, and track investments all in one place.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {menuItems.map((item, index) => (
                <div 
                  key={index} 
                  onClick={() => navigate(item.path)} 
                  className="bg-white border border-slate-200/80 rounded-3xl p-6 hover:border-blue-500 hover:shadow-md transition-all cursor-pointer group flex flex-col justify-between h-[200px]"
                >
                  <div className="flex items-start justify-between">
                    <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${item.color} flex items-center justify-center text-white shadow-lg`}>
                      <item.icon className="w-6 h-6" />
                    </div>
                    <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-blue-600 transition-colors" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-slate-900 mb-1">{item.title}</h3>
                    <p className="text-slate-500 text-xs leading-relaxed">{item.desc}</p>
                  </div>
                  <span className="text-corpBlue text-sm font-semibold tracking-wide mt-2 block">{item.action}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right Sidebar Stack */}
          <div className="space-y-6">
            
            {/* 1. Quick Profile Summary Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <h3 className="font-bold text-base text-slate-900 mb-4 pb-3 border-b border-slate-100">Member Status</h3>
              <div className="flex items-center gap-4 mb-4">
                <div className="w-14 h-14 rounded-full bg-blue-50 border border-blue-100 flex items-center justify-center text-corpBlue text-xl font-bold">
                  {user?.name ? user.name[0] : 'U'}
                </div>
                <div>
                  <h4 className="font-bold text-slate-950 text-base">{user?.name}</h4>
                  <div className="flex items-center gap-1.5 mt-1">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    <span className="text-xs font-semibold text-emerald-600">KYC Verified</span>
                  </div>
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4 pt-2 text-center border-t border-slate-100">
                <div className="bg-slate-50 rounded-xl p-3 border border-slate-100">
                  <span className="block text-xs text-slate-400">Active Plans</span>
                  <span className="text-lg font-bold text-slate-900">1 Plan</span>
                </div>
                <div className="bg-slate-50 rounded-xl p-3 border border-slate-100">
                  <span className="block text-xs text-slate-400">Total Saved</span>
                  <span className="text-lg font-bold text-slate-900">₹999</span>
                </div>
              </div>
            </div>

            {/* 2. Interactive Illustration Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-8 shadow-sm text-center flex flex-col items-center relative overflow-hidden">
              <div className="w-full max-w-[200px] aspect-square flex items-center justify-center mb-4 relative">
                <div className="absolute inset-0 bg-blue-500/5 rounded-full blur-3xl animate-pulse"></div>
                <img 
                  src="/images/member_db.png" 
                  alt="Fintech Growth Illustration" 
                  className="w-full h-full object-contain relative z-10 animate-float" 
                />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-1">Secure Ledger Savings</h3>
              <p className="text-slate-500 text-xs leading-relaxed max-w-xs">Your investments are fully audited and secured with blockchain-backed records.</p>
            </div>

            {/* 3. Live Notifications Feed Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
                <h3 className="font-bold text-base text-slate-900">Recent Alerts</h3>
                <span className="text-xs font-semibold bg-blue-50 text-blue-600 px-2 py-0.5 rounded-full">New</span>
              </div>
              <div className="space-y-3 max-h-[300px] overflow-y-auto pr-1">
                {notifications.length === 0 ? (
                  <p className="text-slate-400 text-xs text-center py-4">No notifications yet.</p>
                ) : (
                  notifications.map(n => (
                    <div 
                      key={n.id} 
                      onClick={() => !n.is_read && handleMarkAsRead(n.id)}
                      className={`flex gap-3 items-start text-xs border-b border-slate-50 last:border-0 pb-3 last:pb-0 cursor-pointer p-1.5 rounded-xl transition-all ${!n.is_read ? 'font-semibold bg-blue-50/40 border border-blue-100/50 shadow-sm' : 'opacity-70'}`}
                    >
                      {n.notification_type === 'success' ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" />
                      ) : (
                        <AlertCircle className={`w-4 h-4 flex-shrink-0 mt-0.5 ${n.notification_type === 'warning' ? 'text-amber-500' : 'text-blue-500'}`} />
                      )}
                      <div className="flex-grow">
                        <p className="text-slate-700 leading-normal">{n.message}</p>
                        <span className="text-[9px] text-slate-400 block mt-1">Click to mark read</span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
};

export default MemberDashboard;

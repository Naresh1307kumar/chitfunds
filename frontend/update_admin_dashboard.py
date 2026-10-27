content = """import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { 
  ShieldCheck, LogOut, Users, BarChart3, CreditCard, Trophy, Bell, Settings, 
  Calendar, FileText, Download, Home, ArrowUpRight, Activity, Sparkles, CheckCircle2, AlertCircle 
} from 'lucide-react';
import api from '../../services/api';

const AdminDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/admin/login');
  };

  const [dashboardData, setDashboardData] = useState({
    total_members: '—',
    active_plans: '—',
    monthly_collection: '—',
    pending_draws: '—',
    pending_approvals: '—'
  });

  const [pendingActions, setPendingActions] = useState([]);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/api/v1/admin/dashboard/stats');
        setDashboardData(res.data);
      } catch (err) {
        console.error('Failed to load stats');
      }
    };
    const fetchPendingActions = async () => {
      try {
        const res = await api.get('/api/v1/admin/dashboard/pending-actions');
        setPendingActions(res.data);
      } catch (err) {
        console.error('Failed to load pending actions');
      }
    };
    fetchStats();
    fetchPendingActions();
  }, []);

  const handleDownloadReport = async (reportType) => {
    try {
      const response = await api.get(`/api/v1/admin/reports/${reportType}/download`, {
        responseType: 'blob'
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${reportType}_report_${new Date().toISOString().slice(0, 10)}.csv`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error('Failed to download report', err);
      alert('Failed to download report. Please make sure server is running.');
    }
  };

  const stats = [
    { 
      label: 'Total Active Members', 
      value: dashboardData.total_members, 
      subtext: '+12% Growth', 
      icon: Users, 
      color: 'from-blue-600 to-indigo-600',
      border: 'border-blue-100',
      badge: 'Active Accounts' 
    },
    { 
      label: 'Active Chit Plans', 
      value: dashboardData.active_plans, 
      subtext: '100% Auction Schemes', 
      icon: BarChart3, 
      color: 'from-amber-500 to-orange-600',
      border: 'border-amber-100',
      badge: 'Live Schemes' 
    },
    { 
      label: 'This Month Collection', 
      value: dashboardData.monthly_collection !== '—' ? `₹${dashboardData.monthly_collection.toLocaleString()}` : '—', 
      subtext: 'Verified Ledger', 
      icon: CreditCard, 
      color: 'from-emerald-500 to-teal-600',
      border: 'border-emerald-100',
      badge: 'Collections' 
    },
    { 
      label: 'Pending Monthly Draws', 
      value: dashboardData.pending_draws, 
      subtext: 'Ready to Conduct', 
      icon: Trophy, 
      color: 'from-purple-600 to-pink-600',
      border: 'border-purple-100',
      badge: 'AI Winner Ready' 
    },
  ];

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-800 relative overflow-hidden font-sans">
      {/* Background glow effects */}
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-blue-600/5 rounded-full blur-[120px] pointer-events-none z-0"></div>
      <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-indigo-600/5 rounded-full blur-[120px] pointer-events-none z-0"></div>

      {/* Top Navbar */}
      <nav className="bg-white/90 backdrop-blur-md border-b border-slate-200/80 px-6 py-4 flex items-center justify-between relative z-10 shadow-sm sticky top-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-2xl bg-gradient-to-br from-slate-900 to-corpNavy flex items-center justify-center text-amber-400 shadow-md">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <span className="font-bold text-xl tracking-tight text-slate-900">SecureChit</span>
          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-amber-500/10 text-amber-700 border border-amber-300/30 uppercase tracking-wider">
            ADMIN PORTAL
          </span>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => navigate('/')}
            className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-corpBlue transition-all bg-slate-50 hover:bg-blue-50 px-4 py-2 rounded-xl border border-slate-200 shadow-sm"
          >
            <Home className="w-4 h-4" /> Public Site
          </button>
          <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
            <div className="hidden md:block text-right">
              <span className="block text-xs font-bold text-slate-900 leading-tight">{user?.name}</span>
              <span className="text-[10px] text-slate-400 font-medium">System Administrator</span>
            </div>
          </div>
          <button 
            onClick={handleLogout} 
            className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-red-600 transition-all bg-slate-50 hover:bg-red-50 px-4 py-2 rounded-xl border border-slate-200 shadow-sm"
          >
            <LogOut className="w-4 h-4" /> Logout
          </button>
        </div>
      </nav>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          
          {/* Main Info & Metrics */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Executive Hero Banner */}
            <div className="bg-gradient-to-br from-slate-900 via-corpNavy to-slate-800 rounded-3xl p-8 shadow-xl text-white relative overflow-hidden border border-slate-800">
              <div className="absolute -top-12 -right-12 w-56 h-56 bg-amber-500/10 rounded-full blur-3xl pointer-events-none"></div>
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 relative z-10">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Sparkles className="w-4 h-4 text-amber-400 animate-pulse" />
                    <span className="text-xs font-bold uppercase tracking-widest text-amber-400">Executive Dashboard</span>
                  </div>
                  <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">System Operations Overview</h1>
                  <p className="text-slate-300 text-sm mt-2 max-w-lg leading-relaxed">
                    Monitor member accounts, execute monthly AI winner draws, and track fund ledgers in real-time.
                  </p>
                </div>
                <div className="bg-white/10 backdrop-blur-md rounded-2xl p-4 border border-white/10 text-center min-w-[160px]">
                  <span className="text-xs text-slate-300 block mb-1">Current Status</span>
                  <span className="text-sm font-extrabold text-emerald-400 flex items-center justify-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span> Live & Healthy
                  </span>
                </div>
              </div>
            </div>

            {/* Stats Metric Cards Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {stats.map((stat, i) => (
                <div 
                  key={i} 
                  className={`bg-white/90 backdrop-blur-md border ${stat.border} rounded-3xl p-6 shadow-sm hover:shadow-lg transition-all duration-300 flex items-center justify-between group hover:-translate-y-1`}
                >
                  <div>
                    <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400 block mb-1">
                      {stat.badge}
                    </span>
                    <p className="text-sm font-semibold text-slate-600 mb-1">{stat.label}</p>
                    <p className="text-3xl font-extrabold text-slate-900 tracking-tight">{stat.value}</p>
                    <p className="text-[11px] font-semibold text-emerald-600 mt-1 flex items-center gap-1">
                      <ArrowUpRight className="w-3 h-3" /> {stat.subtext}
                    </p>
                  </div>
                  <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${stat.color} flex items-center justify-center text-white shadow-md group-hover:scale-110 transition-transform`}>
                    <stat.icon className="w-7 h-7" />
                  </div>
                </div>
              ))}
            </div>

            {/* Operations Management Shortcuts Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div 
                className="bg-white border border-slate-200/80 rounded-3xl p-6 hover:border-blue-500 hover:shadow-lg transition-all cursor-pointer group text-left flex flex-col justify-between h-[180px]" 
                onClick={() => navigate('/admin/members')}
              >
                <div className="w-12 h-12 rounded-2xl bg-blue-50 text-blue-600 flex items-center justify-center border border-blue-100 group-hover:bg-blue-600 group-hover:text-white transition-colors shadow-sm">
                  <Users className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900 mb-0.5">Manage Members</h3>
                  <p className="text-slate-500 text-xs">Approve registrations & view KYC details</p>
                </div>
                <span className="text-corpBlue text-xs font-bold tracking-wide flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  Open Member Portal <ArrowUpRight className="w-3.5 h-3.5" />
                </span>
              </div>

              <div 
                className="bg-white border border-slate-200/80 rounded-3xl p-6 hover:border-amber-500 hover:shadow-lg transition-all cursor-pointer group text-left flex flex-col justify-between h-[180px]" 
                onClick={() => navigate('/admin/plans')}
              >
                <div className="w-12 h-12 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center border border-amber-100 group-hover:bg-amber-500 group-hover:text-white transition-colors shadow-sm">
                  <BarChart3 className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900 mb-0.5">Chit Schemes</h3>
                  <p className="text-slate-500 text-xs">Manage active schemes & conduct draws</p>
                </div>
                <span className="text-amber-600 text-xs font-bold tracking-wide flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  Manage Schemes <ArrowUpRight className="w-3.5 h-3.5" />
                </span>
              </div>

              <div 
                className="bg-white border border-slate-200/80 rounded-3xl p-6 hover:border-emerald-500 hover:shadow-lg transition-all cursor-pointer group text-left flex flex-col justify-between h-[180px]" 
                onClick={() => navigate('/admin/payments')}
              >
                <div className="w-12 h-12 rounded-2xl bg-emerald-50 text-emerald-600 flex items-center justify-center border border-emerald-100 group-hover:bg-emerald-600 group-hover:text-white transition-colors shadow-sm">
                  <CreditCard className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-slate-900 mb-0.5">Payment Ledger</h3>
                  <p className="text-slate-500 text-xs">Verify installment receipts & dues</p>
                </div>
                <span className="text-emerald-600 text-xs font-bold tracking-wide flex items-center gap-1 group-hover:translate-x-1 transition-transform">
                  Verify Payments <ArrowUpRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>

            {/* Reports Download Center */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <FileText className="w-5 h-5 text-corpBlue" />
                  <h3 className="font-bold text-base text-slate-900">Operations & Financial Reports</h3>
                </div>
                <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">Instant Export</span>
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {[
                  { id: 'members', title: 'Members Status Report', desc: 'Active members & KYC status' },
                  { id: 'payments', title: 'Collections History', desc: 'Total collections & transaction log' },
                  { id: 'overdue', title: 'Overdue Installments', desc: 'Pending & overdue payments feed' },
                  { id: 'revenue', title: 'Revenue & Commission', desc: 'Pool values & 5% admin margin' }
                ].map(r => (
                  <button 
                    key={r.id}
                    onClick={() => handleDownloadReport(r.id)}
                    className="flex items-center justify-between p-4 bg-slate-50 hover:bg-blue-50/60 border border-slate-200 hover:border-blue-300 rounded-2xl text-left transition-all group shadow-sm"
                  >
                    <div>
                      <span className="block text-xs font-bold text-slate-800 group-hover:text-corpBlue transition-colors">{r.title}</span>
                      <span className="text-[10px] text-slate-400 mt-0.5 block">{r.desc}</span>
                    </div>
                    <div className="w-8 h-8 rounded-xl bg-white border border-slate-200 group-hover:border-blue-300 flex items-center justify-center text-slate-400 group-hover:text-corpBlue transition-colors shadow-sm">
                      <Download className="w-4 h-4" />
                    </div>
                  </button>
                ))}
              </div>
            </div>

          </div>

          {/* Right Sidebar Stack */}
          <div className="space-y-6">
            
            {/* 1. System Health Widget */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <h3 className="font-bold text-base text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center justify-between">
                <span>System Activity</span>
                <Activity className="w-4 h-4 text-emerald-500 animate-pulse" />
              </h3>
              <div className="space-y-3.5 text-xs">
                <div className="flex justify-between items-center bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                  <span className="text-slate-500 font-medium">Database Connection:</span>
                  <span className="font-bold text-emerald-600 flex items-center gap-1.5">
                    <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping"></span> Active
                  </span>
                </div>
                <div className="flex justify-between items-center bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                  <span className="text-slate-500 font-medium">Pending Approvals:</span>
                  <span className="font-bold text-amber-600">
                    {dashboardData.pending_approvals === '—' ? '—' : `${dashboardData.pending_approvals} Member${dashboardData.pending_approvals !== 1 ? 's' : ''}`}
                  </span>
                </div>
                <div className="flex justify-between items-center bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                  <span className="text-slate-500 font-medium">Server API Latency:</span>
                  <span className="font-bold text-slate-800">12ms (Optimal)</span>
                </div>
              </div>
            </div>

            {/* 2. Business Analytics Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm text-center flex flex-col items-center relative overflow-hidden">
              <div className="w-full max-w-[180px] aspect-square flex items-center justify-center mb-3 relative">
                <div className="absolute inset-0 bg-indigo-500/5 rounded-full blur-3xl animate-pulse"></div>
                <img 
                  src="/images/admin_db.png" 
                  alt="System Analytics Illustration" 
                  className="w-full h-full object-contain relative z-10 animate-float" 
                />
              </div>
              <h3 className="text-base font-bold text-slate-900 mb-1">Automated AI Allocation</h3>
              <p className="text-slate-500 text-xs leading-relaxed max-w-xs">
                AI Smart Engine ranks auction bids based on emergency priorities (Hospital Rank #1).
              </p>
            </div>

            {/* 3. Pending Actions Checklist Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
                <h3 className="font-bold text-base text-slate-900">Pending Actions</h3>
                <span className="text-xs font-bold bg-amber-50 text-amber-700 px-2.5 py-0.5 rounded-full border border-amber-200">Alerts</span>
              </div>
              <div className="space-y-3">
                {pendingActions.length === 0 ? (
                  <div className="text-xs text-slate-400 text-center py-4 flex items-center justify-center gap-1">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" /> All actions completed!
                  </div>
                ) : (
                  pendingActions.map(action => (
                    <div key={action.id} className="flex gap-3 items-start text-xs border-b border-slate-50 last:border-0 pb-3 last:pb-0">
                      <AlertCircle className="w-4 h-4 text-amber-500 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-slate-800 leading-normal font-semibold">{action.text}</p>
                        <span className="text-[10px] font-bold text-amber-600 block mt-1 uppercase">{action.priority}</span>
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

export default AdminDashboard;
"""

open('src/pages/admin/Dashboard.jsx', 'w', encoding='utf-8').write(content)
print("AdminDashboard updated with ultra-premium design!")

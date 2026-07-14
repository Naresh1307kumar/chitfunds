import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { ShieldCheck, LogOut, Users, BarChart3, CreditCard, Trophy, Bell, Settings, Calendar, FileText, Download, Home } from 'lucide-react';
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

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await api.get('/api/v1/admin/dashboard/stats');
        setDashboardData(res.data);
      } catch (err) {
        console.error('Failed to load stats');
      }
    };
    fetchStats();
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
      alert('Failed to download report. Please make sure uvicorn is running.');
    }
  };

  const stats = [
    { label: 'Total Members', value: dashboardData.total_members, icon: Users, color: 'from-blue-500 to-indigo-600' },
    { label: 'Active Plans', value: dashboardData.active_plans, icon: BarChart3, color: 'from-purple-500 to-pink-600' },
    { label: 'This Month Collection', value: dashboardData.monthly_collection !== '—' ? `₹${dashboardData.monthly_collection.toLocaleString()}` : '—', icon: CreditCard, color: 'from-emerald-500 to-teal-600' },
    { label: 'Pending Draws', value: dashboardData.pending_draws, icon: Trophy, color: 'from-amber-500 to-orange-600' },
  ];

  const [pendingActions, setPendingActions] = useState([]);

  useEffect(() => {
    const fetchPendingActions = async () => {
      try {
        const res = await api.get('/api/v1/admin/dashboard/pending-actions');
        setPendingActions(res.data);
      } catch (err) {
        console.error('Failed to load pending actions');
      }
    };
    fetchPendingActions();
  }, []);

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-800 relative overflow-hidden font-sans">
      {/* Background glow effects */}
      <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-indigo-500/5 rounded-full blur-[100px] pointer-events-none z-0"></div>
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-blue-500/5 rounded-full blur-[100px] pointer-events-none z-0"></div>

      {/* Navbar */}
      <nav className="bg-white border-b border-slate-200 px-6 py-4 flex items-center justify-between relative z-10 shadow-sm">
        <div className="flex items-center gap-3">
          <ShieldCheck className="w-8 h-8 text-corpBlue" />
          <span className="font-bold text-xl tracking-tight text-slate-900">SecureChit</span>
          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-corpBlue/10 text-corpBlue border border-corpBlue/20">ADMIN</span>
        </div>
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/')}
            className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-corpBlue transition-colors bg-slate-50 hover:bg-blue-50 px-4 py-2 rounded-xl border border-slate-200"
          >
            <Home className="w-4 h-4" /> Home
          </button>
          <Bell className="w-5 h-5 text-slate-500 hover:text-slate-900 cursor-pointer transition-colors" />
          <Settings className="w-5 h-5 text-slate-500 hover:text-slate-900 cursor-pointer transition-colors" />
          <span className="text-sm font-semibold text-slate-900">{user?.name}</span>
          <button onClick={handleLogout} className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-red-500 transition-colors bg-slate-50 hover:bg-red-50 px-4 py-2 rounded-xl border border-slate-200">
            <LogOut className="w-4 h-4" /> Logout
          </button>
        </div>
      </nav>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-6 py-10 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          
          {/* Main Info & Metrics */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white border border-slate-200/80 rounded-3xl p-8 shadow-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/5 rounded-full blur-3xl"></div>
              <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Admin Dashboard</h1>
              <p className="text-slate-500 mt-2">Welcome back, {user?.name}. Here's your operations overview.</p>
            </div>

            {/* Stats Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {stats.map((stat, i) => (
                <div key={i} className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm flex items-center justify-between">
                  <div>
                    <p className="text-sm text-slate-500 mb-1">{stat.label}</p>
                    <p className="text-3xl font-extrabold text-slate-900 tracking-tight">{stat.value}</p>
                  </div>
                  <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${stat.color} flex items-center justify-center text-white shadow-lg`}>
                    <stat.icon className="w-7 h-7" />
                  </div>
                </div>
              ))}
            </div>

            {/* Download Reports Panel */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-4 pb-3 border-b border-slate-100">
                <FileText className="w-5 h-5 text-corpBlue" />
                <h3 className="font-bold text-base text-slate-900">Download Operations Reports</h3>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <button 
                  onClick={() => handleDownloadReport('members')}
                  className="flex items-center justify-between p-4 bg-slate-50 hover:bg-blue-50 border border-slate-200 hover:border-blue-300 rounded-2xl text-left transition-all group"
                >
                  <div>
                    <span className="block text-sm font-bold text-slate-800">Members Status Report</span>
                    <span className="text-[11px] text-slate-400">List of all registered members & KYC</span>
                  </div>
                  <Download className="w-5 h-5 text-slate-400 group-hover:text-corpBlue transition-colors" />
                </button>
                
                <button 
                  onClick={() => handleDownloadReport('payments')}
                  className="flex items-center justify-between p-4 bg-slate-50 hover:bg-blue-50 border border-slate-200 hover:border-blue-300 rounded-2xl text-left transition-all group"
                >
                  <div>
                    <span className="block text-sm font-bold text-slate-800">Collections History</span>
                    <span className="text-[11px] text-slate-400">Total payments collected & status</span>
                  </div>
                  <Download className="w-5 h-5 text-slate-400 group-hover:text-corpBlue transition-colors" />
                </button>

                <button 
                  onClick={() => handleDownloadReport('overdue')}
                  className="flex items-center justify-between p-4 bg-slate-50 hover:bg-blue-50 border border-slate-200 hover:border-blue-300 rounded-2xl text-left transition-all group"
                >
                  <div>
                    <span className="block text-sm font-bold text-slate-800">Overdue Installments</span>
                    <span className="text-[11px] text-slate-400">Pending/overdue payments feed</span>
                  </div>
                  <Download className="w-5 h-5 text-slate-400 group-hover:text-corpBlue transition-colors" />
                </button>

                <button 
                  onClick={() => handleDownloadReport('revenue')}
                  className="flex items-center justify-between p-4 bg-slate-50 hover:bg-blue-50 border border-slate-200 hover:border-blue-300 rounded-2xl text-left transition-all group"
                >
                  <div>
                    <span className="block text-sm font-bold text-slate-800">Revenue & Draws Summary</span>
                    <span className="text-[11px] text-slate-400">Pool values & admin commission</span>
                  </div>
                  <Download className="w-5 h-5 text-slate-400 group-hover:text-corpBlue transition-colors" />
                </button>
              </div>
            </div>

            {/* Operations Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white border border-slate-200/80 rounded-3xl p-6 hover:border-blue-500 hover:shadow-md transition-all cursor-pointer text-center group" onClick={() => navigate('/admin/members')}>
                <Users className="w-12 h-12 mx-auto mb-4 text-corpBlue" />
                <h3 className="text-lg font-bold text-slate-900 mb-2">Members</h3>
                <p className="text-blue-600 text-xs font-semibold group-hover:text-blue-500 transition-colors">Manage & Approve →</p>
              </div>
              <div className="bg-white border border-slate-200/80 rounded-3xl p-6 hover:border-blue-500 hover:shadow-md transition-all cursor-pointer text-center group" onClick={() => navigate('/admin/plans')}>
                <BarChart3 className="w-12 h-12 mx-auto mb-4 text-corpBlue" />
                <h3 className="text-lg font-bold text-slate-900 mb-2">Chit Plans</h3>
                <p className="text-blue-600 text-xs font-semibold group-hover:text-blue-500 transition-colors">Manage Schemes →</p>
              </div>
              <div className="bg-white border border-slate-200/80 rounded-3xl p-6 hover:border-blue-500 hover:shadow-md transition-all cursor-pointer text-center group" onClick={() => navigate('/admin/payments')}>
                <CreditCard className="w-12 h-12 mx-auto mb-4 text-corpBlue" />
                <h3 className="text-lg font-bold text-slate-900 mb-2">Payments</h3>
                <p className="text-blue-600 text-xs font-semibold group-hover:text-blue-500 transition-colors">Verify Payments →</p>
              </div>
            </div>
          </div>

          {/* Right Sidebar Stack */}
          <div className="space-y-6">
            
            {/* 1. Quick Info/System Health Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <h3 className="font-bold text-base text-slate-900 mb-4 pb-3 border-b border-slate-100">System Activity</h3>
              <div className="space-y-3">
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500">Database Connection:</span>
                  <span className="font-semibold text-emerald-600 flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-emerald-500"></span> Active</span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500">Pending Approvals:</span>
                  <span className="font-semibold text-amber-600">
                    {dashboardData.pending_approvals === '—' ? '—' : `${dashboardData.pending_approvals} Member${dashboardData.pending_approvals !== 1 ? 's' : ''}`}
                  </span>
                </div>
                <div className="flex justify-between text-xs">
                  <span className="text-slate-500">Server Status:</span>
                  <span className="font-semibold text-slate-900">Healthy</span>
                </div>
              </div>
            </div>

            {/* 2. Premium Floating Illustration Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-8 shadow-sm text-center flex flex-col items-center relative overflow-hidden">
              <div className="w-full max-w-[200px] aspect-square flex items-center justify-center mb-4 relative">
                <div className="absolute inset-0 bg-indigo-500/5 rounded-full blur-3xl animate-pulse"></div>
                <img 
                  src="/images/admin_db.png" 
                  alt="System Analytics Illustration" 
                  className="w-full h-full object-contain relative z-10 animate-float" 
                />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-1">Business Analytics</h3>
              <p className="text-slate-500 text-xs leading-relaxed max-w-xs">Track real-time system performance, total collections, and automated schemes payouts.</p>
            </div>

            {/* 3. Pending Actions Checklist Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
                <h3 className="font-bold text-base text-slate-900">Pending Actions</h3>
                <span className="text-xs font-semibold bg-amber-50 text-amber-600 px-2 py-0.5 rounded-full">Alerts</span>
              </div>
              <div className="space-y-4">
                {pendingActions.length === 0 ? (
                  <div className="text-xs text-slate-400 text-center py-4">✅ No pending actions right now!</div>
                ) : (
                  pendingActions.map(action => (
                    <div key={action.id} className="flex gap-3 items-start text-xs border-b border-slate-50 last:border-0 pb-3 last:pb-0">
                      <Calendar className="w-4 h-4 text-corpBlue flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-slate-700 leading-normal font-semibold">{action.text}</p>
                        <span className="text-[10px] text-slate-400 block mt-1">{action.priority}</span>
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

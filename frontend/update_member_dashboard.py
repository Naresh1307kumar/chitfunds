content = """import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import { 
  ShieldCheck, LogOut, User, Bell, FileCheck, Users, HelpCircle, 
  CreditCard, ChevronRight, CheckCircle2, AlertCircle, Home, 
  Trophy, Crown, Ticket, Sparkles, Calendar, Clock, Lock, X
} from 'lucide-react';
import api from '../../services/api';

const MemberDashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState([]);
  const [myPlans, setMyPlans] = useState([]);
  const [loadingPlans, setLoadingPlans] = useState(true);

  // Modal State for Scheme Schedule View
  const [activePlanModal, setActivePlanModal] = useState(null);

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const res = await api.get('/api/v1/member/notifications/');
        setNotifications(res.data);
      } catch (err) {
        console.error('Failed to load notifications');
      }
    };

    const fetchMyPlans = async () => {
      try {
        const res = await api.get('/api/v1/member/plans/my');
        setMyPlans(res.data);
      } catch (err) {
        console.error('Failed to load my plans');
      } finally {
        setLoadingPlans(false);
      }
    };

    fetchNotifications();
    if (user?.status === 'active') {
      fetchMyPlans();
    } else {
      setLoadingPlans(false);
    }
  }, [user]);

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
      desc: "Track your installments and make online payments.",
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
            onClick={() => navigate('/member/payments')}
            className="flex items-center gap-1.5 text-xs font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 px-4 py-2 rounded-xl shadow-sm transition-all"
          >
            <CreditCard className="w-4 h-4" /> Pay Current Month Due
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

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-10 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          
          {/* Main Actions Column */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* User Welcome Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-8 shadow-sm relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-blue-500/5 rounded-full blur-3xl"></div>
              <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Member Portal</h1>
              <p className="text-slate-500 mt-2 text-sm leading-relaxed">
                Welcome back, <strong className="text-slate-800">{user?.name}</strong>. Manage your joined schemes and make installment payments.
              </p>
            </div>

            {/* Joined Schemes Summary Section */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
              <div className="flex items-center justify-between mb-6 pb-3 border-b border-slate-100">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-2xl bg-amber-50 text-amber-600 flex items-center justify-center border border-amber-100">
                    <Trophy className="w-5 h-5" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg text-slate-900">My Joined Schemes</h3>
                    <p className="text-xs text-slate-500">Click on your joined scheme to view month-by-month schedule & pay dues</p>
                  </div>
                </div>
              </div>

              {loadingPlans ? (
                <div className="text-center py-6 text-slate-400 text-xs">Loading joined schemes...</div>
              ) : myPlans.length === 0 ? (
                <div className="bg-slate-50 border border-slate-150 rounded-2xl p-6 text-center text-slate-500 text-sm">
                  You haven't joined any schemes yet.{' '}
                  <button onClick={() => navigate('/member/plans')} className="text-corpBlue font-bold underline hover:text-blue-700">
                    Explore & Join Schemes →
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {myPlans.map((p) => (
                    <div 
                      key={p.plan_id} 
                      onClick={() => setActivePlanModal(p)}
                      className="border border-slate-200 hover:border-corpBlue rounded-2xl p-5 bg-slate-50/50 hover:bg-white transition-all cursor-pointer shadow-sm hover:shadow-md group flex flex-col md:flex-row items-start md:items-center justify-between gap-4"
                    >
                      <div>
                        <div className="flex items-center gap-2">
                          <h4 className="font-bold text-slate-900 text-lg group-hover:text-corpBlue transition-colors">{p.plan_name}</h4>
                          <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 uppercase border border-amber-200">
                            {p.chit_type === 'auction' ? 'Auction Scheme' : 'Lucky Draw'}
                          </span>
                        </div>
                        <p className="text-xs text-slate-500 mt-1">
                          Monthly Installment: <strong className="text-slate-900">₹{p.monthly_amount?.toLocaleString()}</strong> • Total Value: <strong className="text-slate-900">₹{p.total_value?.toLocaleString()}</strong>
                        </p>
                        <div className="flex items-center gap-2 mt-2">
                          <Ticket className="w-4 h-4 text-corpBlue" />
                          <span className="text-xs font-semibold text-slate-700">
                            Tickets: {p.tickets?.map(t => t.ticket_number || 'Pending').join(', ')}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="px-4 py-2.5 bg-corpBlue hover:bg-blue-900 text-white rounded-xl text-xs font-bold shadow-sm transition-all flex items-center gap-1.5">
                          View Schedule & Pay <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
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
                  <span className="text-lg font-bold text-slate-900">{myPlans.length} {myPlans.length === 1 ? 'Plan' : 'Plans'}</span>
                </div>
                <div className="bg-slate-50 rounded-xl p-3 border border-slate-100">
                  <span className="block text-xs text-slate-400">Total Saved</span>
                  <span className="text-lg font-bold text-slate-900">₹{myPlans.reduce((sum, p) => sum + (p.monthly_amount || 0), 0).toLocaleString()}</span>
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

          </div>

        </div>
      </div>

      {/* Scheme Schedule & Payment Modal */}
      {activePlanModal && (
        <div className="fixed inset-0 bg-slate-900/75 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl max-w-2xl w-full overflow-hidden shadow-2xl border border-slate-100 animate-fade-in-up font-sans flex flex-col max-h-[90vh]">
            
            {/* Modal Header */}
            <div className="bg-slate-900 p-6 text-white flex items-center justify-between relative">
              <div>
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-amber-400 block mb-1">
                  Scheme Timeline & Dues
                </span>
                <h3 className="font-extrabold text-xl">{activePlanModal.plan_name}</h3>
                <p className="text-xs text-slate-300 mt-0.5">
                  Monthly Installment: ₹{activePlanModal.monthly_amount?.toLocaleString()} • Duration: {activePlanModal.duration_months} Months
                </p>
              </div>
              <button 
                onClick={() => setActivePlanModal(null)}
                className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Schedule Content */}
            <div className="p-6 overflow-y-auto space-y-4">
              <div className="bg-blue-50 border border-blue-200 rounded-2xl p-4 text-xs text-blue-900 flex items-center justify-between">
                <div>
                  <span className="font-bold block text-sm">Current Active Month: Month 1</span>
                  <span className="text-blue-700">Only the current month's payment is unlocked. Future months are locked 🔒 until next draw.</span>
                </div>
                <button 
                  onClick={() => { setActivePlanModal(null); navigate('/member/payments'); }}
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-xl text-xs shadow-md flex-shrink-0"
                >
                  💳 Pay Month 1 Due (₹{activePlanModal.monthly_amount?.toLocaleString()})
                </button>
              </div>

              <div className="space-y-3">
                {activePlanModal.winners && activePlanModal.winners.map((w, idx) => {
                  const isCurrentActiveMonth = w.month_number === 1 && w.status !== 'completed';
                  const isFutureLockedMonth = w.month_number > 1 && w.status !== 'completed';

                  return (
                    <div 
                      key={idx} 
                      className={`p-4 rounded-2xl border flex items-center justify-between text-xs transition-all ${
                        isCurrentActiveMonth 
                          ? 'bg-emerald-50/70 border-emerald-300 shadow-sm' 
                          : isFutureLockedMonth 
                          ? 'bg-slate-100/60 border-slate-200 opacity-70'
                          : 'bg-amber-50/60 border-amber-200'
                      }`}
                    >
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <span className="font-bold text-sm text-slate-900">Month {w.month_number}</span>
                          {w.status === 'completed' ? (
                            <span className="bg-amber-200 text-amber-900 text-[10px] font-extrabold px-2 py-0.5 rounded uppercase">
                              WON ({w.draw_date})
                            </span>
                          ) : isCurrentActiveMonth ? (
                            <span className="bg-emerald-200 text-emerald-900 text-[10px] font-black px-2 py-0.5 rounded uppercase animate-pulse">
                              UNLOCKED • CURRENT DUE
                            </span>
                          ) : (
                            <span className="bg-slate-200 text-slate-600 text-[10px] font-bold px-2 py-0.5 rounded uppercase flex items-center gap-1">
                              <Lock className="w-3 h-3" /> LOCKED (Unlocks Next Month)
                            </span>
                          )}
                        </div>

                        <span className="block text-slate-600 font-medium">
                          {w.status === 'completed' ? `Winner: ${w.winner_name}` : isCurrentActiveMonth ? 'Installment Due Status: PENDING' : 'Future Monthly Draw'}
                        </span>
                      </div>

                      <div className="text-right">
                        {isCurrentActiveMonth ? (
                          <button 
                            onClick={() => { setActivePlanModal(null); navigate('/member/payments'); }}
                            className="px-4 py-2 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 text-white font-bold rounded-xl text-xs shadow-md transition-all flex items-center gap-1"
                          >
                            <CreditCard className="w-3.5 h-3.5" /> Pay Due (₹{activePlanModal.monthly_amount?.toLocaleString()})
                          </button>
                        ) : isFutureLockedMonth ? (
                          <div className="text-slate-400 font-semibold flex items-center gap-1 justify-end">
                            <Lock className="w-3.5 h-3.5" /> <span>Locked</span>
                          </div>
                        ) : (
                          <span className="font-extrabold text-emerald-700 text-sm">
                            Prize: ₹{w.prize_amount?.toLocaleString()}
                          </span>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Modal Footer */}
            <div className="p-4 bg-slate-50 border-t border-slate-200 text-right">
              <button 
                onClick={() => setActivePlanModal(null)}
                className="px-6 py-2.5 bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold rounded-xl text-xs transition-colors"
              >
                Close Schedule
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};

export default MemberDashboard;
"""

open('src/pages/member/Dashboard.jsx', 'w', encoding='utf-8').write(content)
print("MemberDashboard updated with clean scheme card view, modal schedule, current month payment unlock & locked future months!")

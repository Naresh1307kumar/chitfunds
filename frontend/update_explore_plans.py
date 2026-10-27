new_content = """import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import { ArrowLeft, ShieldCheck, Plus, Users, CalendarDays, ArrowRight, CheckCircle2 } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../../services/api';
import { useAuth } from '../../context/AuthContext';

const ExplorePlans = () => {
  const navigate = useNavigate();
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [joining, setJoining] = useState(null);
  const [ticketCounts, setTicketCounts] = useState({});
  const { user } = useAuth();

  // Reason modal states for Auction plans
  const [showReasonModal, setShowReasonModal] = useState(false);
  const [selectedPlanForReason, setSelectedPlanForReason] = useState(null);
  const [joiningReason, setJoiningReason] = useState('personal');

  const fetchPlans = async () => {
    try {
      const res = await api.get('/api/v1/member/plans');
      setPlans(res.data);
    } catch (error) {
      toast.error('Failed to load available plans');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user?.status === 'active') {
      fetchPlans();
    } else {
      setLoading(false);
    }
  }, [user]);

  const handleJoin = async (plan) => {
    // If it's an auction plan and the reason modal is not open yet, open it first!
    if (plan.chit_type === 'auction' && !showReasonModal) {
      setSelectedPlanForReason(plan);
      setJoiningReason('personal');
      setShowReasonModal(true);
      return;
    }

    const ticketCount = ticketCounts[plan.id] || 1;
    
    // Check if adding this many tickets exceeds total members
    if (plan.current_members + ticketCount > plan.total_members) {
      toast.error(`Cannot buy ${ticketCount} tickets. Only ${plan.total_members - plan.current_members} spots left.`);
      return;
    }

    setJoining(plan.id);
    try {
      const payload = { ticket_count: ticketCount };
      if (plan.chit_type === 'auction') {
        payload.reason = joiningReason;
      }
      const res = await api.post(`/api/v1/member/plans/${plan.id}/join`, payload);
      toast.success(res.data.message);
      setShowReasonModal(false);
      setSelectedPlanForReason(null);
      fetchPlans(); // Refresh to update members count
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to join plan');
    } finally {
      setJoining(null);
    }
  };

  const handleTicketCountChange = (planId, delta, maxAvailable) => {
    setTicketCounts(prev => {
      const current = prev[planId] || 1;
      const newValue = Math.max(1, Math.min(maxAvailable, current + delta));
      return { ...prev, [planId]: newValue };
    });
  };

  if (user?.status !== 'active') {
    return (
      <div className="max-w-4xl mx-auto px-6 py-20 text-center">
        <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-10 max-w-lg mx-auto shadow-sm">
          <ShieldCheck className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Verification Required</h2>
          <p className="text-gray-600 mb-6">
            You must complete your KYC verification and be approved by an administrator before you can join chit plans.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      <div className="flex items-center gap-4 mb-8">
        <button 
          onClick={() => navigate('/member/dashboard')}
          className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
          title="Go Back"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Explore Schemes</h1>
          <p className="text-gray-500 mt-1">Discover and join secure chit fund schemes that suit your financial goals.</p>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-10 text-slate-500 font-medium">Loading available plans...</div>
      ) : plans.length === 0 ? (
        <div className="bg-white border rounded-2xl p-10 text-center text-gray-500 shadow-sm">
          No new plans available to join right now. Please check back later!
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {plans.map(plan => (
            <div key={plan.id} className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all group flex flex-col">
              {/* Header */}
              <div className={`p-6 ${
                  plan.plan_type === 'gold' ? 'bg-gradient-to-br from-yellow-50 to-yellow-100/50 border-b border-yellow-100' :
                  plan.plan_type === 'silver' ? 'bg-gradient-to-br from-gray-50 to-slate-100 border-b border-gray-100' :
                  'bg-gradient-to-br from-orange-50 to-orange-100/50 border-b border-orange-100'
                }`}>
                <div className="flex justify-between items-start mb-2">
                  <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                    plan.plan_type === 'gold' ? 'bg-yellow-200 text-yellow-800' :
                    plan.plan_type === 'silver' ? 'bg-slate-200 text-slate-800' :
                    'bg-orange-200 text-orange-800'
                  }`}>
                    {plan.plan_type} Tier
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider bg-blue-50 text-blue-600 border border-blue-200">
                    {plan.chit_type === 'auction' ? 'Auction' : 'Lucky Draw'}
                  </span>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-1">{plan.plan_name}</h3>
                <p className="text-sm font-medium text-gray-500">₹{plan.total_value.toLocaleString()} Total Value</p>
              </div>

              {/* Body */}
              <div className="p-6 flex-1 flex flex-col">
                <div className="grid grid-cols-2 gap-4 mb-6">
                  <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
                    <p className="text-xs text-gray-500 mb-1">Monthly Amt</p>
                    <p className="font-bold text-gray-900">₹{plan.monthly_amount.toLocaleString()}</p>
                  </div>
                  <div className="bg-gray-50 p-3 rounded-xl border border-gray-100">
                    <p className="text-xs text-gray-500 mb-1">Duration</p>
                    <p className="font-bold text-gray-900">{plan.duration_months} Months</p>
                  </div>
                </div>

                <div className="space-y-3 mb-8 flex-1">
                  <div className="flex items-center gap-3 text-sm text-gray-600">
                    <Users className="w-5 h-5 text-blue-500" />
                    <span><strong className="text-gray-900">{plan.current_members} / {plan.total_members}</strong> Members Joined</span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-gray-600">
                    <CalendarDays className="w-5 h-5 text-blue-500" />
                    <span>Starts: <strong className="text-gray-900">{new Date(plan.start_date).toLocaleDateString()}</strong></span>
                  </div>
                  <div className="flex items-center gap-3 text-sm text-gray-600">
                    <CheckCircle2 className="w-5 h-5 text-green-500" />
                    <span>{plan.commission_rate}% Platform Commission</span>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="mb-6">
                  <div className="flex justify-between text-xs font-semibold mb-1.5">
                    <span className="text-blue-600">Filling Fast</span>
                    <span className="text-gray-500">{Math.round((plan.current_members / plan.total_members) * 100)}% Full</span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2 overflow-hidden">
                    <div 
                      className="bg-blue-600 h-2 rounded-full transition-all duration-1000" 
                      style={{ width: `${(plan.current_members / plan.total_members) * 100}%` }}
                    ></div>
                  </div>
                </div>

                {/* Ticket Selection */}
                <div className="mb-6 flex items-center justify-between bg-blue-50 p-3 rounded-xl border border-blue-100">
                  <div className="text-sm font-semibold text-blue-900">Tickets Needed:</div>
                  <div className="flex items-center gap-3">
                    <button 
                      onClick={() => handleTicketCountChange(plan.id, -1, plan.total_members - plan.current_members)}
                      className="w-8 h-8 rounded-full bg-white border border-blue-200 text-blue-600 flex items-center justify-center font-bold hover:bg-blue-100 disabled:opacity-50"
                      disabled={(ticketCounts[plan.id] || 1) <= 1}
                    >-</button>
                    <span className="font-bold text-lg w-4 text-center">{ticketCounts[plan.id] || 1}</span>
                    <button 
                      onClick={() => handleTicketCountChange(plan.id, 1, plan.total_members - plan.current_members)}
                      className="w-8 h-8 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold hover:bg-blue-700 disabled:opacity-50"
                      disabled={(ticketCounts[plan.id] || 1) >= (plan.total_members - plan.current_members)}
                    >+</button>
                  </div>
                </div>

                <button 
                  onClick={() => handleJoin(plan)}
                  disabled={joining === plan.id || plan.current_members === plan.total_members}
                  className="w-full py-3.5 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 transition-all shadow-md hover:shadow-lg flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed group-hover:scale-[1.02]"
                >
                  {joining === plan.id ? 'Requesting...' : 'Request to Join'} <ArrowRight className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Priority Reason Modal for Auction Plans */}
      {showReasonModal && selectedPlanForReason && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4">
          <div className="bg-white rounded-2xl w-full max-w-md overflow-hidden shadow-2xl p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-2">Priority Reason</h3>
            <p className="text-sm text-gray-500 mb-4">
              Since this is an Auction (Yela) plan, please specify your reason for joining. The system will use this to prioritize draw selections during emergencies.
            </p>
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-gray-600 mb-1 uppercase tracking-wider">Select Reason</label>
                <select 
                  value={joiningReason} 
                  onChange={(e) => setJoiningReason(e.target.value)} 
                  className="w-full px-4 py-2.5 border rounded-xl bg-white focus:ring-2 focus:ring-blue-500 outline-none"
                >
                  <option value="hospital">Hospital / Medical Emergency (Priority 1)</option>
                  <option value="education">Education / College Fees (Priority 2)</option>
                  <option value="marriage">Marriage / Family Event (Priority 3)</option>
                  <option value="business">Business Expansion (Priority 4)</option>
                  <option value="personal">Personal / Savings (Priority 5)</option>
                </select>
              </div>
              <div className="flex gap-3 pt-2">
                <button 
                  onClick={() => { setShowReasonModal(false); setSelectedPlanForReason(null); }} 
                  className="flex-1 py-2.5 border border-gray-300 rounded-xl font-semibold text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button 
                  onClick={() => handleJoin(selectedPlanForReason)}
                  disabled={joining === selectedPlanForReason.id}
                  className="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-semibold transition-colors"
                >
                  {joining === selectedPlanForReason.id ? 'Submitting...' : 'Join Plan'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExplorePlans;
"""

open('src/pages/member/ExplorePlans.jsx', 'w', encoding='utf-8').write(new_content)
print('ExplorePlans updated successfully!')

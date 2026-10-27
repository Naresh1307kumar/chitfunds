content = """import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect, useRef } from 'react';
import { ArrowLeft, ShieldCheck, Plus, Users, CalendarDays, ArrowRight, CheckCircle2, ChevronLeft, ChevronRight, Coins } from 'lucide-react';
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
  const scrollRef = useRef(null);

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

  const scroll = (direction) => {
    if (scrollRef.current) {
      const { scrollLeft, clientWidth } = scrollRef.current;
      const scrollAmount = clientWidth * 0.8;
      scrollRef.current.scrollTo({
        left: direction === 'left' ? scrollLeft - scrollAmount : scrollLeft + scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  const handleJoin = async (plan) => {
    if (!showReasonModal) {
      setSelectedPlanForReason(plan);
      setJoiningReason('personal');
      setShowReasonModal(true);
      return;
    }

    const ticketCount = ticketCounts[plan.id] || 1;
    
    if (plan.current_members + ticketCount > plan.total_members) {
      toast.error(`Cannot buy ${ticketCount} tickets. Only ${plan.total_members - plan.current_members} spots left.`);
      return;
    }

    setJoining(plan.id);
    try {
      const payload = { ticket_count: ticketCount, reason: joiningReason };
      const res = await api.post(`/api/v1/member/plans/${plan.id}/join`, payload);
      toast.success(res.data.message);
      setShowReasonModal(false);
      setSelectedPlanForReason(null);
      fetchPlans();
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
      <div className="flex items-center justify-between mb-8">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Explore Auction Schemes</h1>
            <p className="text-slate-500 text-sm mt-0.5">Scroll horizontally to explore our high-yield auction chit plans.</p>
          </div>
        </div>

        {/* Scroll Control Buttons */}
        <div className="flex items-center gap-2">
          <button 
            onClick={() => scroll('left')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-corpBlue bg-white hover:bg-blue-50 text-slate-600 hover:text-corpBlue flex items-center justify-center transition-all shadow-sm active:scale-95"
            title="Previous Plans"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <button 
            onClick={() => scroll('right')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-corpBlue bg-white hover:bg-blue-50 text-slate-600 hover:text-corpBlue flex items-center justify-center transition-all shadow-sm active:scale-95"
            title="Next Plans"
          >
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-10 text-slate-500 font-medium">Loading available plans...</div>
      ) : plans.length === 0 ? (
        <div className="bg-white border rounded-2xl p-10 text-center text-gray-500 shadow-sm">
          No new plans available to join right now. Please check back later!
        </div>
      ) : (
        <div 
          ref={scrollRef}
          className="flex gap-6 overflow-x-auto snap-x snap-mandatory scrollbar-none pb-8 pt-2 px-1 scroll-smooth"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {plans.map(plan => (
            <div 
              key={plan.id} 
              className="min-w-[320px] sm:min-w-[360px] max-w-[380px] flex-shrink-0 snap-start bg-white border border-gray-200 rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all group flex flex-col hover:-translate-y-1"
            >
              {/* Header */}
              <div className="p-6 bg-gradient-to-br from-amber-50 to-orange-50 border-b border-amber-100">
                <div className="flex justify-between items-start mb-2">
                  <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-amber-200 text-amber-900">
                    {plan.plan_type} Tier
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-amber-600 text-white flex items-center gap-1">
                    <Coins className="w-3 h-3" /> Auction Scheme
                  </span>
                </div>
                <h3 className="text-xl font-bold text-slate-900 mb-1">{plan.plan_name}</h3>
                <p className="text-sm font-semibold text-corpBlue">₹{plan.total_value.toLocaleString()} Total Pool</p>
              </div>

              {/* Body */}
              <div className="p-6 flex-1 flex flex-col">
                <div className="grid grid-cols-2 gap-3 mb-6">
                  <div className="bg-slate-50 p-3 rounded-2xl border border-slate-100">
                    <p className="text-xs text-slate-400 mb-0.5">Monthly Amt</p>
                    <p className="font-extrabold text-slate-900">₹{plan.monthly_amount.toLocaleString()}</p>
                  </div>
                  <div className="bg-slate-50 p-3 rounded-2xl border border-slate-100">
                    <p className="text-xs text-slate-400 mb-0.5">Duration</p>
                    <p className="font-extrabold text-slate-900">{plan.duration_months} Months</p>
                  </div>
                </div>

                <div className="space-y-3 mb-6 flex-1 text-xs">
                  <div className="flex items-center gap-3 text-slate-600">
                    <Users className="w-4 h-4 text-corpBlue" />
                    <span><strong className="text-slate-900">{plan.current_members} / {plan.total_members}</strong> Members Joined</span>
                  </div>
                  <div className="flex items-center gap-3 text-slate-600">
                    <CalendarDays className="w-4 h-4 text-corpBlue" />
                    <span>Starts: <strong className="text-slate-900">{new Date(plan.start_date).toLocaleDateString()}</strong></span>
                  </div>
                  <div className="flex items-center gap-3 text-slate-600">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    <span>{plan.commission_rate}% Platform Commission</span>
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="mb-6">
                  <div className="flex justify-between text-xs font-semibold mb-1.5">
                    <span className="text-corpBlue">Filling Fast</span>
                    <span className="text-slate-500">{Math.round((plan.current_members / plan.total_members) * 100)}% Full</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div 
                      className="bg-corpBlue h-2 rounded-full transition-all duration-1000" 
                      style={{ width: `${(plan.current_members / plan.total_members) * 100}%` }}
                    ></div>
                  </div>
                </div>

                {/* Ticket Selection & Join Button */}
                <div className="mb-4 flex items-center justify-between bg-slate-50 p-3 rounded-2xl border border-slate-200">
                  <div className="text-xs font-semibold text-slate-700">Tickets Needed:</div>
                  <div className="flex items-center gap-2">
                    <button 
                      onClick={() => handleTicketCountChange(plan.id, -1, plan.total_members - plan.current_members)}
                      className="w-7 h-7 rounded-lg bg-white border border-slate-200 flex items-center justify-center font-bold text-slate-700 hover:bg-slate-100 text-sm shadow-sm"
                    >
                      -
                    </button>
                    <span className="font-bold text-slate-900 text-sm w-4 text-center">
                      {ticketCounts[plan.id] || 1}
                    </span>
                    <button 
                      onClick={() => handleTicketCountChange(plan.id, 1, plan.total_members - plan.current_members)}
                      className="w-7 h-7 rounded-lg bg-white border border-slate-200 flex items-center justify-center font-bold text-slate-700 hover:bg-slate-100 text-sm shadow-sm"
                    >
                      +
                    </button>
                  </div>
                </div>

                <button
                  onClick={() => handleJoin(plan)}
                  disabled={joining === plan.id || plan.current_members >= plan.total_members}
                  className="w-full py-3 bg-gradient-to-r from-blue-600 to-corpBlue hover:from-blue-700 hover:to-blue-900 text-white font-bold text-sm rounded-2xl shadow-md transition-all flex items-center justify-center gap-2 disabled:opacity-50"
                >
                  {joining === plan.id ? 'Joining...' : (plan.current_members >= plan.total_members ? 'Plan Full' : 'Request to Join')}
                  <ArrowRight className="w-4 h-4" />
                </button>

              </div>
            </div>
          ))}
        </div>
      )}

      {/* Emergency Need Reason Selection Modal */}
      {showReasonModal && selectedPlanForReason && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl p-6 max-w-md w-full shadow-2xl border border-slate-100 animate-fade-in-up">
            <h3 className="text-xl font-bold text-slate-900 mb-2">Specify Emergency Reason</h3>
            <p className="text-slate-500 text-xs mb-4">
              Select your primary financial need for joining <strong>{selectedPlanForReason.plan_name}</strong>. This priority will determine your rank in monthly AI auction allocation!
            </p>
            <div className="space-y-3 mb-6 text-xs font-semibold">
              {[
                { value: 'hospital', label: '🏥 Hospital / Medical Emergency (Rank 1 - Highest)' },
                { value: 'education', label: '🎓 Higher Education / School Fees (Rank 2)' },
                { value: 'marriage', label: '💍 Marriage / Family Function (Rank 3)' },
                { value: 'business', label: '💼 Business Capital / Expansion (Rank 4)' },
                { value: 'personal', label: '👤 Personal Savings / Investment (Rank 5)' }
              ].map(opt => (
                <label key={opt.value} className={`flex items-center gap-3 p-3 rounded-2xl border cursor-pointer transition-all ${joiningReason === opt.value ? 'bg-blue-50 border-blue-500 text-blue-900 font-bold shadow-sm' : 'border-slate-200 text-slate-700 hover:bg-slate-50'}`}>
                  <input 
                    type="radio" 
                    name="reason" 
                    value={opt.value} 
                    checked={joiningReason === opt.value} 
                    onChange={(e) => setJoiningReason(e.target.value)} 
                    className="accent-corpBlue"
                  />
                  <span>{opt.label}</span>
                </label>
              ))}
            </div>
            <div className="flex gap-3">
              <button 
                onClick={() => setShowReasonModal(false)}
                className="flex-1 py-3 border border-slate-200 rounded-2xl text-slate-600 font-bold hover:bg-slate-50 text-xs"
              >
                Cancel
              </button>
              <button 
                onClick={() => handleJoin(selectedPlanForReason)}
                className="flex-1 py-3 bg-corpBlue text-white rounded-2xl font-bold hover:bg-blue-900 text-xs shadow-md"
              >
                Confirm & Join Plan
              </button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default ExplorePlans;
"""

open('src/pages/member/ExplorePlans.jsx', 'w', encoding='utf-8').write(content)
print("ExplorePlans.jsx updated cleanly to horizontal carousel!")

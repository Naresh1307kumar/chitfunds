content = """import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Trophy, Users, Dices, Coins, Sparkles, CheckCircle2, ShieldAlert } from 'lucide-react';
import toast from 'react-hot-toast';
import api from '../../services/api';
import confetti from 'canvas-confetti';
import { Wheel } from 'react-custom-roulette';

const ConductDraw = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [plan, setPlan] = useState(null);
  const [members, setMembers] = useState([]);
  const [draws, setDraws] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isDrawing, setIsDrawing] = useState(false);
  const [winnerData, setWinnerData] = useState(null);
  
  // Auction-specific form states
  const [selectedWinner, setSelectedWinner] = useState('');
  const [bidAmount, setBidAmount] = useState('');

  // Spinner states
  const [spinnerItems, setSpinnerItems] = useState([]);
  const [mustSpin, setMustSpin] = useState(false);
  const [prizeNumber, setPrizeNumber] = useState(0);
  const [rouletteData, setRouletteData] = useState([{ option: 'Ready to Spin' }]);

  const fetchData = async () => {
    try {
      const [planRes, membersRes, drawsRes] = await Promise.all([
        api.get(`/api/v1/admin/plans/${id}`),
        api.get(`/api/v1/admin/plans/${id}/members`),
        api.get(`/api/v1/admin/draws/${id}`)
      ]);
      setPlan(planRes.data);
      const activeMembers = membersRes.data.filter(m => m.status === 'active');
      setMembers(activeMembers);
      setDraws(drawsRes.data);
      
      // Initialize spinner items
      const eligible = activeMembers.filter(m => !m.has_won);
      if (eligible.length > 0) {
        setSpinnerItems(eligible);
        const colors = ['#1A2B49', '#FFD700', '#FF8C00', '#4F46E5', '#10B981'];
        const textColors = ['white', 'black', 'white', 'white', 'white'];
        const rData = eligible.map((m, i) => ({ 
           option: m.ticket_number, 
           style: { backgroundColor: colors[i % colors.length], textColor: textColors[i % textColors.length] } 
         }));
        setRouletteData(rData.length > 1 ? rData : [...rData, ...rData]); 
      } else {
        setRouletteData([{ option: 'Finished' }]);
      }
    } catch (err) {
      toast.error('Failed to load draw data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [id]);

  const handleConductDraw = async () => {
    const eligibleMembers = members.filter(m => !m.has_won);
    if (eligibleMembers.length === 0) {
      toast.error('No eligible tickets left for the draw');
      return;
    }

    setIsDrawing(true);
    setWinnerData(null);

    try {
      let res;
      if (plan?.chit_type === 'auction') {
        const payload = {};
        if (selectedWinner) payload.winner_ticket_id = Number(selectedWinner);
        if (bidAmount && !isNaN(bidAmount) && Number(bidAmount) > 0) payload.winning_bid_amount = Number(bidAmount);

        res = await api.post(`/api/v1/admin/draws/${id}/conduct`, payload);

        setIsDrawing(false);
        setWinnerData(res.data);
        confetti({
          particleCount: 150,
          spread: 70,
          origin: { y: 0.6 },
          colors: ['#FFD700', '#FFA500', '#1A2B49']
        });
        setSelectedWinner('');
        setBidAmount('');
        fetchData();
      } else {
        // Standard lucky draw
        res = await api.post(`/api/v1/admin/draws/${id}/conduct`);
        const winnerTicket = res.data.ticket_number;
        let targetIndex = spinnerItems.findIndex(m => m.ticket_number === winnerTicket);
        if (targetIndex === -1) targetIndex = 0;
        
        setPrizeNumber(targetIndex);
        setMustSpin(true);
        setWinnerData(res.data);
      }
    } catch (err) {
      setIsDrawing(false);
      setMustSpin(false);
      toast.error(err.response?.data?.detail || 'Failed to conduct draw');
    }
  };

  const getPriorityBadge = (prio) => {
    const badges = {
      1: { text: 'Hospital 🏥 (Rank 1)', bg: 'bg-red-50 text-red-700 border-red-200' },
      2: { text: 'Education 🎓 (Rank 2)', bg: 'bg-blue-50 text-blue-700 border-blue-200' },
      3: { text: 'Marriage 💍 (Rank 3)', bg: 'bg-amber-50 text-amber-700 border-amber-200' },
      4: { text: 'Business 💼 (Rank 4)', bg: 'bg-purple-50 text-purple-700 border-purple-200' },
      5: { text: 'Personal 👤 (Rank 5)', bg: 'bg-slate-100 text-slate-700 border-slate-200' },
    };
    return badges[prio] || badges[5];
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-10 font-sans">
      <div className="flex items-center gap-4 mb-8">
        <button 
          onClick={() => navigate('/admin/plans')}
          className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-300 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
          title="Go Back"
        >
          <ArrowLeft className="w-5 h-5" />
        </button>
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Conduct Monthly Draw</h1>
          <p className="text-slate-500 text-sm">Plan: <span className="font-semibold text-slate-700">{plan?.plan_name}</span> (Month {draws.length + 1} of {plan?.duration_months})</p>
        </div>
      </div>

      {loading ? (
        <div className="text-center py-20 text-slate-400 font-medium">Loading draw system...</div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
          
          {/* Main Action Column */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Conduct Draw Card */}
            <div className="bg-white border border-slate-200/80 rounded-3xl p-8 shadow-sm text-center flex flex-col items-center">
              <h2 className="text-2xl font-bold text-slate-900 mb-2">
                {plan?.chit_type === 'auction' ? 'Auction Winner Selection' : 'Conduct Next Draw'}
              </h2>
              <p className="text-slate-500 text-sm mb-6 max-w-md">
                {plan?.chit_type === 'auction' 
                  ? 'Click "Select Winner" below and the AI engine will automatically choose the winner based on emergency priority ranks.'
                  : 'The system will pick a random winner securely from active tickets.'}
              </p>

              {plan?.chit_type === 'auction' ? (
                <div className="w-full max-w-xl space-y-4 mb-6">
                  {/* Optional Override Selector */}
                  <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5 text-left">
                    <label className="block text-xs font-bold text-slate-700 mb-1.5 uppercase tracking-wider">
                      WINNING BID DISCOUNT (₹) <span className="font-normal text-slate-400">(Optional)</span>
                    </label>
                    <input 
                      type="number" 
                      placeholder="e.g. 2500 (Default: 5% Commission)" 
                      value={bidAmount} 
                      onChange={(e) => setBidAmount(e.target.value)} 
                      className="w-full px-4 py-2.5 border border-slate-200 rounded-xl outline-none focus:ring-2 focus:ring-corpBlue bg-white font-bold text-slate-900 text-sm"
                    />
                  </div>
                </div>
              ) : (
                <div className="w-full flex justify-center mb-8" style={{ minHeight: '300px' }}>
                    <Wheel
                      mustStartSpinning={mustSpin}
                      prizeNumber={prizeNumber}
                      data={rouletteData}
                      outerBorderColor="#1A2B49"
                      outerBorderWidth={5}
                      innerBorderColor="#FFD700"
                      innerBorderWidth={3}
                      radiusLineColor="#FFD700"
                      radiusLineWidth={1}
                      textColors={['#ffffff']}
                      fontSize={14}
                      spinDuration={0.8}
                      onStopSpinning={() => {
                        setMustSpin(false);
                        setIsDrawing(false);
                        if (winnerData) {
                            confetti({
                              particleCount: 150,
                              spread: 70,
                              origin: { y: 0.6 },
                              colors: ['#FFD700', '#FFA500', '#1A2B49']
                            });
                            fetchData();
                        }
                      }}
                    />
                </div>
              )}

              {members.length > 0 && members.filter(m => !m.has_won).length === 0 ? (
                <div className="w-full bg-blue-50 border border-blue-200 text-blue-800 px-6 py-4 rounded-xl flex items-center justify-center gap-3">
                  <Trophy className="w-6 h-6 text-blue-500" />
                  <span className="font-bold text-lg">All Draws Completed for this Plan!</span>
                </div>
              ) : (
                <button 
                  onClick={handleConductDraw}
                  disabled={isDrawing || members.filter(m => !m.has_won).length === 0}
                  className="px-10 py-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-corpBlue text-white font-bold text-lg rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  <Sparkles className="w-5 h-5 text-amber-300 animate-pulse" />
                  {isDrawing ? 'Processing Winner Selection...' : (plan?.chit_type === 'auction' ? 'SELECT WINNER & CONDUCT DRAW' : 'SPIN THE WHEEL')}
                </button>
              )}

              {winnerData && !isDrawing && (
                <div className="mt-6 bg-emerald-50 border border-emerald-200 text-emerald-900 px-6 py-4 rounded-2xl w-full text-left flex items-start gap-4 animate-fade-in-up">
                  <Trophy className="w-8 h-8 text-emerald-600 flex-shrink-0 mt-0.5" />
                  <div>
                    <h4 className="font-bold text-base text-emerald-950">Month {winnerData.month_number} Winner Announced! 🎉</h4>
                    <p className="text-sm mt-1 text-emerald-900">
                      Winner: <strong>{winnerData.winner_name} ({winnerData.ticket_number})</strong>
                    </p>
                    <p className="text-sm mt-0.5 text-emerald-900">
                      Prize Payout: <strong>₹{winnerData.prize_amount?.toLocaleString()}</strong>
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Enrolled Members & Emergency Needs Table */}
            {plan?.chit_type === 'auction' && (
              <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
                <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-100">
                  <div>
                    <h3 className="font-bold text-base text-slate-900">Enrolled Members & Emergency Needs</h3>
                    <p className="text-xs text-slate-500">Live priority ranking for winner allocation</p>
                  </div>
                  <span className="text-xs font-bold bg-slate-100 text-slate-700 px-3 py-1 rounded-full">
                    {members.filter(m => !m.has_won).length} Candidates Remaining
                  </span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse text-xs">
                    <thead>
                      <tr className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                        <th className="py-3 px-4">Ticket #</th>
                        <th className="py-3 px-4">Member Name</th>
                        <th className="py-3 px-4">Emergency Need / Reason</th>
                        <th className="py-3 px-4 text-center">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {members.map((m) => {
                        const badge = getPriorityBadge(m.priority_score || 5);
                        return (
                          <tr key={m.plan_member_id} className={`hover:bg-slate-50/80 ${m.has_won ? 'opacity-50 bg-slate-50/50' : ''}`}>
                            <td className="py-3 px-4 font-bold text-slate-900">{m.ticket_number}</td>
                            <td className="py-3 px-4 font-semibold text-slate-800">{m.name}</td>
                            <td className="py-3 px-4">
                              <span className={`inline-block px-2.5 py-1 rounded-lg text-[11px] font-bold border ${badge.bg}`}>
                                {badge.text}
                              </span>
                            </td>
                            <td className="py-3 px-4 text-center">
                              {m.has_won ? (
                                <span className="inline-flex items-center gap-1 text-emerald-600 font-bold bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200 text-[10px]">
                                  <CheckCircle2 className="w-3 h-3" /> Won
                                </span>
                              ) : (
                                <span className="text-blue-600 font-semibold bg-blue-50 px-2.5 py-0.5 rounded-full border border-blue-200 text-[10px]">
                                  Eligible Candidate
                                </span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

          </div>

          {/* Draw History Sidebar */}
          <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
            <h3 className="font-bold text-lg text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center justify-between">
              <span>Completed Draws</span>
              <span className="text-xs bg-slate-100 text-slate-600 px-2.5 py-1 rounded-full font-semibold">{draws.length} / {plan?.duration_months}</span>
            </h3>

            {draws.length === 0 ? (
              <div className="text-center py-10 text-slate-400 text-sm italic">
                No monthly draws conducted yet.
              </div>
            ) : (
              <div className="space-y-4">
                {draws.map(d => (
                  <div key={d.id} className="border border-slate-150 rounded-2xl p-4 bg-slate-50/50">
                    <div className="flex justify-between items-start mb-2">
                      <span className="font-bold text-slate-900 text-sm">Month {d.month_number}</span>
                      <span className="text-xs text-slate-500">{d.draw_date}</span>
                    </div>
                    <div className="text-xs space-y-1">
                      <p className="text-slate-600">Winner: <span className="font-bold text-slate-900">{d.winner_name}</span></p>
                      <p className="text-slate-600">Ticket: <span className="font-semibold text-slate-700">{d.ticket_number}</span></p>
                      <p className="text-emerald-600 font-bold mt-2">Payout: ₹{d.prize_amount?.toLocaleString()}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>
      )}
    </div>
  );
};

export default ConductDraw;
"""

open('src/pages/admin/ConductDraw.jsx', 'w', encoding='utf-8').write(content)
print("ConductDraw updated cleanly!")

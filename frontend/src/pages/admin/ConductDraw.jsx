import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { ArrowLeft, Trophy, Users, Dices, Coins } from 'lucide-react';
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
  
  // Spinner states
  const [spinnerItems, setSpinnerItems] = useState([]);
  const [mustSpin, setMustSpin] = useState(false);
  const [prizeNumber, setPrizeNumber] = useState(0);
  const [rouletteData, setRouletteData] = useState([{ option: 'Ready to Spin' }]);

  const fetchData = async () => {
    try {
      const [membersRes, drawsRes] = await Promise.all([
        api.get(`/api/v1/admin/plans/${id}/members`),
        api.get(`/api/v1/admin/draws/${id}`)
      ]);
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
        // Roulette needs at least 2 items to spin visually well
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
      const res = await api.post(`/api/v1/admin/draws/${id}/conduct`);
      
      // Find the winner's ticket in the eligible list
      const winnerTicket = res.data.ticket_number;
      
      // For rouletteData matching
      let targetIndex = spinnerItems.findIndex(m => m.ticket_number === winnerTicket);
      if (targetIndex === -1) targetIndex = 0;
      
      // If we duplicated the array for length < 2, the index is the same.
      setPrizeNumber(targetIndex);
      setMustSpin(true);
      
      // We store the res.data so we can show it when it stops
      setWinnerData(res.data);
      
    } catch (err) {
      setIsDrawing(false);
      setMustSpin(false);
      toast.error(err.response?.data?.detail || 'Failed to conduct draw');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      <div className="flex items-center gap-4 mb-8">
        <button 
          onClick={() => navigate('/admin/plans')}
          className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
          title="Go Back"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Monthly Draw</h1>
          <p className="text-gray-500 mt-1">Conduct the lottery draw for this plan</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Draw Section */}
        <div className="bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100 flex flex-col items-center p-10 text-center relative">
          <div className="absolute top-0 right-0 w-64 h-64 bg-blue-50 rounded-full blur-3xl opacity-50 -translate-y-1/2 translate-x-1/2"></div>
          <div className="absolute bottom-0 left-0 w-64 h-64 bg-yellow-50 rounded-full blur-3xl opacity-50 translate-y-1/2 -translate-x-1/2"></div>

          <div className="relative z-10 w-full flex flex-col items-center">
            <div className="w-24 h-24 rounded-full bg-gradient-to-br from-blue-600 to-indigo-800 flex items-center justify-center shadow-lg mb-6">
              <Dices className="w-12 h-12 text-white" />
            </div>
            
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Conduct Next Draw</h2>
            <p className="text-gray-500 mb-8 max-w-sm">The system will securely pick a random winner from the active tickets.</p>

            {/* Spinner Window */}
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

            {members.length > 0 && members.filter(m => !m.has_won).length === 0 ? (
              <div className="w-full bg-blue-50 border border-blue-200 text-blue-800 px-6 py-4 rounded-xl flex items-center justify-center gap-3 mt-2">
                <Trophy className="w-6 h-6 text-blue-500" />
                <span className="font-bold text-lg">All Draws Finished for this Plan!</span>
              </div>
            ) : (
              <button 
                onClick={handleConductDraw}
                disabled={isDrawing || members.filter(m => !m.has_won).length === 0}
                className="px-10 py-4 bg-gradient-to-r from-yellow-500 to-orange-500 text-white font-bold text-xl rounded-full shadow-[0_0_20px_rgba(245,158,11,0.4)] hover:shadow-[0_0_30px_rgba(245,158,11,0.6)] transition-all transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:translate-y-0"
              >
                {isDrawing ? 'Spinning...' : 'SPIN THE WHEEL'}
              </button>
            )}

            {winnerData && !isDrawing && (
              <div className="mt-8 bg-green-50 border border-green-200 text-green-800 px-6 py-4 rounded-xl w-full text-left flex items-start gap-4">
                <Trophy className="w-8 h-8 text-green-500 flex-shrink-0" />
                <div>
                  <h4 className="font-bold">Draw Completed Successfully!</h4>
                  <p className="text-sm opacity-90 mt-1">Prize amount: <strong>₹{winnerData.prize_amount?.toLocaleString()}</strong></p>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* History Section */}
        <div className="bg-white rounded-3xl shadow-sm border border-gray-100 p-8 flex flex-col">
          <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
            <Trophy className="w-5 h-5 text-yellow-500" /> Draw History
          </h3>
          
          <div className="flex-1 overflow-y-auto">
            {draws.length === 0 ? (
              <div className="text-center text-gray-500 py-10 bg-gray-50 rounded-xl">No draws conducted yet.</div>
            ) : (
              <div className="space-y-4">
                {draws.map(draw => (
                  <div key={draw.id} className="p-4 rounded-xl border border-gray-100 flex justify-between items-center bg-gray-50/50 hover:bg-white transition-colors">
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 rounded-lg bg-blue-100 text-blue-700 font-bold flex items-center justify-center">
                        M{draw.month_number}
                      </div>
                      <div>
                        <p className="font-bold text-gray-900">{draw.winner_name || 'Pending'}</p>
                        <p className="text-xs text-gray-500 font-mono">{draw.ticket_number || '-'}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-green-600">₹{draw.prize_amount?.toLocaleString()}</p>
                      <p className="text-xs text-gray-400">{new Date(draw.draw_date).toLocaleDateString()}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConductDraw;

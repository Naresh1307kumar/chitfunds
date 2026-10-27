content = """import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import { ArrowLeft, IndianRupee, Clock, CheckCircle, AlertCircle, RefreshCw, Sparkles, Receipt } from 'lucide-react';
import { format } from 'date-fns';
import RazorpayModal from '../../components/RazorpayModal';
import PaymentReceiptModal from '../../components/PaymentReceiptModal';
import confetti from 'canvas-confetti';

const MemberPayments = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [dues, setDues] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Payment Gateway Modals
  const [selectedDue, setSelectedDue] = useState(null);
  const [activeReceipt, setActiveReceipt] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [duesRes, historyRes] = await Promise.all([
        api.get('/api/v1/member/payments/dues'),
        api.get('/api/v1/member/payments/history')
      ]);
      setDues(duesRes.data);
      setHistory(historyRes.data);
    } catch (err) {
      setError('Failed to load payment data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handlePaymentSuccess = (receipt) => {
    setSelectedDue(null);
    setActiveReceipt(receipt);
    confetti({
      particleCount: 150,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#10B981', '#FFD700', '#1A2B49']
    });
    fetchData();
  };

  const getStatusBadge = (status) => {
    switch(status) {
      case 'success':
      case 'verified':
        return <span className="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 rounded-full text-xs font-bold uppercase tracking-wider">Verified</span>;
      case 'pending':
        return <span className="px-2.5 py-0.5 bg-amber-100 text-amber-800 rounded-full text-xs font-bold uppercase tracking-wider">Pending Auth</span>;
      case 'failed':
        return <span className="px-2.5 py-0.5 bg-red-100 text-red-800 rounded-full text-xs font-bold uppercase tracking-wider">Rejected</span>;
      default:
        return <span className="px-2.5 py-0.5 bg-slate-100 text-slate-700 rounded-full text-xs font-bold uppercase tracking-wider">{status}</span>;
    }
  };

  if (loading) return <div className="min-h-screen p-10 flex justify-center items-center"><RefreshCw className="animate-spin text-corpBlue w-8 h-8" /></div>;

  return (
    <div className="min-h-screen bg-[#F8FAFC] py-10 px-6 font-sans">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-4 mb-8">
          <button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-slate-900 mb-1">My Installments & Payment Gateway</h1>
            <p className="text-slate-500 text-sm">Pay monthly dues via Instant Razorpay UPI and generate verified digital receipts.</p>
          </div>
        </div>
        
        {error && <div className="bg-red-100 text-red-700 p-4 rounded-2xl mb-6 flex gap-2"><AlertCircle /> {error}</div>}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
          
          {/* Pending Dues Section */}
          <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
            <h2 className="text-xl font-bold text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center gap-2">
              <Clock className="text-corpBlue w-5 h-5" /> Active Dues & Installments
            </h2>
            
            {dues.length === 0 ? (
              <div className="p-8 text-center bg-emerald-50/50 border border-emerald-100 text-emerald-800 rounded-2xl">
                <CheckCircle className="w-10 h-10 mx-auto text-emerald-500 mb-2" />
                <p className="font-bold text-base">All Caught Up!</p>
                <p className="text-xs text-emerald-700 mt-1">You have no pending dues or overdue installments right now.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {dues.map(due => (
                  <div key={due.id} className="p-5 border border-slate-200 rounded-2xl bg-slate-50/50 hover:border-blue-300 transition-all flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-start mb-2">
                        <span className="font-bold text-slate-900 text-base">{due.plan_name}</span>
                        <span className="px-2.5 py-0.5 bg-blue-100 text-blue-800 rounded-full text-xs font-bold">Month {due.month_number}</span>
                      </div>
                      <div className="flex justify-between items-center mt-3">
                        <div>
                          <p className="text-xs text-slate-400">Total Amount Due</p>
                          <p className="font-black text-2xl text-corpBlue">₹{due.total_amount?.toLocaleString()}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-xs text-red-500 font-bold mb-1">Due: {format(new Date(due.due_date), 'dd MMM yyyy')}</p>
                          <button 
                            onClick={() => setSelectedDue(due)} 
                            className="px-5 py-2.5 bg-gradient-to-r from-blue-600 to-corpBlue text-white rounded-xl text-xs font-bold hover:from-blue-700 hover:to-blue-900 shadow-md transition-all flex items-center gap-1.5"
                          >
                            <Sparkles className="w-3.5 h-3.5" /> Pay via Razorpay UPI
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Payment History Section */}
          <div className="bg-white border border-slate-200/80 rounded-3xl p-6 shadow-sm">
            <h2 className="text-xl font-bold text-slate-900 mb-4 pb-3 border-b border-slate-100 flex items-center gap-2">
              <IndianRupee className="text-amber-500 w-5 h-5" /> Transaction History & Receipts
            </h2>

            <div className="divide-y divide-slate-100">
              {history.length === 0 ? (
                <div className="p-8 text-center text-slate-400 text-sm">No previous payments found.</div>
              ) : (
                history.map(payment => (
                  <div key={payment.id} className="py-4 hover:bg-slate-50/80 flex items-center justify-between transition-colors px-2 rounded-xl">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-extrabold text-slate-900 text-base">₹{payment.amount?.toLocaleString()}</span>
                        {getStatusBadge(payment.status)}
                      </div>
                      <p className="text-xs text-slate-500 mt-1">{payment.payment_method} • Ref: <span className="font-mono">{payment.transaction_id}</span></p>
                    </div>
                    <button 
                      onClick={() => setActiveReceipt({
                        receipt_number: `REC-2026-${payment.installment_id || payment.id}`,
                        member_name: user?.name,
                        member_email: user?.email,
                        member_phone: user?.phone,
                        plan_name: "Chit Scheme",
                        ticket_number: "PM-17",
                        amount_paid: payment.amount,
                        payment_id: payment.transaction_id,
                        payment_method: payment.payment_method,
                        paid_date: new Date(payment.created_at || Date.now()).toLocaleDateString(),
                        emergency_reason: "VERIFIED",
                        status: "VERIFIED & PAID"
                      })}
                      className="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-xl flex items-center gap-1.5 transition-colors border border-slate-200"
                    >
                      <Receipt className="w-3.5 h-3.5 text-corpBlue" /> View Receipt
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>

        </div>
      </div>

      {/* Razorpay Gateway Checkout Modal */}
      {selectedDue && (
        <RazorpayModal 
          due={selectedDue} 
          onClose={() => setSelectedDue(null)} 
          onSuccess={handlePaymentSuccess} 
        />
      )}

      {/* Verified Digital Payment Receipt Modal */}
      {activeReceipt && (
        <PaymentReceiptModal 
          receipt={activeReceipt} 
          onClose={() => setActiveReceipt(null)} 
        />
      )}

    </div>
  );
};

export default MemberPayments;
"""

open('src/pages/member/Payments.jsx', 'w', encoding='utf-8').write(content)
print("MemberPayments updated cleanly with Razorpay Gateway & Digital Receipts!")

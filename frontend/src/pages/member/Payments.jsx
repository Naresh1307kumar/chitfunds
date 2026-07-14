import { useNavigate } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';
import { ArrowLeft, IndianRupee, Clock, CheckCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { format } from 'date-fns';

const MemberPayments = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [dues, setDues] = useState([]);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Payment Form State
  const [selectedDue, setSelectedDue] = useState(null);
  const [paymentMethod, setPaymentMethod] = useState('UPI');
  const [transactionId, setTransactionId] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

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

  const handlePay = async (e) => {
    e.preventDefault();
    if (!selectedDue || !transactionId) return;

    try {
      setIsSubmitting(true);
      await api.post('/api/v1/member/payments/submit', {
        installment_id: selectedDue.id,
        amount: selectedDue.total_amount,
        payment_method: paymentMethod,
        transaction_id: transactionId,
      });
      
      setSelectedDue(null);
      setTransactionId('');
      fetchData(); // Refresh data
    } catch (err) {
      alert(err.response?.data?.detail || 'Payment submission failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getStatusBadge = (status) => {
    switch(status) {
      case 'success':
        return <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-bold">Verified</span>;
      case 'pending':
        return <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-bold">Pending Auth</span>;
      case 'failed':
        return <span className="px-2 py-1 bg-red-100 text-red-700 rounded-full text-xs font-bold">Rejected</span>;
      default:
        return <span className="px-2 py-1 bg-gray-100 text-gray-700 rounded-full text-xs font-bold">{status}</span>;
    }
  };

  if (loading) return <div className="min-h-screen p-10 flex justify-center"><RefreshCw className="animate-spin text-corpBlue" /></div>;

  return (
    <div className="min-h-screen bg-bgAlt1 py-10 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center gap-4 mb-6">
          <button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-corpTextDark mb-2">My Dues & Payments</h1>
            <p className="text-corpTextLight mb-0">View your pending installments and submit payment proofs.</p>
          </div>
        </div>
        
        {error && <div className="bg-red-100 text-red-700 p-4 rounded-xl mb-6 flex gap-2"><AlertCircle /> {error}</div>}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          
          {/* Dues Section */}
          <div>
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><Clock className="text-corpGold" /> Pending Dues</h2>
            {dues.length === 0 ? (
              <div className="bg-white p-8 rounded-2xl shadow-sm text-center border">
                <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-3" />
                <h3 className="font-bold text-lg">All Cleared!</h3>
                <p className="text-gray-500">You have no pending dues for this month.</p>
              </div>
            ) : (
              <div className="space-y-4">
                {dues.map(due => (
                  <div key={due.id} className={`p-5 rounded-2xl border bg-white shadow-sm transition-all ${selectedDue?.id === due.id ? 'border-corpBlue ring-2 ring-blue-100' : 'border-gray-200'}`}>
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <span className="text-xs font-bold text-blue-600 uppercase tracking-wide">Month {due.month_number}</span>
                        <h3 className="font-bold text-lg text-corpTextDark">{due.plan_name}</h3>
                      </div>
                      <div className="text-right">
                        <p className="text-xs text-gray-500">Amount Due</p>
                        <p className="font-bold text-xl text-corpTextDark">₹{due.total_amount.toLocaleString()}</p>
                      </div>
                    </div>
                    <div className="flex justify-between items-center mt-4">
                      <p className="text-sm text-red-500 font-semibold">Due by: {format(new Date(due.due_date), 'dd MMM yyyy')}</p>
                      {selectedDue?.id === due.id ? (
                        <button onClick={() => setSelectedDue(null)} className="px-4 py-1.5 bg-gray-100 text-gray-700 rounded-lg text-sm font-semibold">Cancel</button>
                      ) : (
                        <button onClick={() => setSelectedDue(due)} className="px-4 py-1.5 bg-corpBlue text-white rounded-lg text-sm font-semibold hover:bg-corpNavy">Pay Now</button>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
            
            {/* Payment Form (Shows when a due is selected) */}
            {selectedDue && (
              <div className="mt-6 bg-white p-6 rounded-2xl border shadow-lg animate-fade-in-up">
                <h3 className="font-bold text-lg mb-4">Submit Payment Details</h3>
                <form onSubmit={handlePay} className="space-y-4">
                  <div className="bg-blue-50 p-4 rounded-xl mb-4 border border-blue-100">
                    <p className="text-sm text-blue-800">Please transfer <strong>₹{selectedDue.total_amount}</strong> via GPay/PhonePe to <strong>+91 9876543210</strong> (or scan the office QR). Enter the UPI Reference Number below to submit.</p>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-1">Payment Method</label>
                    <select value={paymentMethod} onChange={(e) => setPaymentMethod(e.target.value)} className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-corpBlue outline-none">
                      <option value="UPI">UPI (GPay / PhonePe / Paytm)</option>
                      <option value="Bank Transfer">Bank Transfer (IMPS/NEFT)</option>
                      <option value="Cash">Cash (Paid at Branch)</option>
                    </select>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium mb-1">Transaction / Reference ID</label>
                    <input type="text" required value={transactionId} onChange={(e) => setTransactionId(e.target.value)} placeholder="e.g. 31234567890" className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-corpBlue outline-none" />
                  </div>
                  
                  <button type="submit" disabled={isSubmitting} className="w-full py-3 bg-green-600 hover:bg-green-700 text-white font-bold rounded-lg transition-colors">
                    {isSubmitting ? 'Submitting...' : 'Submit Payment Proof'}
                  </button>
                </form>
              </div>
            )}
          </div>

          {/* History Section */}
          <div>
            <h2 className="text-xl font-bold mb-4 flex items-center gap-2"><IndianRupee className="text-corpGold" /> Payment History</h2>
            <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
              {history.length === 0 ? (
                <div className="p-8 text-center text-gray-500">No previous payments found.</div>
              ) : (
                <div className="divide-y">
                  {history.map(payment => (
                    <div key={payment.id} className="p-4 hover:bg-gray-50 flex items-center justify-between">
                      <div>
                        <p className="font-bold text-corpTextDark">₹{payment.amount.toLocaleString()}</p>
                        <p className="text-xs text-gray-500">{payment.payment_method} • Ref: {payment.transaction_id}</p>
                        <p className="text-xs text-gray-400 mt-1">{format(new Date(payment.created_at), 'dd MMM yyyy, hh:mm a')}</p>
                      </div>
                      <div className="text-right">
                        {getStatusBadge(payment.status)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
          
        </div>
      </div>
    </div>
  );
};

export default MemberPayments;

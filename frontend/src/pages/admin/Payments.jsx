import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { IndianRupee, CheckCircle, XCircle, RefreshCw, ArrowLeft, Trash2, Mail } from 'lucide-react';
import { format } from 'date-fns';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

const AdminPayments = () => {
  const navigate = useNavigate();
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Modal State for Reject
  const [rejectModal, setRejectModal] = useState({ show: false, paymentId: null, notes: '' });

  const fetchPayments = async () => {
    try {
      setLoading(true);
      const res = await api.get('/api/v1/admin/payments/');
      setPayments(res.data);
    } catch (err) {
      setError('Failed to load payments');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPayments();
  }, []);

  const handleVerify = async (paymentId, status, notes = '') => {
    try {
      await api.put(`/api/v1/admin/payments/${paymentId}/status`, { status, notes });
      setRejectModal({ show: false, paymentId: null, notes: '' });
      fetchPayments(); // Refresh list
    } catch (err) {
      alert(err.response?.data?.detail || 'Update failed');
    }
  };

  const handleSendDueReminders = async () => {
    try {
      const res = await api.post('/api/v1/admin/payments/send-due-reminders');
      toast.success(`📧 Due reminder emails sent to ${res.data.reminded_members_count || 0} unpaid members!`);
    } catch (err) {
      toast.error('Failed to send due reminder emails');
    }
  };

  const handleClearAllPayments = async () => {
    if (!window.confirm('Are you sure you want to clear all payment records and reset installments to pending?')) return;
    try {
      const res = await api.delete('/api/v1/admin/payments/clear-all');
      toast.success(res.data.message || 'All payment records cleared!');
      fetchPayments();
    } catch (err) {
      toast.error('Failed to clear payments');
    }
  };

  const pendingPayments = payments.filter(p => p.status === 'pending');
  const pastPayments = payments.filter(p => p.status !== 'pending');

  if (loading) return <div className="min-h-screen p-10 flex justify-center"><RefreshCw className="animate-spin text-corpBlue w-8 h-8" /></div>;

  return (
    <div className="p-4 sm:p-8 max-w-7xl mx-auto font-sans">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 sm:mb-8 gap-4">
        <div className="flex items-center gap-3 sm:gap-4">
          <button 
            onClick={() => navigate('/admin/dashboard')}
            className="w-9 h-9 sm:w-10 sm:h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold text-corpTextDark flex items-center gap-2">
              <IndianRupee className="w-7 h-7 sm:w-8 sm:h-8 text-corpGold" /> Payment Verifications
            </h1>
            <p className="text-corpTextLight text-xs sm:text-sm mt-1">Verify manual payments submitted by members</p>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-2 sm:gap-3 w-full sm:w-auto">
          <button 
            onClick={handleSendDueReminders}
            className="flex-1 sm:flex-initial flex items-center justify-center gap-1.5 px-3.5 py-2 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-white rounded-xl shadow-md text-xs font-bold transition-all"
            title="Send email reminders to all members with pending dues"
          >
            <Mail className="w-4 h-4" /> Send Due Reminders
          </button>
          <button 
            onClick={handleClearAllPayments} 
            className="flex-initial flex items-center justify-center gap-1.5 px-3 py-2 bg-red-50 text-red-600 border border-red-200 rounded-xl shadow-sm hover:bg-red-100 text-xs font-bold transition-all"
            title="Delete all payments and reset dues"
          >
            <Trash2 className="w-4 h-4" /> Clear All
          </button>
          <button onClick={fetchPayments} className="flex-initial flex items-center justify-center gap-1.5 px-3 py-2 bg-white border rounded-xl shadow-sm hover:bg-gray-50 text-xs font-semibold">
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        </div>
      </div>

      {error && <div className="bg-red-100 text-red-700 p-4 rounded-xl mb-6">{error}</div>}

      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Pending Verifications ({pendingPayments.length})</h2>
        
        {pendingPayments.length === 0 ? (
          <div className="bg-white p-8 rounded-2xl shadow-sm border text-center text-gray-500">
            No pending payments to verify. You're all caught up!
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {pendingPayments.map(payment => (
              <div key={payment.id} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col justify-between hover:border-blue-300 transition-all font-sans">
                <div>
                  <div className="flex justify-between items-start mb-3">
                    <span className="px-2.5 py-0.5 bg-amber-100 text-amber-800 rounded-full text-[10px] font-extrabold uppercase tracking-wider">
                      Requires Admin Verification
                    </span>
                    <p className="text-[11px] text-slate-400 font-medium">
                      {format(new Date(payment.created_at || Date.now()), 'dd MMM, hh:mm a')}
                    </p>
                  </div>
                  
                  <div className="mb-3 p-3 bg-slate-50 rounded-xl border border-slate-150">
                    <p className="text-[11px] text-slate-400 uppercase font-bold">Member Details</p>
                    <p className="font-extrabold text-slate-900 text-base">{payment.user_name || `Member #${payment.user_id}`}</p>
                    <p className="text-xs text-slate-500 font-medium">{payment.user_phone || payment.user_email}</p>
                  </div>
                  
                  <div className="flex items-center justify-between mb-3 bg-blue-50/60 p-3 rounded-xl border border-blue-100">
                    <div>
                      <p className="text-[10px] text-blue-700 font-bold uppercase">Scheme & Month</p>
                      <p className="font-extrabold text-slate-900 text-xs">{payment.plan_name} (Month {payment.month_number || 1})</p>
                    </div>
                    <div className="text-right">
                      <p className="text-[10px] text-emerald-700 font-bold uppercase">Amount</p>
                      <p className="font-black text-xl text-emerald-800">₹{payment.amount?.toLocaleString()}</p>
                    </div>
                  </div>
                  
                  <div className="bg-slate-50 p-3 rounded-xl mb-4 text-xs border border-slate-200 font-mono">
                    <p className="text-slate-500 mb-0.5">Method: <span className="font-bold text-slate-900 font-sans">{payment.payment_method}</span></p>
                    <p className="text-slate-500">Ref / UTR: <span className="font-bold text-corpBlue">{payment.transaction_id}</span></p>
                  </div>
                </div>
                
                <div className="flex gap-3 pt-2 border-t border-slate-100">
                  <button 
                    onClick={() => setRejectModal({ show: true, paymentId: payment.id, notes: '' })} 
                    className="flex-1 py-2.5 bg-red-50 text-red-600 hover:bg-red-100 font-bold rounded-xl text-xs transition-colors border border-red-200"
                  >
                    ❌ Reject
                  </button>
                  <button 
                    onClick={() => handleVerify(payment.id, 'success')} 
                    className="flex-1 py-2.5 bg-emerald-600 text-white hover:bg-emerald-700 font-extrabold rounded-xl text-xs transition-colors shadow-md flex items-center justify-center gap-1"
                  >
                    ✅ Approve Payment
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div>
        <h2 className="text-xl font-bold mb-4">Past Verifications</h2>
        <div className="bg-white rounded-2xl border shadow-sm overflow-hidden">
          <table className="w-full text-left">
            <thead className="bg-gray-50 border-b text-sm text-gray-500">
              <tr>
                <th className="p-4 font-semibold">Date</th>
                <th className="p-4 font-semibold">Member ID</th>
                <th className="p-4 font-semibold">Ref ID</th>
                <th className="p-4 font-semibold text-right">Amount</th>
                <th className="p-4 font-semibold text-center">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y text-sm">
              {pastPayments.length === 0 ? (
                <tr><td colSpan="5" className="p-8 text-center text-gray-400">No past records</td></tr>
              ) : (
                pastPayments.map(payment => (
                  <tr key={payment.id} className="hover:bg-gray-50">
                    <td className="p-4">{format(new Date(payment.created_at), 'dd MMM yyyy')}</td>
                    <td className="p-4 font-medium text-corpBlue">#{payment.user_id}</td>
                    <td className="p-4 font-mono text-xs">{payment.transaction_id}</td>
                    <td className="p-4 font-bold text-right">₹{payment.amount.toLocaleString()}</td>
                    <td className="p-4 text-center">
                      {payment.status === 'success' ? (
                        <span className="inline-flex items-center gap-1 text-green-600 bg-green-50 px-2 py-1 rounded-full text-xs font-bold"><CheckCircle className="w-3 h-3"/> Approved</span>
                      ) : (
                        <span className="inline-flex items-center gap-1 text-red-600 bg-red-50 px-2 py-1 rounded-full text-xs font-bold"><XCircle className="w-3 h-3"/> Rejected</span>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Reject Modal */}
      {rejectModal.show && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl p-6 w-full max-w-md shadow-2xl animate-fade-in-up">
            <h3 className="text-xl font-bold mb-2">Reject Payment</h3>
            <p className="text-gray-500 text-sm mb-4">Please provide a reason for rejecting this payment (e.g. Reference ID not found in bank statement).</p>
            <textarea 
              className="w-full border rounded-lg p-3 text-sm focus:ring-2 focus:ring-red-500 outline-none mb-4" 
              rows="3" 
              placeholder="Reason for rejection..."
              value={rejectModal.notes}
              onChange={(e) => setRejectModal({...rejectModal, notes: e.target.value})}
            ></textarea>
            <div className="flex justify-end gap-3">
              <button onClick={() => setRejectModal({ show: false, paymentId: null, notes: '' })} className="px-4 py-2 font-bold text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200">Cancel</button>
              <button onClick={() => handleVerify(rejectModal.paymentId, 'failed', rejectModal.notes)} className="px-4 py-2 font-bold text-white bg-red-600 rounded-lg hover:bg-red-700">Confirm Reject</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPayments;

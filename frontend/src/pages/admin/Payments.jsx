import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { IndianRupee, CheckCircle, XCircle, RefreshCw, ArrowLeft } from 'lucide-react';
import { format } from 'date-fns';

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

  const pendingPayments = payments.filter(p => p.status === 'pending');
  const pastPayments = payments.filter(p => p.status !== 'pending');

  if (loading) return <div className="min-h-screen p-10 flex justify-center"><RefreshCw className="animate-spin text-corpBlue w-8 h-8" /></div>;

  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/admin/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-corpTextDark flex items-center gap-2">
              <IndianRupee className="w-8 h-8 text-corpGold" /> Payment Verifications
            </h1>
            <p className="text-corpTextLight mt-1">Verify manual payments submitted by members</p>
          </div>
        </div>
        <button onClick={fetchPayments} className="flex items-center gap-2 px-4 py-2 bg-white border rounded-lg shadow-sm hover:bg-gray-50 text-sm font-semibold">
          <RefreshCw className="w-4 h-4" /> Refresh
        </button>
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
              <div key={payment.id} className="bg-white p-5 rounded-2xl border shadow-sm flex flex-col justify-between">
                <div>
                  <div className="flex justify-between items-start mb-3">
                    <span className="px-2 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-bold uppercase tracking-wider">Requires Verification</span>
                    <p className="text-xs text-gray-400">{format(new Date(payment.created_at), 'dd MMM, hh:mm a')}</p>
                  </div>
                  
                  <div className="mb-4">
                    <p className="text-sm text-gray-500">Member ID</p>
                    <p className="font-bold text-corpTextDark">#{payment.user_id}</p>
                  </div>
                  
                  <div className="mb-4">
                    <p className="text-sm text-gray-500">Amount Paid</p>
                    <p className="font-bold text-2xl text-corpTextDark">₹{payment.amount.toLocaleString()}</p>
                  </div>
                  
                  <div className="bg-gray-50 p-3 rounded-lg mb-4 text-sm border">
                    <p className="text-gray-500 mb-1">Payment Method: <span className="font-bold text-corpTextDark">{payment.payment_method}</span></p>
                    <p className="text-gray-500">Ref ID: <span className="font-mono text-corpBlue">{payment.transaction_id}</span></p>
                  </div>
                </div>
                
                <div className="flex gap-3">
                  <button onClick={() => setRejectModal({ show: true, paymentId: payment.id, notes: '' })} className="flex-1 py-2 bg-red-50 text-red-600 hover:bg-red-100 font-bold rounded-lg transition-colors border border-red-200">
                    Reject
                  </button>
                  <button onClick={() => handleVerify(payment.id, 'success')} className="flex-1 py-2 bg-green-600 text-white hover:bg-green-700 font-bold rounded-lg transition-colors shadow-sm">
                    Approve
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

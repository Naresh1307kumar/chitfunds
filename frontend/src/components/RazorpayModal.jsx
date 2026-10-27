import React, { useState, useEffect } from 'react';
import { ShieldCheck, QrCode, Lock, ArrowLeft, X, Check, Loader2, Sparkles } from 'lucide-react';
import api from '../services/api';
import toast from 'react-hot-toast';

const RazorpayModal = ({ due, onClose, onSuccess }) => {
  const [emergencyReason, setEmergencyReason] = useState('hospital');
  const [isProcessing, setIsProcessing] = useState(false);
  const [copied, setCopied] = useState(false);

  if (!due) return null;

  const upiUri = `upi://pay?pa=nareshk1213@oksbi&pn=Naresh%20Kumar&am=${due.total_amount}&cu=INR`;
  const qrImageUrl = "/images/naresh_gpay_qr.png";

  const handleCopyUpi = () => {
    navigator.clipboard.writeText('nareshk1213@oksbi');
    setCopied(true);
    toast.success('UPI ID (nareshk1213@oksbi) copied to clipboard!');
    setTimeout(() => setCopied(false), 2000);
  };

  // Automatic Background Payment Listener (Polling Backend Only - No Fake Timer!)
  useEffect(() => {
    let intervalId;

    const checkPaymentStatus = async () => {
      try {
        const res = await api.get('/api/v1/member/payments/history');
        const paidItem = res.data.find(p => p.month_number === due.month_number && p.status === 'verified');
        if (paidItem) {
          toast.success('🎉 GPay Payment Detected & Receipt Generated!');
          onSuccess(paidItem);
        }
      } catch (err) {
        console.error('Payment polling error:', err);
      }
    };

    intervalId = setInterval(checkPaymentStatus, 3000);

    return () => {
      clearInterval(intervalId);
    };
  }, [due, onSuccess]);

  const handleManualVerify = async () => {
    try {
      setIsProcessing(true);
      const orderRes = await api.post('/api/v1/member/payments/razorpay/create-order', {
        installment_id: due.id
      });
      const payId = `pay_upi_${Date.now()}`;
      const verifyRes = await api.post('/api/v1/member/payments/razorpay/verify', {
        installment_id: due.id,
        razorpay_payment_id: payId,
        razorpay_order_id: orderRes.data.order_id,
        razorpay_signature: "naresh_gpay_verified",
        payment_method: "Google Pay UPI (nareshk1213@oksbi)",
        reason: emergencyReason
      });
      toast.success('⏳ Payment Request Submitted to Admin for Verification!');
      if (verifyRes.data.receipt) {
        onSuccess(verifyRes.data.receipt);
      } else {
        onClose();
      }
    } catch (e) {
      toast.error('Payment submission failed');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-4 font-sans animate-fade-in">
      <div className="bg-white rounded-3xl w-full max-w-md overflow-hidden shadow-2xl border border-slate-100 flex flex-col max-h-[92vh]">
        
        {/* Header Banner */}
        <div className="bg-gradient-to-r from-corpBlue via-indigo-900 to-blue-950 p-5 text-white relative">
          <div className="flex justify-between items-center relative z-10">
            <div className="flex items-center gap-2.5">
              <div className="w-10 h-10 rounded-2xl bg-white/15 backdrop-blur-md flex items-center justify-center border border-white/20">
                <QrCode className="w-5 h-5 text-emerald-400" />
              </div>
              <div>
                <h3 className="font-extrabold text-base tracking-wide flex items-center gap-1.5">
                  Scan & Pay GPay QR
                </h3>
                <p className="text-[11px] text-blue-200 font-medium">Default Receiver: Naresh kumar Kumar</p>
              </div>
            </div>
            <button 
              onClick={onClose}
              className="w-8 h-8 rounded-full bg-white/15 hover:bg-white/30 flex items-center justify-center text-white transition-colors"
              title="Close"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          <div className="mt-3.5 p-3 bg-white/10 backdrop-blur-md rounded-2xl border border-white/15 flex items-center justify-between">
            <div>
              <span className="text-[9px] uppercase font-bold text-blue-200 block">Total Due Amount</span>
              <span className="text-xl sm:text-2xl font-black text-white">₹{due.total_amount?.toLocaleString()}</span>
            </div>
            <span className="text-[11px] bg-emerald-500/20 text-emerald-300 border border-emerald-400/30 px-2.5 py-1 rounded-full font-bold">
              Month {due.month_number} • {due.plan_name}
            </span>
          </div>
        </div>

        {/* Body Container */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4 text-center">
          
          {/* Emergency Reason Selector */}
          <div className="text-left bg-slate-50 p-3 rounded-2xl border border-slate-200">
            <label className="block text-[10px] font-black text-slate-500 uppercase tracking-wider mb-1">
              Select Financial Need / Emergency Reason
            </label>
            <select 
              value={emergencyReason} 
              onChange={(e) => setEmergencyReason(e.target.value)} 
              className="w-full p-2.5 border border-slate-200 rounded-xl bg-white text-xs font-semibold text-slate-800 outline-none"
            >
              <option value="hospital">🏥 Hospital / Medical Emergency (Rank 1)</option>
              <option value="education">🎓 Higher Education / School Fees (Rank 2)</option>
              <option value="marriage">💍 Marriage / Family Function (Rank 3)</option>
              <option value="business">💼 Business Capital / Expansion (Rank 4)</option>
              <option value="personal">👤 Personal Savings / Investment (Rank 5)</option>
            </select>
          </div>

          {/* Scannable GPay QR Image */}
          <div className="p-4 bg-slate-50/90 border border-slate-200 rounded-2xl space-y-3 shadow-inner">
            <div className="w-48 h-48 bg-white p-2 border-2 border-corpBlue/30 rounded-2xl mx-auto shadow-md flex items-center justify-center relative overflow-hidden">
              <img 
                src={qrImageUrl} 
                alt={`Pay ₹${due.total_amount} GPay QR Code`} 
                className="w-full h-full object-contain rounded-xl"
              />
            </div>

            <div>
              <p className="text-xs font-extrabold text-slate-900">Naresh kumar Kumar (Indian Bank)</p>
              <p className="text-[11px] text-emerald-700 font-bold mt-0.5">Scan using GPay, PhonePe, Paytm or BHIM (₹{due.total_amount?.toLocaleString()})</p>
            </div>

            <div className="p-2.5 bg-white border border-slate-200 rounded-xl flex items-center justify-between text-left">
              <div>
                <span className="text-[10px] text-slate-400 font-bold block uppercase">Default Receiver UPI ID</span>
                <strong className="text-xs font-mono text-slate-900">nareshk1213@oksbi</strong>
              </div>
              <button 
                onClick={handleCopyUpi}
                className="px-2.5 py-1 bg-blue-50 text-corpBlue hover:bg-blue-100 rounded-lg text-[10px] font-bold transition-colors flex items-center gap-1 border border-blue-200"
              >
                {copied ? <Check className="w-3 h-3 text-emerald-600" /> : 'Copy UPI'}
              </button>
            </div>
          </div>

          {/* Submit Payment Request for Admin Approval */}
          <div className="space-y-2">
            <button
              onClick={handleManualVerify}
              disabled={isProcessing}
              className="w-full py-3.5 bg-gradient-to-r from-blue-700 via-corpBlue to-indigo-900 hover:from-blue-800 hover:to-indigo-950 text-white font-extrabold text-xs rounded-2xl shadow-md transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isProcessing ? (
                <>
                  <Loader2 className="w-4 h-4 text-white animate-spin" /> Submitting Request...
                </>
              ) : (
                <>
                  📩 Submit Payment Request for Admin Verification
                </>
              )}
            </button>

            <button
              onClick={onClose}
              className="w-full py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs rounded-2xl border border-slate-200"
            >
              <ArrowLeft className="w-4 h-4 inline mr-1" /> Cancel Payment
            </button>
          </div>

        </div>

      </div>
    </div>
  );
};

export default RazorpayModal;

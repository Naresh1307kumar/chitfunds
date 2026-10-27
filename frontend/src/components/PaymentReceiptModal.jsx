import React from 'react';
import { ShieldCheck, Download, Printer, CheckCircle2, X, ArrowLeft } from 'lucide-react';

const PaymentReceiptModal = ({ receipt, onClose }) => {
  if (!receipt) return null;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="fixed inset-0 bg-slate-900/70 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-lg w-full overflow-hidden shadow-2xl border border-slate-100 animate-fade-in-up font-sans">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-slate-900 via-corpNavy to-slate-800 p-6 text-white flex items-center justify-between relative overflow-hidden">
          <div className="flex items-center gap-3 relative z-10">
            <button 
              onClick={onClose}
              className="w-9 h-9 rounded-xl bg-white/10 hover:bg-white/20 border border-white/20 flex items-center justify-center text-white transition-all shadow-sm active:scale-95 group"
              title="Go Back"
            >
              <ArrowLeft className="w-4 h-4 text-white group-hover:-translate-x-0.5 transition-transform" />
            </button>
            <div className="w-10 h-10 rounded-2xl bg-white/10 border border-white/20 flex items-center justify-center text-amber-400">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <div>
              <h3 className="font-extrabold text-lg tracking-tight">SecureChit Receipt</h3>
              <p className="text-[11px] text-slate-300">Official Payment Proof Voucher</p>
            </div>
          </div>
          <button 
            onClick={onClose} 
            className="w-8 h-8 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors relative z-10"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Receipt Voucher Body */}
        <div className="p-6 space-y-5 bg-slate-50/50 print:p-0">
          
          {/* Status Banner */}
          <div className="bg-emerald-50 border border-emerald-200 rounded-2xl p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-8 h-8 text-emerald-600 flex-shrink-0" />
              <div>
                <span className="text-[10px] font-extrabold uppercase tracking-widest text-emerald-700 block">Payment Verified</span>
                <span className="font-bold text-slate-900 text-sm">Receipt #{receipt.receipt_number}</span>
              </div>
            </div>
            <span className="bg-emerald-600 text-white font-black text-[10px] px-2.5 py-1 rounded-full uppercase tracking-widest shadow-sm">
              PAID
            </span>
          </div>

          {/* Details Table */}
          <div className="bg-white rounded-2xl border border-slate-200 p-5 space-y-3 text-xs shadow-sm">
            <div className="flex justify-between pb-2 border-b border-slate-100">
              <span className="text-slate-500">Member Name:</span>
              <span className="font-bold text-slate-900">{receipt.member_name}</span>
            </div>
            <div className="flex justify-between pb-2 border-b border-slate-100">
              <span className="text-slate-500">Chit Scheme:</span>
              <span className="font-bold text-slate-900">{receipt.plan_name}</span>
            </div>
            <div className="flex justify-between pb-2 border-b border-slate-100">
              <span className="text-slate-500">Ticket ID:</span>
              <span className="font-bold text-corpBlue">{receipt.ticket_number}</span>
            </div>
            <div className="flex justify-between pb-2 border-b border-slate-100">
              <span className="text-slate-500">Emergency Reason:</span>
              <span className="font-bold text-amber-700 uppercase bg-amber-50 px-2 py-0.5 rounded border border-amber-200 text-[10px]">
                {receipt.emergency_reason}
              </span>
            </div>
            <div className="flex justify-between pb-2 border-b border-slate-100">
              <span className="text-slate-500">Payment Gateway:</span>
              <span className="font-semibold text-slate-800">{receipt.payment_method}</span>
            </div>
            <div className="flex justify-between pb-2 border-b border-slate-100">
              <span className="text-slate-500">Razorpay Payment ID:</span>
              <span className="font-mono text-slate-700">{receipt.payment_id}</span>
            </div>
            <div className="flex justify-between items-center pt-2">
              <span className="text-sm font-bold text-slate-800">Total Amount Paid:</span>
              <span className="text-2xl font-black text-emerald-600">₹{receipt.amount_paid?.toLocaleString()}</span>
            </div>
          </div>

          <p className="text-[10px] text-slate-400 text-center leading-relaxed">
            This digital receipt is generated by SecureChit Management System. Authenticated with Razorpay Gateway Ledger.
          </p>

        </div>

        {/* Footer Action Buttons */}
        <div className="p-4 bg-white border-t border-slate-200 flex gap-3">
          <button 
            onClick={handlePrint}
            className="flex-1 py-3 bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold rounded-2xl text-xs transition-colors flex items-center justify-center gap-2 border border-slate-200"
          >
            <Printer className="w-4 h-4" /> Print Receipt
          </button>
          <button 
            onClick={onClose}
            className="flex-1 py-3 bg-corpBlue hover:bg-blue-900 text-white font-bold rounded-2xl text-xs transition-colors shadow-md flex items-center justify-center gap-2"
          >
            <CheckCircle2 className="w-4 h-4" /> Done
          </button>
        </div>

      </div>
    </div>
  );
};

export default PaymentReceiptModal;

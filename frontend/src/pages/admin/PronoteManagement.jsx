import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import toast from 'react-hot-toast';
import {
  FileText, ArrowLeft, RefreshCw, CheckCircle, Trash2, Printer,
  Eraser, Save, ShieldCheck, UserCheck, Calendar, IndianRupee,
  Percent, FileSignature, AlertCircle, Eye, X
} from 'lucide-react';
import { format } from 'date-fns';

const PronoteManagement = () => {
  const navigate = useNavigate();
  const canvasRef = useRef(null);

  // Data lists
  const [members, setMembers] = useState([]);
  const [plans, setPlans] = useState([]);
  const [pronotes, setPronotes] = useState([]);
  const [loading, setLoading] = useState(true);

  // Canvas drawing state
  const [isDrawing, setIsDrawing] = useState(false);
  const [signatureData, setSignatureData] = useState(null);
  const [hasDrawn, setHasDrawn] = useState(false);

  // Form State
  const todayStr = new Date().toISOString().split('T')[0];
  const nextYearStr = new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];

  const [formData, setFormData] = useState({
    member_id: '',
    member_name: '',
    chit_id: '',
    loan_amount: '',
    issue_date: todayStr,
    due_date: nextYearStr,
    interest_rate: '0',
    repayment_amount: '0',
    purpose: 'Chit Auction Prize Payout & Security Guarantee',
    status: 'active'
  });

  const [autoPronoteId, setAutoPronoteId] = useState('PRN-2026-0001');
  const [selectedPronoteForPrint, setSelectedPronoteForPrint] = useState(null);

  // Initial Fetch Data
  const fetchData = async () => {
    try {
      setLoading(true);
      const [mRes, pRes, nRes] = await Promise.all([
        api.get('/api/v1/admin/members'),
        api.get('/api/v1/admin/plans/'),
        api.get('/api/v1/admin/pronotes/')
      ]);

      setMembers(mRes.data || []);
      setPlans(pRes.data || []);
      const notesList = nRes.data || [];
      setPronotes(notesList);

      // Generate next Pronote ID
      const year = new Date().getFullYear();
      const count = notesList.length + 1;
      setAutoPronoteId(`PRN-${year}-${count.toString().padStart(4, '0')}`);
    } catch (err) {
      console.error('Failed to load pronotes data:', err);
      toast.error('Failed to load members, plans or pronotes');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  // Recalculate Repayment Amount whenever loan_amount or interest_rate changes
  useEffect(() => {
    const principal = parseFloat(formData.loan_amount) || 0;
    const rate = parseFloat(formData.interest_rate) || 0;
    const total = principal + (principal * rate) / 100;
    setFormData((prev) => ({ ...prev, repayment_amount: total.toFixed(2) }));
  }, [formData.loan_amount, formData.interest_rate]);

  // Handle Member selection
  const handleMemberChange = (e) => {
    const mId = e.target.value;
    const selectedM = members.find((m) => m.id === parseInt(mId));
    setFormData((prev) => ({
      ...prev,
      member_id: mId,
      member_name: selectedM ? (selectedM.name || selectedM.username) : ''
    }));
  };

  // Canvas Drawing Handlers
  const startDrawing = (e) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX || (e.touches && e.touches[0].clientX)) - rect.left;
    const y = (e.clientY || (e.touches && e.touches[0].clientY)) - rect.top;

    ctx.beginPath();
    ctx.moveTo(x, y);
    setIsDrawing(true);
    setHasDrawn(true);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX || (e.touches && e.touches[0].clientX)) - rect.left;
    const y = (e.clientY || (e.touches && e.touches[0].clientY)) - rect.top;

    ctx.lineWidth = 2.5;
    ctx.lineCap = 'round';
    ctx.strokeStyle = '#1e293b';
    ctx.lineTo(x, y);
    ctx.stroke();
  };

  const stopDrawing = () => {
    if (isDrawing && canvasRef.current) {
      setIsDrawing(false);
      const dataUrl = canvasRef.current.toDataURL('image/png');
      setSignatureData(dataUrl);
    }
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
    }
    setHasDrawn(false);
    setSignatureData(null);
  };

  // Clear Form & Signature
  const handleClearForm = () => {
    setFormData({
      member_id: '',
      member_name: '',
      chit_id: '',
      loan_amount: '',
      issue_date: todayStr,
      due_date: nextYearStr,
      interest_rate: '0',
      repayment_amount: '0',
      purpose: 'Chit Auction Prize Payout & Security Guarantee',
      status: 'active'
    });
    clearCanvas();
    toast.success('Form cleared!');
  };

  // Save Pronote
  const handleSavePronote = async (e) => {
    e.preventDefault();

    if (!formData.member_id) {
      toast.error('Please select a Member');
      return;
    }
    if (!formData.loan_amount || parseFloat(formData.loan_amount) <= 0) {
      toast.error('Please enter a valid Loan Amount');
      return;
    }
    if (!hasDrawn || !signatureData) {
      toast.error('Please provide a Member Digital Signature on the canvas');
      return;
    }

    try {
      const payload = {
        member_id: parseInt(formData.member_id),
        chit_id: formData.chit_id ? parseInt(formData.chit_id) : null,
        loan_amount: parseFloat(formData.loan_amount),
        issue_date: formData.issue_date,
        due_date: formData.due_date,
        interest_rate: parseFloat(formData.interest_rate || 0),
        repayment_amount: parseFloat(formData.repayment_amount),
        purpose: formData.purpose,
        status: formData.status,
        signature: signatureData
      };

      const res = await api.post('/api/v1/admin/pronotes/', payload);
      toast.success(`🎉 Promissory Note ${res.data.pronote_id} created successfully!`);

      // Refresh list & reset form
      fetchData();
      handleClearForm();
    } catch (err) {
      console.error('Error saving pronote:', err);
      toast.error(err.response?.data?.detail || 'Failed to save Promissory Note');
    }
  };

  // Update Status
  const handleStatusChange = async (noteId, newStatus) => {
    try {
      await api.put(`/api/v1/admin/pronotes/${noteId}/status`, { status: newStatus });
      toast.success('Pronote status updated!');
      fetchData();
    } catch (err) {
      toast.error('Failed to update status');
    }
  };

  // Delete Pronote
  const handleDeletePronote = async (noteId) => {
    if (!window.confirm('Are you sure you want to delete this Promissory Note?')) return;
    try {
      await api.delete(`/api/v1/admin/pronotes/${noteId}`);
      toast.success('Promissory Note deleted!');
      fetchData();
    } catch (err) {
      toast.error('Failed to delete Promissory Note');
    }
  };

  // Print Action
  const handlePrint = (note) => {
    setSelectedPronoteForPrint(note || {
      pronote_id: autoPronoteId,
      member_name: formData.member_name || 'Selected Member',
      loan_amount: parseFloat(formData.loan_amount) || 0,
      issue_date: formData.issue_date,
      due_date: formData.due_date,
      interest_rate: formData.interest_rate,
      repayment_amount: formData.repayment_amount,
      purpose: formData.purpose,
      status: formData.status,
      signature: signatureData,
      chit_name: plans.find((p) => p.id === parseInt(formData.chit_id))?.plan_name || 'General Chit Fund Security'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50">
        <RefreshCw className="w-8 h-8 text-corpBlue animate-spin" />
      </div>
    );
  }

  return (
    <div className="p-4 sm:p-8 max-w-7xl mx-auto font-sans">
      
      {/* Header Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 sm:mb-8 gap-4 border-b border-slate-200 pb-5">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/admin/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors bg-white shadow-sm"
            title="Go Back to Admin Dashboard"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
          <div>
            <div className="flex items-center gap-2">
              <FileSignature className="w-8 h-8 text-corpBlue" />
              <h1 className="text-2xl sm:text-3xl font-extrabold text-corpNavy">
                PROMISSORY NOTE (Pronote)
              </h1>
            </div>
            <p className="text-corpTextLight text-xs sm:text-sm font-medium mt-0.5">
              Secure Chit Fund • Member Security & Legal Loan Agreement Management
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={fetchData}
            className="px-3.5 py-2 bg-white border border-slate-200 rounded-xl shadow-sm hover:bg-slate-50 text-slate-700 text-xs font-bold flex items-center gap-1.5 transition-all"
          >
            <RefreshCw className="w-4 h-4" /> Refresh
          </button>
        </div>
      </div>

      {/* Main Pronote Form Card */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-xl overflow-hidden mb-10">
        
        {/* Form Header Banner */}
        <div className="bg-gradient-to-r from-slate-900 via-corpNavy to-slate-800 text-white p-6 sm:p-8 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <span className="px-3 py-1 bg-amber-500/20 text-amber-300 border border-amber-400/30 rounded-full text-[10px] font-extrabold uppercase tracking-widest inline-block mb-2">
              Official Legal Instrument
            </span>
            <h2 className="text-2xl sm:text-3xl font-black tracking-tight flex items-center gap-2">
              PROMISSORY NOTE
            </h2>
            <p className="text-slate-300 text-xs sm:text-sm font-medium">Secure Chit Fund Management System</p>
          </div>

          <div className="bg-white/10 backdrop-blur-md px-4 py-2.5 rounded-2xl border border-white/15 text-right">
            <span className="text-[10px] text-slate-300 block uppercase font-extrabold tracking-wider">Pronote ID</span>
            <span className="text-xl font-mono font-extrabold text-amber-400">{autoPronoteId}</span>
          </div>
        </div>

        {/* Form Inputs */}
        <form onSubmit={handleSavePronote} className="p-6 sm:p-8 space-y-6">
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            
            {/* Pronote ID (Read only) */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Pronote ID <span className="text-slate-400 font-normal">(Auto-generated)</span>
              </label>
              <input
                type="text"
                readOnly
                value={autoPronoteId}
                className="w-full bg-slate-100 border border-slate-200 rounded-xl p-3 text-sm font-mono font-bold text-slate-600 outline-none cursor-not-allowed"
              />
            </div>

            {/* Select Member */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Select Member <span className="text-red-500">*</span>
              </label>
              <select
                required
                value={formData.member_id}
                onChange={handleMemberChange}
                className="w-full border border-slate-300 rounded-xl p-3 text-sm focus:ring-2 focus:ring-corpBlue focus:border-corpBlue outline-none font-medium bg-white"
              >
                <option value="">-- Select Member --</option>
                {members.map((m) => (
                  <option key={m.id} value={m.id}>
                    #{m.id} - {m.name || m.username} ({m.phone || m.email})
                  </option>
                ))}
              </select>
            </div>

            {/* Member Name (Read only / Auto-filled) */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Member Name
              </label>
              <input
                type="text"
                readOnly
                value={formData.member_name}
                placeholder="Selected Member Name"
                className="w-full bg-slate-50 border border-slate-200 rounded-xl p-3 text-sm font-bold text-slate-900 outline-none"
              />
            </div>

            {/* Select Chit Scheme */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Chit Scheme / Plan
              </label>
              <select
                value={formData.chit_id}
                onChange={(e) => setFormData({ ...formData, chit_id: e.target.value })}
                className="w-full border border-slate-300 rounded-xl p-3 text-sm focus:ring-2 focus:ring-corpBlue focus:border-corpBlue outline-none font-medium bg-white"
              >
                <option value="">-- General Chit Fund Security --</option>
                {plans.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.plan_name} (₹{p.total_value?.toLocaleString()} Pool)
                  </option>
                ))}
              </select>
            </div>

            {/* Loan Amount */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Loan / Payout Amount (₹) <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <IndianRupee className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                <input
                  type="number"
                  required
                  min="1"
                  step="100"
                  placeholder="e.g. 50000"
                  value={formData.loan_amount}
                  onChange={(e) => setFormData({ ...formData, loan_amount: e.target.value })}
                  className="w-full border border-slate-300 rounded-xl p-3 pl-10 text-sm font-bold text-slate-900 focus:ring-2 focus:ring-corpBlue focus:border-corpBlue outline-none"
                />
              </div>
            </div>

            {/* Interest Rate (%) */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Interest Rate (% per annum)
              </label>
              <div className="relative">
                <Percent className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                <input
                  type="number"
                  min="0"
                  step="0.1"
                  placeholder="0"
                  value={formData.interest_rate}
                  onChange={(e) => setFormData({ ...formData, interest_rate: e.target.value })}
                  className="w-full border border-slate-300 rounded-xl p-3 pl-10 text-sm font-bold text-slate-900 focus:ring-2 focus:ring-corpBlue focus:border-corpBlue outline-none"
                />
              </div>
            </div>

            {/* Issue Date */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Issue Date <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                required
                value={formData.issue_date}
                onChange={(e) => setFormData({ ...formData, issue_date: e.target.value })}
                className="w-full border border-slate-300 rounded-xl p-3 text-sm font-medium focus:ring-2 focus:ring-corpBlue focus:border-corpBlue outline-none"
              />
            </div>

            {/* Due Date */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Due Date <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                required
                value={formData.due_date}
                onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
                className="w-full border border-slate-300 rounded-xl p-3 text-sm font-medium focus:ring-2 focus:ring-corpBlue focus:border-corpBlue outline-none"
              />
            </div>

            {/* Repayment Amount (Auto calculated) */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Repayment Amount (₹) <span className="text-slate-400 font-normal">(Auto-calculated)</span>
              </label>
              <input
                type="text"
                readOnly
                value={`₹ ${parseFloat(formData.repayment_amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}`}
                className="w-full bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-xl p-3 text-sm font-black outline-none"
              />
            </div>

            {/* Purpose */}
            <div className="md:col-span-2">
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Purpose / Remarks
              </label>
              <input
                type="text"
                value={formData.purpose}
                onChange={(e) => setFormData({ ...formData, purpose: e.target.value })}
                placeholder="Reason for Promissory Note"
                className="w-full border border-slate-300 rounded-xl p-3 text-sm focus:ring-2 focus:ring-corpBlue focus:border-corpBlue outline-none font-medium"
              />
            </div>

            {/* Status */}
            <div>
              <label className="block text-xs font-extrabold text-slate-700 uppercase mb-1.5">
                Status
              </label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="w-full border border-slate-300 rounded-xl p-3 text-sm font-bold focus:ring-2 focus:ring-corpBlue focus:border-corpBlue outline-none bg-white"
              >
                <option value="pending_signature">Pending Member Signature</option>
                <option value="active">Active (Signed & Pending Repayment)</option>
                <option value="paid">Paid & Discharged</option>
                <option value="overdue">Overdue</option>
              </select>
            </div>

          </div>

          {/* Digital Signature Canvas Section */}
          <div className="pt-4 border-t border-slate-150">
            <div className="flex justify-between items-center mb-3">
              <div>
                <label className="text-sm font-extrabold text-slate-900 uppercase flex items-center gap-2">
                  <FileSignature className="w-5 h-5 text-corpBlue" /> Member Digital Signature <span className="text-red-500">*</span>
                </label>
                <p className="text-xs text-slate-500">
                  Draw member signature inside the box using mouse, finger, or stylus touch.
                </p>
              </div>
              <button
                type="button"
                onClick={clearCanvas}
                className="px-3 py-1.5 text-xs font-bold text-red-600 bg-red-50 hover:bg-red-100 rounded-lg border border-red-200 flex items-center gap-1 transition-all"
              >
                <Eraser className="w-3.5 h-3.5" /> Clear Signature
              </button>
            </div>

            <div className="relative bg-slate-50 border-2 border-dashed border-slate-300 rounded-2xl overflow-hidden flex flex-col items-center justify-center p-2 group hover:border-corpBlue transition-all">
              {!hasDrawn && (
                <div className="absolute inset-0 pointer-events-none flex flex-col items-center justify-center text-slate-400">
                  <FileSignature className="w-10 h-10 mb-1 opacity-30" />
                  <span className="text-xs font-extrabold uppercase tracking-wider opacity-60">Sign Here</span>
                </div>
              )}
              <canvas
                ref={canvasRef}
                width={700}
                height={160}
                onMouseDown={startDrawing}
                onMouseMove={draw}
                onMouseUp={stopDrawing}
                onMouseLeave={stopDrawing}
                onTouchStart={startDrawing}
                onTouchMove={draw}
                onTouchEnd={stopDrawing}
                className="w-full h-40 bg-transparent cursor-crosshair touch-none"
              />
            </div>
            {hasDrawn && (
              <p className="text-[11px] text-emerald-600 font-bold mt-1.5 flex items-center gap-1">
                <CheckCircle className="w-3.5 h-3.5" /> Digital signature captured successfully!
              </p>
            )}
          </div>

          {/* Form Action Buttons */}
          <div className="flex flex-wrap items-center justify-end gap-3 pt-6 border-t border-slate-100">
            <button
              type="button"
              onClick={handleClearForm}
              className="px-5 py-3 rounded-xl border border-slate-200 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold text-xs transition-all flex items-center gap-1.5"
            >
              <Eraser className="w-4 h-4" /> Clear
            </button>

            <button
              type="button"
              onClick={() => handlePrint(null)}
              className="px-5 py-3 rounded-xl border border-amber-300 bg-amber-50 hover:bg-amber-100 text-amber-800 font-bold text-xs transition-all flex items-center gap-1.5"
            >
              <Printer className="w-4 h-4" /> Print Pronote Preview
            </button>

            <button
              type="submit"
              className="px-7 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-corpBlue hover:from-blue-700 hover:to-blue-900 text-white font-extrabold text-xs shadow-lg hover:shadow-xl transition-all flex items-center gap-2"
            >
              <Save className="w-4 h-4" /> Save Promissory Note
            </button>
          </div>

        </form>
      </div>

      {/* Promissory Notes History & Management Table */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <FileText className="w-6 h-6 text-corpBlue" /> Issued Promissory Notes ({pronotes.length})
          </h2>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead className="bg-slate-50 border-b border-slate-200 text-xs font-bold text-slate-500 uppercase tracking-wider">
                <tr>
                  <th className="p-4">Pronote ID</th>
                  <th className="p-4">Member Name</th>
                  <th className="p-4">Chit Scheme</th>
                  <th className="p-4 text-right">Loan Amount</th>
                  <th className="p-4 text-right">Repayment</th>
                  <th className="p-4 text-center">Due Date</th>
                  <th className="p-4 text-center">Status</th>
                  <th className="p-4 text-center">Signature</th>
                  <th className="p-4 text-center">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-150 text-xs font-medium text-slate-700">
                {pronotes.length === 0 ? (
                  <tr>
                    <td colSpan="9" className="p-8 text-center text-slate-400 font-medium">
                      No Promissory Notes created yet. Fill out the form above to generate one.
                    </td>
                  </tr>
                ) : (
                  pronotes.map((note) => (
                    <tr key={note.id} className="hover:bg-slate-50 transition-colors">
                      <td className="p-4 font-mono font-bold text-corpBlue">{note.pronote_id}</td>
                      <td className="p-4 font-bold text-slate-900">{note.member_name}</td>
                      <td className="p-4 text-slate-600">{note.chit_name || 'General Security'}</td>
                      <td className="p-4 text-right font-extrabold text-slate-900">
                        ₹{note.loan_amount?.toLocaleString('en-IN')}
                      </td>
                      <td className="p-4 text-right font-extrabold text-emerald-700">
                        ₹{note.repayment_amount?.toLocaleString('en-IN')}
                      </td>
                      <td className="p-4 text-center font-mono">
                        {note.due_date ? format(new Date(note.due_date), 'dd MMM yyyy') : 'N/A'}
                      </td>
                      <td className="p-4 text-center">
                        <select
                          value={note.status}
                          onChange={(e) => handleStatusChange(note.id, e.target.value)}
                          className={`px-2.5 py-1 rounded-full text-[11px] font-extrabold border uppercase tracking-wider outline-none cursor-pointer ${
                            note.status === 'pending_signature'
                              ? 'bg-amber-100 text-amber-900 border-amber-300'
                              : note.status === 'active'
                              ? 'bg-blue-50 text-blue-800 border-blue-300'
                              : note.status === 'paid'
                              ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
                              : 'bg-red-50 text-red-800 border-red-300'
                          }`}
                        >
                          <option value="pending_signature">Pending Signature</option>
                          <option value="active">Active</option>
                          <option value="paid">Paid</option>
                          <option value="overdue">Overdue</option>
                        </select>
                      </td>
                      <td className="p-4 text-center">
                        {note.signature ? (
                          <img
                            src={note.signature}
                            alt="Signature"
                            className="h-7 max-w-[80px] object-contain border border-slate-200 bg-white rounded p-0.5 mx-auto"
                          />
                        ) : (
                          <span className="text-slate-400 italic">None</span>
                        )}
                      </td>
                      <td className="p-4 text-center">
                        <div className="flex items-center justify-center gap-2">
                          <button
                            onClick={() => handlePrint(note)}
                            className="p-2 bg-blue-50 text-corpBlue hover:bg-blue-100 rounded-xl border border-blue-200 font-bold transition-all"
                            title="View & Print Official Pronote"
                          >
                            <Printer className="w-4 h-4" />
                          </button>
                          <button
                            onClick={() => handleDeletePronote(note.id)}
                            className="p-2 bg-red-50 text-red-600 hover:bg-red-100 rounded-xl border border-red-200 font-bold transition-all"
                            title="Delete Pronote"
                          >
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Printable Official Promissory Note Modal */}
      {selectedPronoteForPrint && (
        <div 
          onClick={() => setSelectedPronoteForPrint(null)}
          className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto cursor-pointer"
        >
          <div 
            onClick={(e) => e.stopPropagation()} 
            className="bg-white rounded-3xl w-full max-w-3xl shadow-2xl border border-slate-200 overflow-hidden my-8 animate-fade-in font-serif cursor-default"
          >
            
            {/* Modal Header Bar */}
            <div className="px-6 py-4 bg-slate-900 text-white flex justify-between items-center font-sans print:hidden">
              <div className="flex items-center gap-2">
                <FileSignature className="w-5 h-5 text-amber-400" />
                <h3 className="font-bold text-sm">Official Promissory Note Legal Document</h3>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => window.print()}
                  className="px-4 py-1.5 bg-amber-500 hover:bg-amber-600 text-slate-950 font-extrabold rounded-lg text-xs flex items-center gap-1.5 transition-all shadow-sm"
                >
                  <Printer className="w-3.5 h-3.5" /> Print Now
                </button>
                <button
                  onClick={() => setSelectedPronoteForPrint(null)}
                  className="px-3 py-1.5 bg-red-600/80 hover:bg-red-600 text-white font-bold rounded-lg text-xs flex items-center gap-1 transition-all"
                >
                  <X className="w-4 h-4" /> Close Document
                </button>
              </div>
            </div>

            {/* Legal Document Content */}
            <div className="printable-pronote-area p-8 sm:p-12 space-y-6 text-slate-900 leading-relaxed border-8 border-double border-slate-300 m-4 rounded-xl bg-amber-50/20">
              
              {/* Document Header */}
              <div className="text-center border-b-2 border-slate-900 pb-6">
                <h1 className="text-3xl sm:text-4xl font-black uppercase tracking-wider text-slate-950 mb-1">
                  PROMISSORY NOTE
                </h1>
                <p className="text-sm font-sans font-bold tracking-widest text-slate-600 uppercase">
                  Secure Chit Fund Management System
                </p>
                <div className="flex justify-between items-center mt-6 text-xs font-sans font-semibold text-slate-600">
                  <p>Pronote ID: <strong className="font-mono text-slate-900">{selectedPronoteForPrint.pronote_id}</strong></p>
                  <p>Date of Issue: <strong className="text-slate-900">{selectedPronoteForPrint.issue_date}</strong></p>
                  <p>Place: <strong>Tamil Nadu, India</strong></p>
                </div>
              </div>

              {/* Amount Stamp Box */}
              <div className="flex justify-between items-center bg-amber-100/60 p-4 rounded-xl border border-amber-300 font-sans">
                <div>
                  <span className="text-[10px] text-amber-900 font-bold uppercase tracking-wider block">Principal Loan Amount</span>
                  <span className="text-2xl font-black text-slate-950">
                    ₹{parseFloat(selectedPronoteForPrint.loan_amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </span>
                </div>
                <div className="text-right">
                  <span className="text-[10px] text-amber-900 font-bold uppercase tracking-wider block">Total Repayment Due</span>
                  <span className="text-2xl font-black text-emerald-900">
                    ₹{parseFloat(selectedPronoteForPrint.repayment_amount || selectedPronoteForPrint.loan_amount || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                  </span>
                </div>
              </div>

              {/* Legal Undertaking Text */}
              <div className="text-sm sm:text-base text-justify space-y-4 font-serif">
                <p>
                  On Demand, I, <strong className="underline decoration-slate-400 font-bold text-slate-950">{selectedPronoteForPrint.member_name}</strong>, residing at the registered address associated with Chit Member Account, promise to pay <strong>SECURE CHIT FUND ADMINISTRATION</strong> or order, the sum of <strong>Rupees {parseFloat(selectedPronoteForPrint.loan_amount || 0).toLocaleString('en-IN')} Only</strong> with interest thereon at the rate of <strong>{selectedPronoteForPrint.interest_rate || 0}%</strong> per annum from the date hereof until full payment is received.
                </p>
                <p>
                  This Promissory Note is executed towards security for the Chit Fund Scheme: <strong className="font-sans font-bold text-slate-950">{selectedPronoteForPrint.chit_name || 'General Security'}</strong>. The full repayment shall be cleared on or before <strong className="font-sans font-bold text-slate-950">{selectedPronoteForPrint.due_date}</strong>.
                </p>
                {selectedPronoteForPrint.purpose && (
                  <p className="text-xs italic text-slate-600 font-sans">
                    <strong>Purpose/Remarks:</strong> {selectedPronoteForPrint.purpose}
                  </p>
                )}
              </div>

              {/* Signatures & Seal Section */}
              <div className="pt-12 grid grid-cols-2 gap-8 items-end font-sans">
                <div className="text-center border-t border-slate-400 pt-3">
                  <div className="h-16 flex items-center justify-center">
                    <ShieldCheck className="w-12 h-12 text-corpBlue opacity-80" />
                  </div>
                  <p className="text-xs font-bold text-slate-900 uppercase mt-2">Authorized Officer Signature</p>
                  <p className="text-[10px] text-slate-500 font-medium">Secure Chit Fund Administration</p>
                </div>

                <div className="text-center border-t border-slate-400 pt-3">
                  <div className="h-16 flex items-center justify-center">
                    {selectedPronoteForPrint.signature ? (
                      <img
                        src={selectedPronoteForPrint.signature}
                        alt="Member Signature"
                        className="max-h-14 max-w-full object-contain"
                      />
                    ) : (
                      <span className="text-xs text-slate-400 italic">Signature Pending / Not Recorded</span>
                    )}
                  </div>
                  <p className="text-xs font-bold text-slate-900 uppercase mt-2">
                    {selectedPronoteForPrint.member_name}
                  </p>
                  <p className="text-[10px] text-slate-500 font-medium">Member Signature (Maker)</p>
                </div>
              </div>

              <div className="text-center pt-6 border-t border-slate-200 text-[10px] text-slate-400 font-sans">
                <p>Legal Security Document • Governed under Negotiable Instruments Act • Secure Chit Fund</p>
              </div>

            </div>

            {/* Modal Bottom Exit Footer */}
            <div className="px-6 py-3 bg-slate-100 border-t border-slate-200 text-right font-sans print:hidden">
              <button
                onClick={() => setSelectedPronoteForPrint(null)}
                className="px-5 py-2 bg-slate-700 hover:bg-slate-800 text-white font-bold rounded-xl text-xs transition-colors"
              >
                Close & Exit Preview
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};

export default PronoteManagement;

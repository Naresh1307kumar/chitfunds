import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { ArrowLeft, User, Phone, Mail, ShieldCheck, FileText, CheckCircle, XCircle, Clock, AlertTriangle } from 'lucide-react';
import toast from 'react-hot-toast';

const MemberDetails = () => {
  const { id } = useParams();
  const [member, setMember] = useState(null);
  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);
  const [selectedDoc, setSelectedDoc] = useState(null);
  const navigate = useNavigate();

  const fetchMember = async () => {
    try {
      const res = await api.get(`/api/v1/admin/members/${id}`);
      setMember(res.data);
    } catch (err) {
      toast.error('Failed to load member details');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMember();
  }, [id]);

  const handleStatusChange = async (status) => {
    setUpdating(true);
    try {
      await api.put(`/api/v1/admin/members/${id}/status`, { status });
      toast.success(`Member status updated to ${status}`);
      fetchMember();
    } catch (err) {
      toast.error('Failed to update status');
    } finally {
      setUpdating(false);
    }
  };

  const handleKycStatusChange = async (kyc_status) => {
    setUpdating(true);
    try {
      await api.put(`/api/v1/admin/members/${id}/kyc`, { kyc_status });
      toast.success(`KYC status updated to ${kyc_status}`);
      fetchMember();
    } catch (err) {
      toast.error('Failed to update KYC status');
    } finally {
      setUpdating(false);
    }
  };

  const handleDeleteMember = async () => {
    if (!window.confirm('Are you sure you want to permanently delete this member? This action cannot be undone.')) return;
    setUpdating(true);
    try {
      await api.delete(`/api/v1/admin/members/${id}`);
      toast.success('Member deleted permanently');
      navigate('/admin/members');
    } catch (err) {
      toast.error('Failed to delete member');
    } finally {
      setUpdating(false);
    }
  };

  const handleUnlock = async () => {
    setUpdating(true);
    try {
      await api.post(`/api/v1/admin/members/${id}/unlock`);
      toast.success('Member account unlocked');
      fetchMember();
    } catch (err) {
      toast.error('Failed to unlock member');
    } finally {
      setUpdating(false);
    }
  };

  if (loading) return <div className="text-center py-10">Loading member details...</div>;
  if (!member) return <div className="p-10 text-center text-red-500">Member not found.</div>;

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <div className="flex items-center gap-4 mb-6">
        <button 
          onClick={() => navigate('/admin/members')}
          className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
          title="Go Back"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <span className="text-sm font-semibold text-slate-600">Back to Members List</span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Profile Card */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 text-center">
            <div className="w-24 h-24 rounded-full bg-blue-100 flex items-center justify-center text-blue-700 font-bold text-3xl mx-auto mb-4">
              {member.name.charAt(0).toUpperCase()}
            </div>
            <h2 className="text-xl font-bold text-gray-900">{member.name}</h2>
            <p className="text-gray-500 text-sm mb-4">Member #{member.id.toString().padStart(4, '0')}</p>
            
            <div className="flex justify-center gap-2 mb-6">
              {member.status === 'active' ? (
                <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-xs font-bold">ACTIVE</span>
              ) : member.status === 'pending' ? (
                <span className="px-3 py-1 bg-yellow-100 text-yellow-700 rounded-full text-xs font-bold">PENDING APPROVAL</span>
              ) : (
                <span className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-xs font-bold uppercase">{member.status}</span>
              )}
            </div>

            <div className="space-y-3 text-left border-t border-gray-100 pt-6">
              <div className="flex items-center gap-3">
                <Mail className="w-5 h-5 text-gray-400" />
                <span className="text-sm text-gray-700">{member.email}</span>
              </div>
              <div className="flex items-center gap-3">
                <Phone className="w-5 h-5 text-gray-400" />
                <span className="text-sm text-gray-700">{member.phone}</span>
              </div>
              <div className="flex items-center gap-3">
                <ShieldCheck className="w-5 h-5 text-gray-400" />
                <span className="text-sm text-gray-700">Aadhar: {member.aadhar_number || 'N/A'}</span>
              </div>
            </div>

            <div className="mt-8 pt-6 border-t border-gray-100">
              <h3 className="text-sm font-bold text-gray-900 mb-3 text-left">Update Login Status</h3>
              {member.kyc_status !== 'verified' ? (
                <div className="text-xs text-yellow-700 bg-yellow-50 p-3 rounded-lg border border-yellow-200">
                  <span className="font-bold">Action Restricted:</span> Approve the member's KYC documents to unlock login status controls.
                </div>
              ) : (
                <div className="grid grid-cols-2 gap-2">
                  {member.status === 'pending' || member.status === 'suspended' ? (
                    <button onClick={() => handleStatusChange('active')} disabled={updating} className="py-2 bg-green-600 text-white rounded-lg text-sm font-semibold hover:bg-green-700">
                      Approve
                    </button>
                  ) : (
                    <button onClick={() => handleStatusChange('suspended')} disabled={updating} className="py-2 bg-orange-600 text-white rounded-lg text-sm font-semibold hover:bg-orange-700">
                      Suspend
                    </button>
                  )}
                  <button onClick={() => handleStatusChange('rejected')} disabled={updating} className="py-2 bg-red-100 text-red-600 rounded-lg text-sm font-semibold hover:bg-red-200">
                    Reject
                  </button>
                </div>
              )}
              <div className="mt-3">
                <button onClick={handleDeleteMember} disabled={updating} className="w-full py-2 bg-white border border-red-200 text-red-600 rounded-lg text-sm font-semibold hover:bg-red-50 transition-colors">
                  Delete Member
                </button>
              </div>
              
              {member.failed_login_attempts >= 5 && (
                <div className="mt-4 pt-4 border-t border-red-100 bg-red-50 p-4 rounded-xl">
                  <h3 className="text-sm font-bold text-red-900 mb-2 flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4" /> Account Locked
                  </h3>
                  <p className="text-xs text-red-700 mb-3">Due to multiple failed login attempts, this account is locked.</p>
                  <button onClick={handleUnlock} disabled={updating} className="w-full py-2 bg-red-600 text-white rounded-lg text-sm font-semibold hover:bg-red-700 transition-colors">
                    Unlock Account
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column: Details */}
        <div className="lg:col-span-2 space-y-6">
          {/* KYC Section */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <FileText className="w-5 h-5 text-blue-600" /> KYC Documents
              </h3>
              <div>
                {member.kyc_status === 'verified' && <span className="text-green-600 font-bold text-sm flex items-center gap-1"><CheckCircle className="w-4 h-4"/> Verified</span>}
                {member.kyc_status === 'pending' && <span className="text-yellow-600 font-bold text-sm flex items-center gap-1"><Clock className="w-4 h-4"/> Pending Review</span>}
                {member.kyc_status === 'rejected' && <span className="text-red-600 font-bold text-sm flex items-center gap-1"><XCircle className="w-4 h-4"/> Rejected</span>}
                {member.kyc_status === 'not_submitted' && <span className="text-gray-400 font-bold text-sm flex items-center gap-1"><AlertTriangle className="w-4 h-4"/> Not Submitted</span>}
              </div>
            </div>

            {member.kyc_documents.length === 0 ? (
              <div className="p-6 bg-gray-50 rounded-xl text-center text-sm text-gray-500 border border-dashed border-gray-300">
                Member has not uploaded any KYC documents yet.
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-4 mb-6">
                {member.kyc_documents.map(doc => (
                  <div key={doc.id} className="border rounded-xl p-4 flex flex-col items-center cursor-pointer hover:border-blue-500 transition-colors"
                       onClick={() => setSelectedDoc(doc.file_path)}>
                    <div className="w-full h-32 bg-gray-100 rounded-lg mb-3 flex items-center justify-center overflow-hidden">
                       <img src={`http://localhost:8000/${doc.file_path}`} alt={doc.document_type} className="object-cover w-full h-full" />
                    </div>
                    <p className="font-semibold text-sm capitalize">{doc.document_type.replace('_', ' ')}</p>
                    <p className={`text-xs mt-1 ${doc.status === 'verified' ? 'text-green-600' : doc.status === 'rejected' ? 'text-red-600' : 'text-yellow-600'}`}>
                      Status: {doc.status}
                    </p>
                  </div>
                ))}
              </div>
            )}

            {/* KYC Actions */}
            {member.kyc_status === 'pending' && (
              <div className="flex gap-3 pt-6 border-t border-gray-100">
                <button onClick={() => handleKycStatusChange('verified')} disabled={updating} className="flex-1 py-3 bg-blue-600 text-white rounded-xl text-sm font-semibold hover:bg-blue-700 transition-colors">
                  Verify All KYC Documents
                </button>
                <button onClick={() => handleKycStatusChange('rejected')} disabled={updating} className="flex-1 py-3 bg-red-50 text-red-600 rounded-xl text-sm font-semibold hover:bg-red-100 transition-colors">
                  Reject KYC
                </button>
              </div>
            )}
          </div>

          {/* Guarantor Section */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-bold text-gray-900 flex items-center gap-2 mb-6">
              <User className="w-5 h-5 text-blue-600" /> Guarantor Details
            </h3>
            
            {member.guarantors.length === 0 ? (
              <div className="p-6 bg-gray-50 rounded-xl text-center text-sm text-gray-500 border border-dashed border-gray-300">
                No guarantor details provided yet.
              </div>
            ) : (
              <div className="grid grid-cols-2 gap-4">
                {member.guarantors.map(g => (
                  <div key={g.id} className="col-span-2 md:col-span-1 bg-gray-50 rounded-xl p-4 border border-gray-100">
                    <p className="font-bold text-gray-900">{g.name}</p>
                    <p className="text-sm text-gray-500 mb-3">{g.relationship_to_member}</p>
                    <div className="space-y-1 text-sm">
                      <p><span className="text-gray-500">Phone:</span> {g.phone}</p>
                      <p><span className="text-gray-500">Aadhar:</span> {g.aadhar_number}</p>
                      <p><span className="text-gray-500">Address:</span> {g.address}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Lightbox */}
      {selectedDoc && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4" onClick={() => setSelectedDoc(null)}>
          <div className="relative max-w-4xl max-h-full">
            <button className="absolute -top-10 right-0 text-white hover:text-gray-300 font-bold" onClick={() => setSelectedDoc(null)}>
              Close
            </button>
            <img src={`http://localhost:8000/${selectedDoc}`} alt="Document" className="max-w-full max-h-[80vh] object-contain rounded-lg shadow-2xl" />
          </div>
        </div>
      )}
    </div>
  );
};

export default MemberDetails;

import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { ShieldCheck, Upload, FileText, CheckCircle, AlertTriangle , ArrowLeft } from 'lucide-react';
import toast from 'react-hot-toast';

const KYCUpload = () => {
  const navigate = useNavigate();
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);

  // Document types we need
  const requiredDocs = [
    { type: 'aadhar_front', label: 'Aadhar Card (Front)' },
    { type: 'aadhar_back', label: 'Aadhar Card (Back)' },
    { type: 'pan_card', label: 'PAN Card' },
    { type: 'passport_photo', label: 'Passport Size Photo' }
  ];

  const fetchKyc = async () => {
    try {
      const res = await api.get('/api/v1/member/kyc');
      setDocuments(res.data);
    } catch (err) {
      toast.error('Failed to load KYC status');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchKyc();
  }, []);

  const handleFileUpload = async (e, type) => {
    const file = e.target.files[0];
    if (!file) return;

    // Validate size (e.g. 5MB limit)
    if (file.size > 5 * 1024 * 1024) {
      toast.error('File size should be less than 5MB');
      return;
    }

    const formData = new FormData();
    formData.append('document_type', type);
    formData.append('file', file);

    setUploading(true);
    try {
      await api.post('/api/v1/member/kyc', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      toast.success(`${type.replace('_', ' ')} uploaded successfully`);
      fetchKyc();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to upload document');
    } finally {
      setUploading(false);
    }
  };

  const getDocStatus = (type) => {
    return documents.find(d => d.document_type === type);
  };

  const allUploaded = requiredDocs.every(req => getDocStatus(req.type));

  if (loading) return <div className="p-10 text-center">Loading KYC Details...</div>;

  return (
    <div className="max-w-4xl mx-auto px-6 py-10">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
        <div className="flex items-center gap-4 mb-6 pb-6 border-b border-gray-100">
          <button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-355 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
            <ShieldCheck className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white mr-2"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <h2 className="text-2xl font-bold text-gray-900">KYC Verification</h2>
            <p className="text-gray-500 text-sm">Upload your identity documents to complete verification</p>
          </div>
        </div>

        {!allUploaded && (
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-3 rounded-xl flex items-start gap-3 mb-8">
            <AlertTriangle className="w-5 h-5 flex-shrink-0 mt-0.5" />
            <div className="text-sm">
              <p className="font-bold">Action Required</p>
              <p>Please upload all the mandatory documents below to proceed.</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {requiredDocs.map(req => {
            const uploadedDoc = getDocStatus(req.type);
            return (
              <div key={req.type} className={`border rounded-xl p-5 transition-all ${uploadedDoc ? 'border-green-200 bg-green-50/30' : 'border-gray-200 bg-gray-50'}`}>
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-2">
                    <FileText className="w-5 h-5 text-gray-400" />
                    <span className="font-semibold text-gray-800">{req.label}</span>
                  </div>
                  {uploadedDoc && (
                    <span className={`text-xs font-bold px-2 py-1 rounded-full ${uploadedDoc.status === 'verified' ? 'bg-green-100 text-green-700' : uploadedDoc.status === 'rejected' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>
                      {uploadedDoc.status.toUpperCase()}
                    </span>
                  )}
                </div>

                {uploadedDoc && uploadedDoc.status === 'rejected' && (
                  <p className="text-xs text-red-600 mb-3 bg-red-50 p-2 rounded">
                    Reason: {uploadedDoc.rejection_reason || 'Document unclear/invalid. Please re-upload.'}
                  </p>
                )}

                {uploadedDoc && uploadedDoc.status === 'verified' ? (
                  <div className="flex items-center gap-2 text-sm text-green-600 font-semibold bg-white p-3 rounded-lg border border-green-100">
                    <CheckCircle className="w-5 h-5" /> Document Verified
                  </div>
                ) : (
                  <div>
                    <input 
                      type="file" 
                      id={`file-${req.type}`} 
                      className="hidden" 
                      accept="image/*,.pdf"
                      onChange={(e) => handleFileUpload(e, req.type)}
                      disabled={uploading}
                    />
                    <label 
                      htmlFor={`file-${req.type}`}
                      className={`flex flex-col items-center justify-center w-full h-32 border-2 border-dashed rounded-lg cursor-pointer bg-white hover:bg-gray-50 transition-colors ${uploadedDoc && uploadedDoc.status !== 'rejected' ? 'border-blue-300' : 'border-gray-300'}`}
                    >
                      <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        <Upload className={`w-8 h-8 mb-2 ${uploadedDoc ? 'text-blue-500' : 'text-gray-400'}`} />
                        <p className="text-sm text-gray-500">
                          {uploading ? 'Uploading...' : uploadedDoc ? 'Click to replace document' : 'Click to upload'}
                        </p>
                      </div>
                    </label>
                  </div>
                )}
              </div>
            );
          })}
        </div>

        <div className="mt-8 pt-6 border-t border-gray-100 flex justify-end">
          <button 
            onClick={() => navigate('/member/dashboard')}
            className="px-6 py-2.5 bg-gray-100 text-gray-700 font-semibold rounded-xl hover:bg-gray-200 transition-colors"
          >
            {allUploaded ? 'Back to Dashboard' : 'Upload Later'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default KYCUpload;

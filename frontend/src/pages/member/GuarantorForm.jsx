import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';
import { ArrowLeft, UserPlus, User, Phone, ShieldCheck, MapPin, Heart, ArrowRight } from 'lucide-react';
import toast from 'react-hot-toast';

const GuarantorForm = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState({
    name: '',
    phone: '',
    aadhar_number: '',
    relationship_to_member: '',
    address: ''
  });

  useEffect(() => {
    const fetchGuarantor = async () => {
      try {
        const res = await api.get('/api/v1/member/profile/guarantor');
        if (res.data && res.data.length > 0) {
          setForm(res.data[0]);
        }
      } catch (err) {
        // It's ok if not found
      } finally {
        setLoading(false);
      }
    };
    fetchGuarantor();
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post('/api/v1/member/profile/guarantor', form);
      toast.success('Guarantor details saved successfully');
      navigate('/member/dashboard');
    } catch (err) {
      toast.error('Failed to save details');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="p-10 text-center">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto px-6 py-10">
      <div className="bg-white rounded-2xl shadow-sm border border-gray-200 p-8">
        <div className="flex items-center gap-4 mb-8 pb-6 border-b border-gray-100">
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">
            <button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white mr-2"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <UserPlus className="w-6 h-6 text-blue-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Guarantor Details</h2>
            <p className="text-gray-500 text-sm">Add a guarantor for your chit plans</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Name */}
            <div>
              <label className="block text-sm font-semibold mb-2 text-gray-700">Full Name</label>
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input type="text" name="name" value={form.name} onChange={handleChange} required
                  className="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-xl border border-gray-200 focus:border-blue-500 focus:bg-white outline-none transition-all" />
              </div>
            </div>

            {/* Phone */}
            <div>
              <label className="block text-sm font-semibold mb-2 text-gray-700">Phone Number</label>
              <div className="relative">
                <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input type="text" name="phone" value={form.phone} onChange={handleChange} required maxLength={10}
                  className="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-xl border border-gray-200 focus:border-blue-500 focus:bg-white outline-none transition-all" />
              </div>
            </div>

            {/* Aadhar */}
            <div>
              <label className="block text-sm font-semibold mb-2 text-gray-700">Aadhar Number</label>
              <div className="relative">
                <ShieldCheck className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input type="text" name="aadhar_number" value={form.aadhar_number} onChange={handleChange} required maxLength={12}
                  className="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-xl border border-gray-200 focus:border-blue-500 focus:bg-white outline-none transition-all" />
              </div>
            </div>

            {/* Relationship */}
            <div>
              <label className="block text-sm font-semibold mb-2 text-gray-700">Relationship</label>
              <div className="relative">
                <Heart className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <select name="relationship_to_member" value={form.relationship_to_member} onChange={handleChange} required
                  className="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-xl border border-gray-200 focus:border-blue-500 focus:bg-white outline-none transition-all appearance-none">
                  <option value="" disabled>Select relation...</option>
                  <option value="Father">Father</option>
                  <option value="Mother">Mother</option>
                  <option value="Spouse">Spouse</option>
                  <option value="Sibling">Sibling</option>
                  <option value="Friend">Friend</option>
                  <option value="Other">Other</option>
                </select>
              </div>
            </div>

            {/* Address */}
            <div className="md:col-span-2">
              <label className="block text-sm font-semibold mb-2 text-gray-700">Full Address</label>
              <div className="relative">
                <MapPin className="absolute left-4 top-4 w-5 h-5 text-gray-400" />
                <textarea name="address" value={form.address} onChange={handleChange} required rows={3}
                  className="w-full pl-12 pr-4 py-3 bg-gray-50 rounded-xl border border-gray-200 focus:border-blue-500 focus:bg-white outline-none transition-all resize-none"></textarea>
              </div>
            </div>
          </div>

          <div className="pt-6 border-t border-gray-100 flex justify-end gap-3">
            <button type="button" onClick={() => navigate('/member/dashboard')}
              className="px-6 py-3 bg-gray-100 text-gray-700 font-semibold rounded-xl hover:bg-gray-200 transition-colors">
              Cancel
            </button>
            <button type="submit" disabled={saving}
              className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-xl hover:bg-blue-700 transition-colors flex items-center gap-2">
              {saving ? 'Saving...' : <>Save Details <ArrowRight className="w-4 h-4" /></>}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default GuarantorForm;

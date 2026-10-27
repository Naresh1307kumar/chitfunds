import React, { useState, useEffect } from 'react';
import { ShieldCheck, Plus, Pencil, Trash2, Eye, Info, Users, Clock, Edit2, Trophy , ArrowLeft } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import api from '../../services/api';

const ManagePlans = () => {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingPlan, setEditingPlan] = useState(null);
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    plan_name: '',
    plan_type: 'silver',
    chit_type: 'lucky_draw',
    monthly_amount: '',
    total_members: '',
    duration_months: '',
    commission_rate: 5.0,
    start_date: ''
  });

  const fetchPlans = async () => {
    try {
      const res = await api.get('/api/v1/admin/plans');
      setPlans(res.data);
    } catch (error) {
      toast.error('Failed to load plans');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlans();
  }, []);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const openCreateModal = () => {
    setEditingPlan(null);
    setFormData({
      plan_name: '', plan_type: 'silver', chit_type: 'lucky_draw', monthly_amount: '', total_members: '',
      duration_months: '', commission_rate: 5.0, start_date: ''
    });
    setIsModalOpen(true);
  };

  const openEditModal = (plan) => {
    setEditingPlan(plan);
    setFormData({
      plan_name: plan.plan_name,
      plan_type: plan.plan_type,
      chit_type: plan.chit_type || 'lucky_draw',
      monthly_amount: plan.monthly_amount,
      total_members: plan.total_members,
      duration_months: plan.duration_months,
      commission_rate: plan.commission_rate,
      start_date: plan.start_date
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingPlan) {
        await api.put(`/api/v1/admin/plans/${editingPlan.id}`, formData);
        toast.success('Plan updated successfully');
      } else {
        await api.post('/api/v1/admin/plans', formData);
        toast.success('Plan created successfully');
      }
      setIsModalOpen(false);
      fetchPlans();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'An error occurred');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this plan?')) return;
    try {
      await api.delete(`/api/v1/admin/plans/${id}`);
      toast.success('Plan deleted successfully');
      fetchPlans();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to delete plan');
    }
  };

  const handleStartPlan = async (id) => {
    if (!window.confirm('Are you sure you want to start this plan? Month 1 installments will be generated.')) return;
    try {
      await api.post(`/api/v1/admin/plans/${id}/start`);
      toast.success('Plan started successfully!');
      fetchPlans();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to start plan');
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-10">
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
            <h1 className="text-2xl sm:text-3xl font-bold" style={{ color: '#1A2B49' }}>Manage Chit Plans</h1>
            <p className="text-gray-500 text-xs sm:text-sm mt-0.5">Create and manage chit fund schemes</p>
          </div>
        </div>
        <button onClick={openCreateModal} className="w-full sm:w-auto flex items-center justify-center gap-2 bg-blue-600 text-white px-5 py-2.5 rounded-xl font-semibold hover:bg-blue-700 transition-colors shadow-sm">
          <Plus className="w-5 h-5" /> New Plan
        </button>
      </div>

      {loading ? (
        <div className="text-center py-10">Loading plans...</div>
      ) : plans.length === 0 ? (
        <div className="bg-white border rounded-2xl p-10 text-center text-gray-500 shadow-sm">
          No plans available. Create your first chit plan!
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {plans.map(plan => (
            <div key={plan.id} className="bg-white border rounded-2xl p-6 shadow-sm hover:shadow-md transition-shadow relative">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-bold text-lg" style={{ color: '#1A2B49' }}>{plan.plan_name}</h3>
                  <span className={`inline-block mt-1 px-2.5 py-0.5 rounded-full text-xs font-semibold ${
                    plan.status === 'active' ? 'bg-green-100 text-green-700' :
                    plan.status === 'completed' ? 'bg-blue-100 text-blue-700' :
                    'bg-yellow-100 text-yellow-700'
                  }`}>
                    {plan.status.toUpperCase()}
                  </span>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => openEditModal(plan)} className="p-1.5 text-gray-400 hover:text-blue-600 bg-gray-50 rounded-lg"><Edit2 className="w-4 h-4" /></button>
                  <button onClick={() => handleDelete(plan.id)} className="p-1.5 text-gray-400 hover:text-red-600 bg-gray-50 rounded-lg"><Trash2 className="w-4 h-4" /></button>
                </div>
              </div>
              
              <div className="space-y-2 mb-6">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Monthly Amt:</span>
                  <span className="font-semibold text-gray-900">₹{plan.monthly_amount}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Total Value:</span>
                  <span className="font-semibold text-gray-900">₹{plan.total_value}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Duration:</span>
                  <span className="font-semibold text-gray-900">{plan.duration_months} Months</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Members:</span>
                  <span className="font-semibold text-gray-900">{plan.current_members} / {plan.total_members}</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-500">Chit Type:</span>
                  <span className="font-semibold text-blue-600">{plan.chit_type === 'auction' ? 'Auction' : 'Lucky Draw'}</span>
                </div>
              </div>
              
              <div className="flex flex-col gap-2">
                <button onClick={() => navigate(`/admin/plans/${plan.id}/members`)} className="w-full py-2.5 bg-gray-50 hover:bg-gray-100 text-blue-600 font-semibold rounded-xl text-sm transition-colors flex items-center justify-center gap-2">
                  <Users className="w-4 h-4" /> Manage Members
                </button>
                {plan.status === 'draft' && (
                  <button 
                    onClick={() => handleStartPlan(plan.id)}
                    disabled={plan.current_members < plan.total_members}
                    className="w-full py-2.5 bg-green-50 hover:bg-green-100 text-green-700 font-semibold rounded-xl text-sm transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <ShieldCheck className="w-4 h-4" /> Start Plan
                  </button>
                )}
                {plan.status === 'active' && (
                  <button onClick={() => navigate(`/admin/plans/${plan.id}/draws`)} className="w-full py-2.5 bg-yellow-50 hover:bg-yellow-100 text-yellow-700 font-semibold rounded-xl text-sm transition-colors flex items-center justify-center gap-2">
                    <Trophy className="w-4 h-4" /> Conduct Draw
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-3 sm:p-4">
          <div className="bg-white rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl">
            <div className="px-6 py-4 border-b flex justify-between items-center">
              <h2 className="text-xl font-bold">{editingPlan ? 'Edit Plan' : 'Create New Plan'}</h2>
              <button onClick={() => setIsModalOpen(false)} className="text-gray-400 hover:text-gray-700">✕</button>
            </div>
            <div className="p-6">
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-1">Plan Name</label>
                  <input type="text" name="plan_name" value={formData.plan_name} onChange={handleInputChange} required className="w-full px-4 py-2 border rounded-xl" placeholder="e.g., Deepavali 1L Scheme" />
                </div>
                <div>
                  <label className="block text-sm font-semibold text-gray-700 mb-1">Chit Type</label>
                  <select name="chit_type" value={formData.chit_type} onChange={handleInputChange} className="w-full px-4 py-2 border rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option value="lucky_draw">Lucky Draw</option>
                    <option value="auction">Auction</option>
                  </select>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Monthly Amount (₹)</label>
                    <input type="number" name="monthly_amount" value={formData.monthly_amount} onChange={handleInputChange} required className="w-full px-4 py-2 border rounded-xl" />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Total Members</label>
                    <input type="number" name="total_members" value={formData.total_members} onChange={handleInputChange} required className="w-full px-4 py-2 border rounded-xl" />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Duration (Months)</label>
                    <input type="number" name="duration_months" value={formData.duration_months} onChange={handleInputChange} required className="w-full px-4 py-2 border rounded-xl" />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Start Date</label>
                    <input type="date" name="start_date" value={formData.start_date} onChange={handleInputChange} required className="w-full px-4 py-2 border rounded-xl" />
                  </div>
                </div>
                <div className="pt-4 flex gap-3">
                  <button type="button" onClick={() => setIsModalOpen(false)} className="flex-1 py-2.5 border border-gray-300 rounded-xl font-semibold text-gray-700 hover:bg-gray-50">Cancel</button>
                  <button type="submit" className="flex-1 py-2.5 bg-blue-600 text-white rounded-xl font-semibold hover:bg-blue-700">{editingPlan ? 'Update Plan' : 'Create Plan'}</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ManagePlans;

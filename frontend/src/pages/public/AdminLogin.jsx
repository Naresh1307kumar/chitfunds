import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, Mail, Lock, Eye, EyeOff, ArrowRight, AlertCircle, User } from 'lucide-react';
import toast from 'react-hot-toast';
import ParticleBackground from '../../components/ParticleBackground';

const AdminLogin = () => {
  const { loginAdmin } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await loginAdmin(form.username, form.password);
      toast.success('Welcome, Admin!');
      navigate('/admin/dashboard');
    } catch (err) {
      let msg = 'Login failed. Please check your credentials.';
      if (err.response?.data?.detail) {
        if (Array.isArray(err.response.data.detail)) {
          msg = err.response.data.detail[0].msg.replace('Value error, ', '');
        } else {
          msg = err.response.data.detail;
        }
      }
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4 auth-animated-bg relative overflow-hidden">
      <ParticleBackground />
      <div className="relative w-full max-w-md auth-content">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-2xl" style={{ background: '#0F4C81' }}>
            <ShieldCheck className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-white text-2xl font-bold tracking-tight">SecureChit</h1>
          <p className="text-blue-300 text-sm mt-1">Administration Portal</p>
        </div>

        {/* Card */}
        <div className="bg-white rounded-3xl shadow-2xl p-10">
          <div className="text-center mb-8">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full text-xs font-semibold mb-4" style={{ background: '#FEF3C7', color: '#92400E' }}>
              <div className="w-2 h-2 rounded-full bg-yellow-500" />
              Admin Access Only
            </div>
            <h2 className="text-2xl font-bold" style={{ color: '#1A2B49' }}>Admin Login</h2>
            <p className="text-gray-500 text-sm mt-1">Authorized personnel only</p>
          </div>

          {error && (
            <div className="flex items-start gap-3 p-4 rounded-xl mb-6" style={{ background: '#FEF2F2', border: '1px solid #FECACA' }}>
              <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
              <p className="text-red-700 text-sm">{error}</p>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            {/* Username */}
            <div>
              <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>Admin Username</label>
              <div className="relative">
                <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  name="username"
                  value={form.username}
                  onChange={handleChange}
                  placeholder="Enter admin username"
                  required
                  className="w-full pl-12 pr-4 py-3.5 rounded-xl border text-sm outline-none transition-all"
                  style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                  onFocus={e => e.target.style.borderColor = '#1A2B49'}
                  onBlur={e => e.target.style.borderColor = '#DCE3EA'}
                />
              </div>
            </div>

            {/* Password */}
            <div>
              <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>Password</label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  value={form.password}
                  onChange={handleChange}
                  placeholder="Enter admin password"
                  required
                  className="w-full pl-12 pr-12 py-3.5 rounded-xl border text-sm outline-none transition-all"
                  style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                  onFocus={e => e.target.style.borderColor = '#1A2B49'}
                  onBlur={e => e.target.style.borderColor = '#DCE3EA'}
                />
                <button type="button" onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                  {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all"
              style={{ background: loading ? '#6B7280' : '#1A2B49' }}>
              {loading
                ? <><div className="w-5 h-5 border-2 border-white/40 border-t-white rounded-full animate-spin" />Signing in...</>
                : <>Access Dashboard <ArrowRight className="w-4 h-4" /></>}
            </button>
          </form>

          <p className="mt-6 text-center text-xs text-gray-400">
            Member?{' '}
            <a href="/login" className="hover:underline" style={{ color: '#0F4C81' }}>Login here</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default AdminLogin;

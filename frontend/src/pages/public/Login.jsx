import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, Mail, Lock, Eye, EyeOff, ArrowRight, ArrowLeft, AlertCircle, User } from 'lucide-react';
import toast from 'react-hot-toast';
import ParticleBackground from '../../components/ParticleBackground';

const Login = () => {
  const { loginMember } = useAuth();
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
      await loginMember(form.username, form.password);
      toast.success('Welcome back!');
      navigate('/member/dashboard');
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
    <div className="min-h-screen flex auth-animated-bg relative overflow-hidden">
      {/* Back to Home Arrow */}
      <button 
        onClick={() => navigate('/')} 
        className="absolute top-6 left-6 w-10 h-10 rounded-full bg-white shadow-md border border-slate-200 flex items-center justify-center text-slate-600 hover:text-corpBlue hover:border-corpBlue transition-all z-20 group"
      >
        <ArrowLeft className="w-5 h-5 group-hover:-translate-x-0.5 transition-transform" />
      </button>
      <ParticleBackground />
      
      {/* Left Panel */}
      <div className="hidden lg:flex lg:w-1/2 flex-col justify-center px-16 text-white auth-content">
        <div className="flex items-center gap-3 mb-10">
          <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
            <ShieldCheck className="w-7 h-7 text-white" />
          </div>
          <span className="text-2xl font-bold tracking-tight">SecureChit</span>
        </div>
        <h1 className="text-5xl font-bold leading-tight mb-6">
          Welcome Back to<br />
          <span style={{ color: '#C9A227' }}>SecureChit</span>
        </h1>
        <p className="text-blue-200 text-lg leading-relaxed mb-10">
          Access your chit fund dashboard, track your investments, and manage your payments securely.
        </p>
        <div className="space-y-4">
          {['100% Secure & Transparent', 'Real-time Payment Tracking', 'Instant Notifications'].map((item, i) => (
            <div key={i} className="flex items-center gap-3">
              <div className="w-6 h-6 rounded-full flex items-center justify-center" style={{ background: '#C9A227' }}>
                <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20"><path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" /></svg>
              </div>
              <span className="text-blue-100">{item}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Right Panel — Form */}
      <div className="w-full lg:w-1/2 flex items-center justify-center px-4 py-8 sm:px-6 sm:py-12 auth-content">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-3xl shadow-2xl p-6 sm:p-10">
            {/* Header */}
            <div className="flex items-center gap-3 mb-2 lg:hidden">
              <ShieldCheck className="w-7 h-7" style={{ color: '#0F4C81' }} />
              <span className="text-xl font-bold" style={{ color: '#1A2B49' }}>SecureChit</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold mb-1" style={{ color: '#1A2B49' }}>Member Login</h2>
            <p className="text-gray-500 mb-6 sm:mb-8 text-xs sm:text-sm">Sign in to your member account</p>

            {/* Error */}
            {error && (
              <div className="flex items-start gap-3 p-4 rounded-xl mb-6" style={{ background: '#FEF2F2', border: '1px solid #FECACA' }}>
                <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-5">
              {/* Username */}
              <div>
                <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>Username</label>
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    name="username"
                    value={form.username}
                    onChange={handleChange}
                    placeholder="Enter your username"
                    required
                    className="w-full pl-12 pr-4 py-3.5 rounded-xl border text-sm outline-none transition-all"
                    style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                    onFocus={e => e.target.style.borderColor = '#0F4C81'}
                    onBlur={e => e.target.style.borderColor = '#DCE3EA'}
                  />
                </div>
              </div>

              {/* Password */}
              <div>
                <div className="flex justify-between mb-2">
                  <label className="text-sm font-semibold" style={{ color: '#1A2B49' }}>Password</label>
                  <Link to="/forgot-password" className="text-sm font-semibold hover:underline" style={{ color: '#0F4C81' }}>
                    Forgot Password?
                  </Link>
                </div>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    name="password"
                    value={form.password}
                    onChange={handleChange}
                    placeholder="Enter your password"
                    required
                    className="w-full pl-12 pr-12 py-3.5 rounded-xl border text-sm outline-none transition-all"
                    style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                    onFocus={e => e.target.style.borderColor = '#0F4C81'}
                    onBlur={e => e.target.style.borderColor = '#DCE3EA'}
                  />
                  <button type="button" onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* Submit */}
              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all"
                style={{ background: loading ? '#93A8C4' : '#0F4C81' }}
              >
                {loading ? (
                  <><div className="w-5 h-5 border-2 border-white/40 border-t-white rounded-full animate-spin" />Signing in...</>
                ) : (
                  <>Sign In <ArrowRight className="w-4 h-4" /></>
                )}
              </button>
            </form>

            {/* Footer */}
            <div className="mt-8 text-center space-y-3">
              <p className="text-sm text-gray-500">
                Don't have an account?{' '}
                <Link to="/register" className="font-semibold hover:underline" style={{ color: '#0F4C81' }}>Register here</Link>
              </p>
              <div className="border-t pt-4">
                <Link to="/admin/login" className="text-xs text-gray-400 hover:text-gray-600 transition-colors">
                  Admin? Login here →
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;

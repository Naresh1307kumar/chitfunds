import React, { useState } from 'react';
import { Link, useSearchParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, Lock, Eye, EyeOff, ArrowRight, AlertCircle, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';

const ResetPassword = () => {
  const { resetPassword } = useAuth();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const token = searchParams.get('token');
  
  const [form, setForm] = useState({ password: '', confirmPassword: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4" style={{ background: '#F4F6F8' }}>
        <div className="text-center">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Invalid Reset Link</h2>
          <p className="text-gray-500 mb-6">The password reset link is invalid or missing the token.</p>
          <Link to="/forgot-password" className="text-blue-600 hover:underline font-semibold">Request a new link</Link>
        </div>
      </div>
    );
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await resetPassword(token, form.password);
      setSuccess(true);
      toast.success('Password updated successfully!');
      setTimeout(() => navigate('/login'), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reset password. Token may be expired.');
    } finally {
      setLoading(false);
    }
  };

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4" style={{ background: 'linear-gradient(135deg, #0F4C81 0%, #1A2B49 100%)' }}>
        <div className="bg-white rounded-3xl shadow-2xl p-10 max-w-md w-full text-center">
          <div className="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6" style={{ background: '#ECFDF5' }}>
            <CheckCircle className="w-10 h-10 text-green-500" />
          </div>
          <h2 className="text-2xl font-bold mb-3" style={{ color: '#1A2B49' }}>Password Reset!</h2>
          <p className="text-gray-500 mb-8 text-sm leading-relaxed">
            Your password has been successfully updated. Redirecting to login...
          </p>
          <Link to="/login" className="block w-full py-3.5 rounded-xl font-bold text-white text-sm text-center transition-all" style={{ background: '#0F4C81' }}>
            Login Now
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ background: 'linear-gradient(135deg, #0F4C81 0%, #1A2B49 100%)' }}>
      <div className="bg-white rounded-3xl shadow-2xl p-10 max-w-md w-full">
        <div className="flex items-center gap-3 mb-8 justify-center">
          <ShieldCheck className="w-8 h-8" style={{ color: '#0F4C81' }} />
          <span className="text-2xl font-bold" style={{ color: '#1A2B49' }}>SecureChit</span>
        </div>
        <h2 className="text-2xl font-bold mb-1 text-center" style={{ color: '#1A2B49' }}>Create New Password</h2>
        <p className="text-gray-500 mb-8 text-sm text-center">
          Enter your new password below.
        </p>

        {error && (
          <div className="flex items-start gap-3 p-4 rounded-xl mb-6" style={{ background: '#FEF2F2', border: '1px solid #FECACA' }}>
            <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Password */}
          <div>
            <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>New Password</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input type={showPassword ? 'text' : 'password'} name="password" value={form.password} onChange={handleChange} placeholder="Min. 8 characters" required
                className="w-full pl-12 pr-12 py-3.5 rounded-xl border text-sm outline-none transition-all"
                style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                onFocus={e => e.target.style.borderColor = '#0F4C81'}
                onBlur={e => e.target.style.borderColor = '#DCE3EA'} />
              <button type="button" onClick={() => setShowPassword(!showPassword)}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          {/* Confirm Password */}
          <div>
            <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>Confirm Password</label>
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input type="password" name="confirmPassword" value={form.confirmPassword} onChange={handleChange} placeholder="Re-enter password" required
                className="w-full pl-12 pr-4 py-3.5 rounded-xl border text-sm outline-none transition-all"
                style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                onFocus={e => e.target.style.borderColor = '#0F4C81'}
                onBlur={e => e.target.style.borderColor = '#DCE3EA'} />
            </div>
          </div>

          <button type="submit" disabled={loading}
            className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all mt-2"
            style={{ background: loading ? '#93A8C4' : '#0F4C81' }}>
            {loading ? <><div className="w-5 h-5 border-2 border-white/40 border-t-white rounded-full animate-spin" />Saving...</> : <>Reset Password <ArrowRight className="w-4 h-4" /></>}
          </button>
        </form>
      </div>
    </div>
  );
};

export default ResetPassword;

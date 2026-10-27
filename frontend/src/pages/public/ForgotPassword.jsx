import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, ArrowRight, AlertCircle, User, Lock, Key, Eye, EyeOff, CheckCircle, RotateCw } from 'lucide-react';
import toast from 'react-hot-toast';

const ForgotPassword = () => {
  const { forgotPassword, resetPassword } = useAuth();
  const navigate = useNavigate();

  // Step state: 'request' | 'verify' | 'success'
  const [step, setStep] = useState('request');
  const [username, setUsername] = useState('');
  const [maskedEmail, setMaskedEmail] = useState('');

  // OTP and New Password state
  const [otp, setOtp] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);

  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [error, setError] = useState('');

  // 1. Send OTP to registered email
  const handleRequestOtp = async (e) => {
    e.preventDefault();
    if (!username.trim()) {
      setError('Please enter your username or registered email.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await forgotPassword(username.trim());
      setMaskedEmail(res.email || 'your registered email');
      setStep('verify');
      toast.success(res.message || 'OTP sent to your registered email!');
    } catch (err) {
      setError(err.response?.data?.detail || 'No registered account found with this username or email.');
    } finally {
      setLoading(false);
    }
  };

  // Resend OTP
  const handleResendOtp = async () => {
    setResending(true);
    setError('');
    try {
      await forgotPassword(username.trim());
      toast.success('A new OTP has been sent to your email!');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to resend OTP.');
    } finally {
      setResending(false);
    }
  };

  // 2. Verify OTP & Reset Password
  const handleResetPassword = async (e) => {
    e.preventDefault();
    setError('');

    if (!otp.trim()) {
      setError('Please enter the 6-digit OTP sent to your email.');
      return;
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }
    if (password !== confirmPassword) {
      setError('Passwords do not match.');
      return;
    }

    setLoading(true);
    try {
      await resetPassword(otp.trim(), password, username.trim());
      setStep('success');
      toast.success('Password updated successfully!');
      setTimeout(() => navigate('/login'), 2500);
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid or expired OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Success Screen
  if (step === 'success') {
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
          <Link to="/login" className="block w-full py-3.5 rounded-xl font-bold text-white text-sm text-center transition-all shadow-lg hover:shadow-xl" style={{ background: '#0F4C81' }}>
            Login Now
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ background: 'linear-gradient(135deg, #0F4C81 0%, #1A2B49 100%)' }}>
      <div className="bg-white rounded-3xl shadow-2xl p-10 max-w-md w-full">
        {/* Header */}
        <div className="flex items-center gap-3 mb-8 justify-center">
          <ShieldCheck className="w-8 h-8" style={{ color: '#0F4C81' }} />
          <span className="text-2xl font-bold" style={{ color: '#1A2B49' }}>SecureChit</span>
        </div>

        {step === 'request' ? (
          <>
            <h2 className="text-2xl font-bold mb-1 text-center" style={{ color: '#1A2B49' }}>Forgot Password?</h2>
            <p className="text-gray-500 mb-8 text-sm text-center">
              Enter your username or email address to receive a secure OTP code.
            </p>

            {error && (
              <div className="flex items-start gap-3 p-4 rounded-xl mb-6" style={{ background: '#FEF2F2', border: '1px solid #FECACA' }}>
                <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            <form onSubmit={handleRequestOtp} className="space-y-5">
              <div>
                <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>Username or Email</label>
                <div className="relative">
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={username}
                    onChange={(e) => { setUsername(e.target.value); setError(''); }}
                    placeholder="Enter your username or email"
                    required
                    className="w-full pl-12 pr-4 py-3.5 rounded-xl border text-sm outline-none transition-all"
                    style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                    onFocus={e => e.target.style.borderColor = '#0F4C81'}
                    onBlur={e => e.target.style.borderColor = '#DCE3EA'}
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all shadow-lg hover:shadow-xl"
                style={{ background: loading ? '#93A8C4' : '#0F4C81' }}
              >
                {loading ? (
                  <><div className="w-5 h-5 border-2 border-white/40 border-t-white rounded-full animate-spin" />Sending OTP to Email...</>
                ) : (
                  <>Send OTP <ArrowRight className="w-4 h-4" /></>
                )}
              </button>
            </form>
          </>
        ) : (
          <>
            <h2 className="text-2xl font-bold mb-1 text-center" style={{ color: '#1A2B49' }}>Enter OTP & New Password</h2>
            <p className="text-gray-500 mb-6 text-sm text-center">
              We sent a 6-digit OTP code to <span className="font-semibold text-slate-800">{maskedEmail}</span>.
            </p>

            {error && (
              <div className="flex items-start gap-3 p-4 rounded-xl mb-6" style={{ background: '#FEF2F2', border: '1px solid #FECACA' }}>
                <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            <form onSubmit={handleResetPassword} className="space-y-4">
              {/* 6-Digit OTP */}
              <div>
                <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>6-Digit OTP</label>
                <div className="relative">
                  <Key className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="text"
                    value={otp}
                    onChange={(e) => { setOtp(e.target.value.replace(/\D/g, '').slice(0, 6)); setError(''); }}
                    placeholder="Enter 6-digit OTP"
                    maxLength={6}
                    required
                    className="w-full pl-12 pr-4 py-3.5 rounded-xl border text-sm font-mono tracking-widest outline-none transition-all"
                    style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                    onFocus={e => e.target.style.borderColor = '#0F4C81'}
                    onBlur={e => e.target.style.borderColor = '#DCE3EA'}
                  />
                </div>
              </div>

              {/* New Password */}
              <div>
                <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>New Password</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => { setPassword(e.target.value); setError(''); }}
                    placeholder="Min. 8 characters"
                    required
                    className="w-full pl-12 pr-12 py-3.5 rounded-xl border text-sm outline-none transition-all"
                    style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                    onFocus={e => e.target.style.borderColor = '#0F4C81'}
                    onBlur={e => e.target.style.borderColor = '#DCE3EA'}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>

              {/* Confirm Password */}
              <div>
                <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>Confirm Password</label>
                <div className="relative">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => { setConfirmPassword(e.target.value); setError(''); }}
                    placeholder="Re-enter new password"
                    required
                    className="w-full pl-12 pr-4 py-3.5 rounded-xl border text-sm outline-none transition-all"
                    style={{ borderColor: '#DCE3EA', background: '#F8FAFC' }}
                    onFocus={e => e.target.style.borderColor = '#0F4C81'}
                    onBlur={e => e.target.style.borderColor = '#DCE3EA'}
                  />
                </div>
              </div>

              <div className="flex items-center justify-between pt-1">
                <button
                  type="button"
                  onClick={handleResendOtp}
                  disabled={resending}
                  className="text-xs font-semibold text-blue-700 hover:underline flex items-center gap-1"
                >
                  <RotateCw className={`w-3.5 h-3.5 ${resending ? 'animate-spin' : ''}`} />
                  {resending ? 'Sending...' : 'Resend OTP'}
                </button>
                <button
                  type="button"
                  onClick={() => { setStep('request'); setError(''); }}
                  className="text-xs text-gray-500 hover:underline"
                >
                  Change username/email
                </button>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all shadow-lg hover:shadow-xl mt-2"
                style={{ background: loading ? '#93A8C4' : '#0F4C81' }}
              >
                {loading ? (
                  <><div className="w-5 h-5 border-2 border-white/40 border-t-white rounded-full animate-spin" />Verifying & Resetting...</>
                ) : (
                  <>Reset Password <ArrowRight className="w-4 h-4" /></>
                )}
              </button>
            </form>
          </>
        )}

        <p className="mt-8 text-center text-sm text-gray-500">
          Remember your password?{' '}
          <Link to="/login" className="font-semibold hover:underline" style={{ color: '#0F4C81' }}>Back to login</Link>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;

import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, Mail, ArrowRight, AlertCircle, CheckCircle, User } from 'lucide-react';

const ForgotPassword = () => {
  const { forgotPassword } = useAuth();
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [resetToken, setResetToken] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const res = await forgotPassword(username);
      setResetToken(res.reset_token_debug);
      setSuccess(true);
    } catch (err) {
      setError('Failed to send reset link. Please try again.');
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
          <h2 className="text-2xl font-bold mb-3" style={{ color: '#1A2B49' }}>Check your email</h2>
          <p className="text-gray-500 mb-6 text-sm leading-relaxed">
            If an account exists for {username}, you will receive a password reset link shortly.
          </p>

          {/* DEVELOPMENT ONLY: Show the link for testing */}
          {resetToken && resetToken !== 'undefined' && (
            <div className="bg-yellow-50 border border-yellow-200 p-4 rounded-xl mb-6 text-left">
              <p className="text-xs font-bold text-yellow-800 mb-2 uppercase tracking-wide">Developer Testing Link:</p>
              <Link to={`/reset-password?token=${resetToken}`} className="text-sm font-medium text-blue-600 hover:underline break-all">
                Click here to Reset Password
              </Link>
            </div>
          )}

          <Link to="/login" className="block w-full py-3.5 rounded-xl font-bold text-white text-sm text-center transition-all" style={{ background: '#0F4C81' }}>
            Back to Login
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
        <h2 className="text-2xl font-bold mb-1 text-center" style={{ color: '#1A2B49' }}>Forgot Password?</h2>
        <p className="text-gray-500 mb-8 text-sm text-center">
          Enter your username to get a password reset link.
        </p>

        {error && (
          <div className="flex items-start gap-3 p-4 rounded-xl mb-6" style={{ background: '#FEF2F2', border: '1px solid #FECACA' }}>
            <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
            <p className="text-red-700 text-sm">{error}</p>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-semibold mb-2" style={{ color: '#1A2B49' }}>Username</label>
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={username}
                onChange={(e) => { setUsername(e.target.value); setError(''); }}
                placeholder="Enter your username"
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
            className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all"
            style={{ background: loading ? '#93A8C4' : '#0F4C81' }}
          >
            {loading ? (
              <><div className="w-5 h-5 border-2 border-white/40 border-t-white rounded-full animate-spin" />Sending...</>
            ) : (
              <>Send Reset Link <ArrowRight className="w-4 h-4" /></>
            )}
          </button>
        </form>

        <p className="mt-8 text-center text-sm text-gray-500">
          Remember your password?{' '}
          <Link to="/login" className="font-semibold hover:underline" style={{ color: '#0F4C81' }}>Back to login</Link>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;

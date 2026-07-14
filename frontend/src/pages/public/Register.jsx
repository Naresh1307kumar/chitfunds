import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { ShieldCheck, Mail, Lock, User, Phone, Eye, EyeOff, ArrowRight, ArrowLeft, AlertCircle, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';
import ParticleBackground from '../../components/ParticleBackground';

const Register = () => {
  const { register } = useAuth();
  const navigate = useNavigate();
  
  const [step, setStep] = useState(1);
  const [form, setForm] = useState({ username: '', name: '', email: '', phone: '', password: '', confirmPassword: '' });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError('');
  };

  const handleNext = () => {
    if (step === 1) {
      if (!form.name || !form.username || !form.email || !form.phone) {
        setError('Please fill in all account information.');
        return;
      }
      if (form.phone.length !== 10 || !/^\d+$/.test(form.phone)) {
        setError('Phone number must be exactly 10 digits.');
        return;
      }
      setError('');
      setStep(2);
    }
  };

  const handleBack = () => {
    setStep(1);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.password || !form.confirmPassword) {
      setError('Please fill in both password fields.');
      return;
    }
    if (form.password.length < 8) {
      setError('Password must be at least 8 characters.');
      return;
    }
    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    
    setLoading(true);
    setError('');
    try {
      // Register without aadhar number
      await register(form.username, form.name, form.email, form.phone, null, form.password);
      setSuccess(true);
      toast.success('Registration successful! Awaiting admin approval.');
    } catch (err) {
      let msg = 'Registration failed. Please try again.';
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

  if (success) {
    return (
      <div className="min-h-screen flex items-center justify-center px-4 auth-animated-bg relative overflow-hidden">
        <ParticleBackground />
        <div className="bg-white rounded-3xl shadow-2xl p-10 max-w-md w-full text-center auth-content animate-float">
          <div className="w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6" style={{ background: '#ECFDF5' }}>
            <CheckCircle className="w-10 h-10 text-green-500" />
          </div>
          <h2 className="text-2xl font-bold mb-3" style={{ color: '#1A2B49' }}>Registration Submitted!</h2>
          <p className="text-gray-500 mb-8 text-sm leading-relaxed">
            Your account is under review. Admin will approve your account shortly. You'll be able to login once approved.
          </p>
          <Link to="/login" className="block w-full py-3.5 rounded-xl font-bold text-white text-sm text-center transition-all shadow-md hover:opacity-90" style={{ background: '#0F4C81' }}>
            Back to Login
          </Link>
        </div>
      </div>
    );
  }

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
          Start Your<br />
          <span style={{ color: '#C9A227' }}>Investment Journey</span>
        </h1>
        <p className="text-blue-200 text-lg leading-relaxed mb-10">
          Join thousands of members who trust SecureChit for transparent, secure chit fund management.
        </p>
        
        {/* Step indicators on left */}
        <div className="space-y-6">
          <div className="flex items-center gap-4">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-colors ${step === 1 ? 'bg-corpGold text-slate-900 shadow-md' : 'bg-white/20 text-blue-100'}`}>
              1
            </div>
            <span className={`text-sm ${step === 1 ? 'font-bold text-white' : 'text-blue-200'}`}>Account Details</span>
          </div>
          <div className="flex items-center gap-4">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-colors ${step === 2 ? 'bg-corpGold text-slate-900 shadow-md' : 'bg-white/20 text-blue-100'}`}>
              2
            </div>
            <span className={`text-sm ${step === 2 ? 'font-bold text-white' : 'text-blue-200'}`}>Password & Security</span>
          </div>
        </div>
      </div>

      {/* Right Panel */}
      <div className="w-full lg:w-1/2 flex items-center justify-center px-6 py-12 auth-content">
        <div className="w-full max-w-md">
          <div className="bg-white rounded-3xl shadow-2xl p-10">
            <div className="flex items-center gap-3 mb-2 lg:hidden">
              <ShieldCheck className="w-7 h-7" style={{ color: '#0F4C81' }} />
              <span className="text-xl font-bold" style={{ color: '#1A2B49' }}>SecureChit</span>
            </div>
            <h2 className="text-3xl font-bold mb-1" style={{ color: '#1A2B49' }}>Create Account</h2>
            <p className="text-gray-500 mb-8 text-sm">Step {step} of 2 - {step === 1 ? 'Account Details' : 'Security'}</p>

            {error && (
              <div className="flex items-start gap-3 p-4 rounded-xl mb-6" style={{ background: '#FEF2F2', border: '1px solid #FECACA' }}>
                <AlertCircle className="w-5 h-5 text-red-500 mt-0.5 flex-shrink-0" />
                <p className="text-red-700 text-sm">{error}</p>
              </div>
            )}

            <form onSubmit={e => e.preventDefault()} className="space-y-4">
              {step === 1 && (
                <>
                  {/* Name */}
                  <div>
                    <label className="block text-xs font-bold mb-1 uppercase tracking-wider text-slate-500">Full Name</label>
                    <div className="relative">
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input type="text" name="name" value={form.name} onChange={handleChange} placeholder="Rahul Sharma" required
                        className="w-full pl-11 pr-4 py-2.5 rounded-xl border text-sm outline-none bg-[#F8FAFC]"
                        style={{ borderColor: '#DCE3EA' }} />
                    </div>
                  </div>

                  {/* Username */}
                  <div>
                    <label className="block text-xs font-bold mb-1 uppercase tracking-wider text-slate-500">Username</label>
                    <div className="relative">
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input type="text" name="username" value={form.username} onChange={handleChange} placeholder="Unique Username" required
                        className="w-full pl-11 pr-4 py-2.5 rounded-xl border text-sm outline-none bg-[#F8FAFC]"
                        style={{ borderColor: '#DCE3EA' }} />
                    </div>
                  </div>

                  {/* Email */}
                  <div>
                    <label className="block text-xs font-bold mb-1 uppercase tracking-wider text-slate-500">Email Address</label>
                    <div className="relative">
                      <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input type="email" name="email" value={form.email} onChange={handleChange} placeholder="you@example.com" required
                        className="w-full pl-11 pr-4 py-2.5 rounded-xl border text-sm outline-none bg-[#F8FAFC]"
                        style={{ borderColor: '#DCE3EA' }} />
                    </div>
                  </div>

                  {/* Phone */}
                  <div>
                    <label className="block text-xs font-bold mb-1 uppercase tracking-wider text-slate-500">Phone Number</label>
                    <div className="relative">
                      <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input type="tel" name="phone" value={form.phone} onChange={handleChange} placeholder="10-digit mobile number" required maxLength={10}
                        className="w-full pl-11 pr-4 py-2.5 rounded-xl border text-sm outline-none bg-[#F8FAFC]"
                        style={{ borderColor: '#DCE3EA' }} />
                    </div>
                  </div>

                  <button type="button" onClick={handleNext}
                    className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all mt-4 hover:opacity-90 shadow-md"
                    style={{ background: '#0F4C81' }}>
                    Continue <ArrowRight className="w-4 h-4" />
                  </button>
                </>
              )}

              {step === 2 && (
                <>
                  {/* Password */}
                  <div>
                    <label className="block text-xs font-bold mb-1 uppercase tracking-wider text-slate-500">Password</label>
                    <div className="relative">
                      <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input type={showPassword ? 'text' : 'password'} name="password" value={form.password} onChange={handleChange} placeholder="Min. 8 characters" required
                        className="w-full pl-11 pr-11 py-2.5 rounded-xl border text-sm outline-none bg-[#F8FAFC]"
                        style={{ borderColor: '#DCE3EA' }} />
                      <button type="button" onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600">
                        {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                      </button>
                    </div>
                  </div>

                  {/* Confirm Password */}
                  <div>
                    <label className="block text-xs font-bold mb-1 uppercase tracking-wider text-slate-500">Confirm Password</label>
                    <div className="relative">
                      <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
                      <input type="password" name="confirmPassword" value={form.confirmPassword} onChange={handleChange} placeholder="Re-enter password" required
                        className="w-full pl-11 pr-4 py-2.5 rounded-xl border text-sm outline-none bg-[#F8FAFC]"
                        style={{ borderColor: '#DCE3EA' }} />
                    </div>
                  </div>

                  <div className="flex gap-4 mt-6">
                    <button type="button" onClick={handleBack}
                      className="w-1/2 py-3 rounded-xl border font-bold text-slate-700 text-sm hover:bg-slate-50 transition-colors"
                      style={{ borderColor: '#DCE3EA' }}>
                      Back
                    </button>
                    <button type="button" onClick={handleSubmit} disabled={loading}
                      className="w-1/2 py-3 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all shadow-md hover:opacity-90"
                      style={{ background: loading ? '#93A8C4' : '#0F4C81' }}>
                      {loading
                        ? <><div className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full animate-spin" />Submitting...</>
                        : <>Submit <ArrowRight className="w-4 h-4" /></>}
                    </button>
                  </div>
                </>
              )}
            </form>

            <p className="mt-6 text-center text-sm text-slate-500">
              Already have an account?{' '}
              <Link to="/login" className="font-semibold hover:underline" style={{ color: '#0F4C81' }}>Sign in</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;

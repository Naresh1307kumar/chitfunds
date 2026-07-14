with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app = f.read()

start_marker = "const JoinPlanModal = ({ plan, onClose }) => {"
end_marker = "const ScrollToTop = () => {"

if start_marker in app and end_marker in app:
    parts_start = app.split(start_marker)
    # The second part contains JoinPlanModal + ScrollToTop + everything else
    remaining = parts_start[1]
    
    parts_end = remaining.split(end_marker)
    # parts_end[0] is the rest of JoinPlanModal
    # parts_end[1] is ScrollToTop + the rest of App.jsx
    
    new_join_modal_code = """const JoinPlanModal = ({ plan, onClose }) => {
  const [step, setStep] = React.useState(0); // Start at Step 0: Account Check
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const navigate = useNavigate();
  
  const [formData, setFormData] = React.useState({
    username: '',
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    
    // Guarantor
    g_name: '',
    g_phone: '',
    g_address: '',
    g_relationship: ''
  });

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleNext = () => {
    if (step === 1) {
      if (!formData.username || !formData.name || !formData.email || !formData.phone || !formData.password) {
        setError('Please fill in all account details.');
        return;
      }
      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match.');
        return;
      }
      if (formData.phone.length !== 10 || !/^\\d+$/.test(formData.phone)) {
        setError('Phone Number must be exactly 10 digits.');
        return;
      }
    }
    setStep(step + 1);
  };

  const handleBack = () => {
    setStep(step - 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.g_name || !formData.g_phone || !formData.g_address || !formData.g_relationship) {
      setError('Please fill in all guarantor details.');
      return;
    }
    if (formData.g_phone.length !== 10 || !/^\\d+$/.test(formData.g_phone)) {
      setError('Guarantor phone must be 10 digits.');
      return;
    }

    setLoading(true);
    try {
      await api.post('/api/v1/auth/register', {
        username: formData.username,
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        password: formData.password,
        aadhar_number: null
      });
      setStep(3);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-3xl w-full max-w-xl overflow-hidden shadow-2xl border border-slate-100 flex flex-col max-h-[90vh]">
        <div className="px-8 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Join Plan: {plan?.name}</h2>
            <p className="text-xs text-slate-500 mt-0.5">Monthly Installment: ₹{plan?.monthlyAmount}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 text-2xl font-semibold">&times;</button>
        </div>

        {/* Step Indicator */}
        {step > 0 && (
          <div className="flex justify-between items-center px-8 py-4 bg-slate-50/50 border-b border-slate-100 text-xs font-semibold text-slate-400">
            <div className={`flex items-center gap-2 ${step >= 1 ? 'text-corpBlue' : ''}`}>
              <span className={`w-5 h-5 rounded-full flex items-center justify-center border ${step >= 1 ? 'border-corpBlue bg-blue-50' : 'border-slate-300'}`}>1</span>
              <span>Account Details</span>
            </div>
            <div className="w-12 h-0.5 bg-slate-200"></div>
            <div className={`flex items-center gap-2 ${step >= 2 ? 'text-corpBlue' : ''}`}>
              <span className={`w-5 h-5 rounded-full flex items-center justify-center border ${step >= 2 ? 'border-corpBlue bg-blue-50' : 'border-slate-300'}`}>2</span>
              <span>Guarantor Info</span>
            </div>
            <div className="w-12 h-0.5 bg-slate-200"></div>
            <div className={`flex items-center gap-2 ${step >= 3 ? 'text-corpBlue' : ''}`}>
              <span className={`w-5 h-5 rounded-full flex items-center justify-center border ${step >= 3 ? 'border-corpBlue bg-blue-50' : 'border-slate-300'}`}>3</span>
              <span>Success</span>
            </div>
          </div>
        )}

        <div className="p-8 overflow-y-auto flex-grow text-slate-700">
          {error && (
            <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm mb-6 flex items-center gap-2 border border-red-100">
              <p className="font-medium">⚠️ {error}</p>
            </div>
          )}

          {step === 0 && (
            <div className="text-center py-6 space-y-6">
              <div className="w-16 h-16 rounded-full bg-blue-50 border border-blue-100 flex items-center justify-center mx-auto text-corpBlue">
                <span className="text-3xl font-bold">👤</span>
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-900">Do you have a SecureChit Account?</h3>
                <p className="text-slate-500 text-sm mt-2 max-w-sm mx-auto">Please let us know if you already have an account with us to proceed correctly.</p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
                <button 
                  onClick={() => { onClose(); navigate('/login'); }}
                  className="px-6 py-3 border border-slate-350 hover:bg-slate-50 text-slate-700 font-bold rounded-xl text-sm transition-colors"
                >
                  Yes, I have an account (Log In)
                </button>
                <button 
                  onClick={() => setStep(1)}
                  className="px-6 py-3 bg-corpBlue hover:bg-corpNavy text-white font-bold rounded-xl text-sm transition-colors shadow-md"
                >
                  No, I need to register
                </button>
              </div>
            </div>
          )}

          {step === 1 && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Full Name</label>
                  <input type="text" name="name" value={formData.name} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Ramesh Kumar" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Username</label>
                  <input type="text" name="username" value={formData.username} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="ramesh123" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Email Address</label>
                  <input type="email" name="email" value={formData.email} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="name@email.com" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Phone Number</label>
                  <input type="text" name="phone" value={formData.phone} onChange={handleInputChange} maxLength="10" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="10-digit number" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Password</label>
                  <input type="password" name="password" value={formData.password} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Min 8 chars" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Confirm Password</label>
                  <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Repeat password" />
                </div>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Guarantor Name</label>
                  <input type="text" name="g_name" value={formData.g_name} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Guarantor Full Name" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Guarantor Phone</label>
                  <input type="text" name="g_phone" value={formData.g_phone} onChange={handleInputChange} maxLength="10" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="10-digit number" />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Relationship</label>
                <input type="text" name="g_relationship" value={formData.g_relationship} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="e.g. Father, Friend" />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Guarantor Address</label>
                <textarea name="g_address" value={formData.g_address} onChange={handleInputChange} required rows="3" className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Full residential address of guarantor"></textarea>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="text-center py-6">
              <div className="w-20 h-20 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center mx-auto mb-6 text-emerald-500">
                <span className="text-3xl font-bold">✓</span>
              </div>
              <h3 className="text-2xl font-bold text-slate-900 mb-2">Onboarding Successful!</h3>
              <p className="text-slate-500 text-sm max-w-sm mx-auto leading-relaxed">
                Your application to join the <strong>{plan?.name}</strong> has been submitted. Admin will review and approve your account shortly. 
              </p>
              <p className="text-slate-400 text-xs max-w-xs mx-auto mt-4 leading-relaxed">
                Once approved, you can login to upload your official KYC documents.
              </p>
            </div>
          )}
        </div>

        {step > 0 && step < 3 && (
          <div className="px-8 py-4 border-t border-slate-100 bg-slate-50 flex justify-between items-center">
            <button onClick={handleBack} className="px-5 py-2.5 border border-slate-350 text-slate-700 font-semibold rounded-xl text-sm hover:bg-slate-100 transition-colors">Back</button>
            {step === 1 ? (
              <button onClick={handleNext} className="px-6 py-2.5 bg-corpBlue text-white font-semibold rounded-xl text-sm hover:bg-corpNavy transition-colors">Continue</button>
            ) : (
              <button onClick={handleSubmit} disabled={loading} className="px-6 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl text-sm hover:bg-emerald-700 transition-colors disabled:opacity-50">
                {loading ? 'Submitting...' : 'Submit Application'}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
"""
    
    # Reassemble App.jsx
    app = parts_start[0] + new_join_modal_code + "\n\n" + end_marker + parts_end[1]
    
    with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(app)
    print("JoinPlanModal updated successfully using string split!")
else:
    print("Error: Markers not found in App.jsx!")

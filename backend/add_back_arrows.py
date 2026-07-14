with open('../frontend/src/pages/public/Login.jsx', 'r', encoding='utf-8') as f:
    login = f.read()

# 1. Update Login.jsx lucide-react imports to include ArrowLeft
login = login.replace(
    "import { ShieldCheck, Mail, Lock, Eye, EyeOff, ArrowRight, AlertCircle, User } from 'lucide-react';",
    "import { ShieldCheck, Mail, Lock, Eye, EyeOff, ArrowRight, ArrowLeft, AlertCircle, User } from 'lucide-react';"
)

# 2. Add floating circular back arrow button inside Login component
old_login_root = '<div className="min-h-screen flex auth-animated-bg relative overflow-hidden">'
new_login_root = """<div className="min-h-screen flex auth-animated-bg relative overflow-hidden">
      {/* Back to Home Arrow */}
      <button 
        onClick={() => navigate('/')} 
        className="absolute top-6 left-6 w-10 h-10 rounded-full bg-white shadow-md border border-slate-200 flex items-center justify-center text-slate-600 hover:text-corpBlue hover:border-corpBlue transition-all z-20 group"
      >
        <ArrowLeft className="w-5 h-5 group-hover:-translate-x-0.5 transition-transform" />
      </button>"""

login = login.replace(old_login_root, new_login_root)

with open('../frontend/src/pages/public/Login.jsx', 'w', encoding='utf-8') as f:
    f.write(login)

# ----------------- REGISTER PAGE -----------------
with open('../frontend/src/pages/public/Register.jsx', 'r', encoding='utf-8') as f:
    register = f.read()

# 1. Update Register.jsx imports to include ArrowLeft
register = register.replace(
    "import { ShieldCheck, Mail, Lock, User, Phone, Eye, EyeOff, ArrowRight, AlertCircle, CheckCircle } from 'lucide-react';",
    "import { ShieldCheck, Mail, Lock, User, Phone, Eye, EyeOff, ArrowRight, ArrowLeft, AlertCircle, CheckCircle } from 'lucide-react';"
)

# 2. Add floating back arrow button inside Register component
old_register_root = '<div className="min-h-screen flex auth-animated-bg relative overflow-hidden">'
new_register_root = """<div className="min-h-screen flex auth-animated-bg relative overflow-hidden">
      {/* Back to Home Arrow */}
      <button 
        onClick={() => navigate('/')} 
        className="absolute top-6 left-6 w-10 h-10 rounded-full bg-white shadow-md border border-slate-200 flex items-center justify-center text-slate-600 hover:text-corpBlue hover:border-corpBlue transition-all z-20 group"
      >
        <ArrowLeft className="w-5 h-5 group-hover:-translate-x-0.5 transition-transform" />
      </button>"""

register = register.replace(old_register_root, new_register_root)

# 3. Clean up the manual "Back to Login" button in Step 1 to look cleaner
# We keep the back button in Step 2, or replace Step 1 with just Continue button
register = register.replace(
    """                  <div className="flex gap-4 mt-6">
                    <button type="button" onClick={() => navigate('/login')}
                      className="w-1/2 py-3 rounded-xl border font-bold text-slate-755 text-sm hover:bg-slate-50 transition-colors"
                      style={{ borderColor: '#DCE3EA' }}>
                      Back to Login
                    </button>
                    <button type="button" onClick={handleNext}
                      className="w-1/2 py-3 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all shadow-md hover:opacity-90"
                      style={{ background: '#0F4C81' }}>
                      Continue <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>""",
    """                  <button type="button" onClick={handleNext}
                    className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all mt-4 hover:opacity-90 shadow-md animate-pulse-subtle"
                    style={{ background: '#0F4C81' }}>
                    Continue <ArrowRight className="w-4 h-4" />
                  </button>"""
)

# Also let's handle case if my target has slate-750
register = register.replace(
    """                  <div className="flex gap-4 mt-6">
                    <button type="button" onClick={() => navigate('/login')}
                      className="w-1/2 py-3 rounded-xl border font-bold text-slate-750 text-sm hover:bg-slate-50 transition-colors"
                      style={{ borderColor: '#DCE3EA' }}>
                      Back to Login
                    </button>
                    <button type="button" onClick={handleNext}
                      className="w-1/2 py-3 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all shadow-md hover:opacity-90"
                      style={{ background: '#0F4C81' }}>
                      Continue <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>""",
    """                  <button type="button" onClick={handleNext}
                    className="w-full py-3.5 rounded-xl font-bold text-white text-sm flex items-center justify-center gap-2 transition-all mt-4 hover:opacity-90 shadow-md"
                    style={{ background: '#0F4C81' }}>
                    Continue <ArrowRight className="w-4 h-4" />
                  </button>"""
)

with open('../frontend/src/pages/public/Register.jsx', 'w', encoding='utf-8') as f:
    f.write(register)

# ----------------- APP.JSX (JOIN PLAN MODAL) -----------------
with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app = f.read()

# 1. Ensure ArrowLeft is imported at the top of App.jsx if not already
app = app.replace(
    "import { \n  ShieldCheck, Menu, X, ArrowRight, Users, CalendarDays, \n  BellRing, BarChart3, CheckCircle2, Phone, Mail, MapPin,",
    "import { \n  ShieldCheck, Menu, X, ArrowRight, ArrowLeft, Users, CalendarDays, \n  BellRing, BarChart3, CheckCircle2, Phone, Mail, MapPin,"
)
app = app.replace(
    "import { \n  ShieldCheck, Menu, X, ArrowRight, Users, CalendarDays,",
    "import { \n  ShieldCheck, Menu, X, ArrowRight, ArrowLeft, Users, CalendarDays,"
)
app = app.replace(
    "import { \n  ShieldCheck, Menu, X, ArrowRight,",
    "import { \n  ShieldCheck, Menu, X, ArrowRight, ArrowLeft,"
)

# 2. Add back arrow in JoinPlanModal header next to the title
old_modal_header = """        <div className="px-8 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div>
            <h2 className="text-xl font-bold text-slate-900">Join Plan: {plan?.name}</h2>
            <p className="text-xs text-slate-500 mt-0.5">Monthly Installment: ₹{plan?.monthlyAmount}</p>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 text-2xl font-semibold">&times;</button>
        </div>"""

new_modal_header = """        <div className="px-8 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div className="flex items-center gap-3">
            {step > 0 && step < 3 && (
              <button 
                onClick={handleBack} 
                className="w-8 h-8 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors"
                title="Go Back"
              >
                <ArrowLeft className="w-4 h-4" />
              </button>
            )}
            <div>
              <h2 className="text-xl font-bold text-slate-900">Join Plan: {plan?.name}</h2>
              <p className="text-xs text-slate-500 mt-0.5">Monthly Installment: ₹{plan?.monthlyAmount}</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 text-2xl font-semibold">&times;</button>
        </div>"""

app = app.replace(old_modal_header, new_modal_header)

# 3. Clean up the big "Back" button in the modal footer to keep it neat and modern
# Since we now have the elegant arrow next to the title, we can remove the footer "Back" button
# and just center or align the action buttons to the right.
old_modal_footer = """        {step > 0 && step < 3 && (
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
        )}"""

new_modal_footer = """        {step > 0 && step < 3 && (
          <div className="px-8 py-4 border-t border-slate-100 bg-slate-50 flex justify-end items-center">
            {step === 1 ? (
              <button onClick={handleNext} className="px-6 py-2.5 bg-corpBlue text-white font-semibold rounded-xl text-sm hover:bg-corpNavy transition-colors shadow-md">Continue</button>
            ) : (
              <button onClick={handleSubmit} disabled={loading} className="px-6 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl text-sm hover:bg-emerald-700 transition-colors disabled:opacity-50 shadow-md">
                {loading ? 'Submitting...' : 'Submit Application'}
              </button>
            )}
          </div>
        )}"""

app = app.replace(old_modal_footer, new_modal_footer)

with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app)

print("Floating circular back arrows and modal header back arrow successfully implemented!")

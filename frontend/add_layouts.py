import os
import re

base_dir = r"c:\chit fund\frontend\src"

member_layout_code = """import React from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ShieldCheck, CreditCard, User, LogOut, LayoutDashboard, 
  FileCheck, Users, HelpCircle 
} from 'lucide-react';

export const MemberLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/member/dashboard', icon: LayoutDashboard },
    { name: 'Schemes', path: '/member/plans', icon: ShieldCheck },
    { name: 'Payments', path: '/member/payments', icon: CreditCard },
    { name: 'KYC', path: '/member/kyc', icon: FileCheck },
    { name: 'Guarantors', path: '/member/guarantor', icon: Users },
  ];

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
      {/* Side Nav */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col shadow-sm z-20 hidden md:flex">
        <div className="p-6 border-b border-slate-100 flex items-center gap-2">
          <ShieldCheck className="w-8 h-8 text-corpBlue" />
          <span className="font-bold text-xl tracking-tight text-slate-900">SecureChit</span>
        </div>
        <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
          {navItems.map(item => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            return (
              <Link key={item.path} to={item.path} className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-semibold text-sm ${isActive ? 'bg-corpBlue text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}>
                <Icon className="w-5 h-5" />
                {item.name}
              </Link>
            );
          })}
        </div>
      </aside>

      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Nav */}
        <nav className="bg-white border-b border-slate-200 px-4 sm:px-6 py-3.5 flex items-center justify-between z-10 shadow-sm shrink-0">
          <div className="flex items-center gap-2 sm:gap-3">
            <span className="md:hidden font-bold text-lg sm:text-xl tracking-tight text-slate-900 flex items-center gap-2">
               <ShieldCheck className="w-6 h-6 text-corpBlue" /> SecureChit
            </span>
            <span className="px-2 py-0.5 rounded text-[9px] sm:text-[10px] font-bold bg-blue-50 text-blue-600 border border-blue-200 hidden md:inline-block">MEMBER</span>
          </div>
          
          <div className="flex items-center gap-2 sm:gap-3">
            {location.pathname !== '/member/payments' && (
              <button 
                onClick={() => navigate('/member/payments')}
                className="flex items-center gap-1.5 text-xs font-bold text-white bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-700 hover:to-teal-700 px-4 py-2 rounded-xl shadow-sm transition-all"
              >
                <CreditCard className="w-4 h-4" /> <span className="hidden sm:inline">Pay Current</span> Month Due
              </button>
            )}
            
            <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
              <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-slate-100 text-corpBlue border border-slate-200">
                <User className="w-5 h-5" />
              </div>
              <div className="hidden md:block text-left">
                <span className="block text-sm font-semibold text-slate-900 leading-tight">{user?.name}</span>
                <span className="text-[11px] text-slate-500">ID: PM-{user?.id || '0042'}</span>
              </div>
            </div>
            
            <button onClick={handleLogout} className="flex items-center gap-1 text-xs sm:text-sm text-slate-500 hover:text-red-500 transition-colors bg-slate-50 hover:bg-red-50 px-4 py-2 rounded-xl border border-slate-200 ml-2">
              <LogOut className="w-4 h-4" /> <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </nav>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto relative">
          {children}
        </main>
      </div>
    </div>
  );
};
"""

admin_layout_code = """import React from 'react';
import { useLocation, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { 
  ShieldCheck, User, LogOut, LayoutDashboard, Users, FileCheck, 
  CreditCard, Home, Settings
} from 'lucide-react';

export const AdminLayout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/admin/dashboard', icon: LayoutDashboard },
    { name: 'Members', path: '/admin/members', icon: Users },
    { name: 'Chit Plans', path: '/admin/plans', icon: ShieldCheck },
    { name: 'Payments', path: '/admin/payments', icon: CreditCard },
    { name: 'Pronotes', path: '/admin/pronotes', icon: FileCheck },
  ];

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden font-sans">
      {/* Side Nav */}
      <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col shadow-xl z-20 hidden md:flex">
        <div className="p-6 border-b border-slate-800 flex items-center gap-2 text-white">
          <ShieldCheck className="w-8 h-8 text-amber-500" />
          <span className="font-bold text-xl tracking-tight">SecureChit</span>
        </div>
        <div className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
          {navItems.map(item => {
            const isActive = location.pathname.startsWith(item.path);
            const Icon = item.icon;
            return (
              <Link key={item.path} to={item.path} className={`flex items-center gap-3 px-4 py-3 rounded-xl transition-all font-semibold text-sm ${isActive ? 'bg-corpBlue text-white shadow-md' : 'hover:bg-slate-800 hover:text-white'}`}>
                <Icon className="w-5 h-5" />
                {item.name}
              </Link>
            );
          })}
        </div>
      </aside>

      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Top Nav */}
        <nav className="bg-white border-b border-slate-200 px-4 sm:px-6 py-3.5 flex items-center justify-between z-10 shadow-sm shrink-0">
          <div className="flex items-center gap-2 sm:gap-3">
             <span className="md:hidden font-bold text-lg sm:text-xl tracking-tight text-slate-900 flex items-center gap-2">
               <ShieldCheck className="w-6 h-6 text-amber-500" /> SecureChit
             </span>
             <span className="px-2 py-0.5 rounded-full text-[9px] sm:text-[10px] font-extrabold bg-amber-500/10 text-amber-700 border border-amber-300/30 uppercase tracking-wider hidden md:inline-block">
                ADMIN PORTAL
             </span>
          </div>
          
          <div className="flex items-center gap-2 sm:gap-3">
            <button 
              onClick={() => navigate('/')}
              className="flex items-center gap-1.5 text-xs font-semibold text-slate-600 hover:text-corpBlue transition-all bg-slate-50 hover:bg-blue-50 px-4 py-2 rounded-xl border border-slate-200 shadow-sm"
            >
              <Home className="w-4 h-4" /> <span className="hidden sm:inline">Public Site</span>
            </button>
            
            <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
              <div className="hidden md:block text-right">
                <span className="block text-xs font-bold text-slate-900 leading-tight">{user?.name}</span>
                <span className="text-[10px] text-slate-400 font-medium">System Administrator</span>
              </div>
              <div className="w-10 h-10 rounded-xl flex items-center justify-center bg-slate-900 text-amber-400 shadow-md">
                <User className="w-5 h-5" />
              </div>
            </div>
            
            <button onClick={handleLogout} className="flex items-center gap-1 text-xs sm:text-sm text-slate-500 hover:text-red-500 transition-colors bg-slate-50 hover:bg-red-50 px-4 py-2 rounded-xl border border-slate-200 ml-2">
              <LogOut className="w-4 h-4" /> <span className="hidden sm:inline">Logout</span>
            </button>
          </div>
        </nav>

        {/* Page Content */}
        <main className="flex-1 overflow-y-auto relative bg-slate-50/50">
          {children}
        </main>
      </div>
    </div>
  );
};
"""

with open(os.path.join(base_dir, 'components', 'MemberLayout.jsx'), 'w') as f:
    f.write(member_layout_code)
    
with open(os.path.join(base_dir, 'components', 'AdminLayout.jsx'), 'w') as f:
    f.write(admin_layout_code)

print("Layouts created.")

# Now strip <nav>...</nav> from Dashboard.jsx (member and admin)
def strip_nav(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Regex to find <nav>...</nav>
    # Since it can be multiline, we use re.DOTALL
    new_content = re.sub(r'\{/\*\s*Navbar\s*\*/\}\s*<nav.*?</nav>', '', content, flags=re.DOTALL)
    
    with open(filepath, 'w') as f:
        f.write(new_content)

strip_nav(os.path.join(base_dir, 'pages', 'member', 'Dashboard.jsx'))
strip_nav(os.path.join(base_dir, 'pages', 'admin', 'Dashboard.jsx'))
print("Navs stripped from dashboards.")

# Now update App.jsx
app_path = os.path.join(base_dir, 'App.jsx')
with open(app_path, 'r', encoding='utf-8') as f:
    app_content = f.read()

# Add imports
if 'MemberLayout' not in app_content:
    import_stmt = "import { MemberLayout } from './components/MemberLayout';\nimport { AdminLayout } from './components/AdminLayout';\n"
    app_content = app_content.replace("import { ProtectedRoute", import_stmt + "import { ProtectedRoute")

# Wrap Member routes
member_routes = [
    ('MemberDashboard', 'MemberLayout'),
    ('KYCUpload', 'MemberLayout'),
    ('GuarantorForm', 'MemberLayout'),
    ('ExplorePlans', 'MemberLayout'),
    ('MemberPayments', 'MemberLayout'),
]

admin_routes = [
    ('AdminDashboard', 'AdminLayout'),
    ('MembersList', 'AdminLayout'),
    ('MemberDetails', 'AdminLayout'),
    ('ManagePlans', 'AdminLayout'),
    ('PlanMembers', 'AdminLayout'),
    ('ConductDraw', 'AdminLayout'),
    ('AdminPayments', 'AdminLayout'),
    ('PronoteManagement', 'AdminLayout'),
]

for comp, layout in member_routes + admin_routes:
    # Look for `<Component />` and replace with `<Layout><Component /></Layout>`
    # But only if not already wrapped
    if f"<{layout}>" not in app_content:
        # Regex to find `<Component />` inside `<ProtectedRoute>` or `<RoleRoute>`
        pattern = rf'(<({comp})\s*/>)'
        replacement = rf'<{layout}>\1</{layout}>'
        app_content = re.sub(pattern, replacement, app_content)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_content)

print("App.jsx updated.")

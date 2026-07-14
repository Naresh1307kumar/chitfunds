import os

# ----------------- 1. MEMBERS LIST -----------------
with open("../frontend/src/pages/admin/MembersList.jsx", 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "import { ShieldCheck, Users, Search, MoreVertical, CheckCircle, Clock, XCircle, Eye } from 'lucide-react';",
    "import { ShieldCheck, Users, Search, MoreVertical, CheckCircle, Clock, XCircle, Eye, ArrowLeft } from 'lucide-react';"
)
c = c.replace(
    "import { Link } from 'react-router-dom';",
    "import { Link, useNavigate } from 'react-router-dom';"
)
c = c.replace(
    "const MembersList = () => {",
    "const MembersList = () => {\n  const navigate = useNavigate();"
)
c = c.replace(
    """      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Members List</h1>""",
    """      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/admin/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Members List</h1>"""
)
# Close div tag properly if we open one
c = c.replace(
    """          <p className="text-gray-500 mt-1">Manage and approve registered members.</p>
        </div>
        <div className="flex bg-white rounded-lg p-1 shadow-sm border border-gray-200">""",
    """          <p className="text-gray-500 mt-1">Manage and approve registered members.</p>
          </div>
        </div>
        <div className="flex bg-white rounded-lg p-1 shadow-sm border border-gray-200"."""
)
# Just in case my dot typo happened, let's look at the close container
c = c.replace(
    """          <p className="text-gray-500 mt-1">Manage and approve registered members.</p>
          </div>
        </div>
        <div className="flex bg-white rounded-lg p-1 shadow-sm border border-gray-200".""",
    """          <p className="text-gray-500 mt-1">Manage and approve registered members.</p>
          </div>
        </div>
        <div className="flex bg-white rounded-lg p-1 shadow-sm border border-gray-200">"""
)

with open("../frontend/src/pages/admin/MembersList.jsx", 'w', encoding='utf-8') as f:
    f.write(c)
print("MembersList.jsx updated!")


# ----------------- 2. MEMBER DETAILS -----------------
with open("../frontend/src/pages/admin/MemberDetails.jsx", 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    """      <Link to="/admin/members" className="inline-flex items-center gap-2 text-sm text-gray-500 hover:text-blue-600 mb-6 transition-colors">
        <ArrowLeft className="w-4 h-4" /> Back to Members
      </Link>""",
    """      <div className="flex items-center gap-4 mb-6">
        <button 
          onClick={() => navigate('/admin/members')}
          className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
          title="Go Back"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <span className="text-sm font-semibold text-slate-600">Back to Members List</span>
      </div>"""
)

with open("../frontend/src/pages/admin/MemberDetails.jsx", 'w', encoding='utf-8') as f:
    f.write(c)
print("MemberDetails.jsx updated!")


# ----------------- 3. PLAN MEMBERS -----------------
with open("../frontend/src/pages/admin/PlanMembers.jsx", 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "import { useParams, Link } from 'react-router-dom';",
    "import { useParams, Link, useNavigate } from 'react-router-dom';"
)
c = c.replace(
    "const PlanMembers = () => {",
    "const PlanMembers = () => {\n  const navigate = useNavigate();"
)
c = c.replace(
    """      <div className="mb-6">
        <Link to="/admin/plans" className="flex items-center gap-2 text-blue-600 font-semibold hover:text-blue-700 transition-colors inline-block mb-4">
          <ArrowLeft className="w-4 h-4" /> Back to Plans
        </Link>
        <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Plan Members</h1>
        <p className="text-gray-500 mt-1">Approve or reject members for this plan</p>
      </div>""",
    """      <div className="flex items-center gap-4 mb-8">
        <button 
          onClick={() => navigate('/admin/plans')}
          className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
          title="Go Back"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Plan Members</h1>
          <p className="text-gray-500 mt-1">Approve or reject members for this plan</p>
        </div>
      </div>"""
)

with open("../frontend/src/pages/admin/PlanMembers.jsx", 'w', encoding='utf-8') as f:
    f.write(c)
print("PlanMembers.jsx updated!")


# ----------------- 4. CONDUCT DRAW -----------------
with open("../frontend/src/pages/admin/ConductDraw.jsx", 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "import { useParams, Link } from 'react-router-dom';",
    "import { useParams, Link, useNavigate } from 'react-router-dom';"
)
c = c.replace(
    "const ConductDraw = () => {",
    "const ConductDraw = () => {\n  const navigate = useNavigate();"
)
c = c.replace(
    """      <div className="mb-6">
        <Link to="/admin/plans" className="flex items-center gap-2 text-blue-600 font-semibold hover:text-blue-700 transition-colors inline-block mb-4">
          <ArrowLeft className="w-4 h-4" /> Back to Plans
        </Link>
        <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Monthly Draw</h1>
        <p className="text-gray-500 mt-1">Conduct the lottery draw for this plan</p>
      </div>""",
    """      <div className="flex items-center gap-4 mb-8">
        <button 
          onClick={() => navigate('/admin/plans')}
          className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
          title="Go Back"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Monthly Draw</h1>
          <p className="text-gray-500 mt-1">Conduct the lottery draw for this plan</p>
        </div>
      </div>"""
)

with open("../frontend/src/pages/admin/ConductDraw.jsx", 'w', encoding='utf-8') as f:
    f.write(c)
print("ConductDraw.jsx updated!")


# ----------------- 5. ADMIN PAYMENTS -----------------
with open("../frontend/src/pages/admin/Payments.jsx", 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace(
    "import { IndianRupee, CheckCircle, XCircle, RefreshCw } from 'lucide-react';",
    "import { IndianRupee, CheckCircle, XCircle, RefreshCw, ArrowLeft } from 'lucide-react';"
)
c = c.replace(
    "const AdminPayments = () => {",
    "import { useNavigate } from 'react-router-dom';\n\nconst AdminPayments = () => {\n  const navigate = useNavigate();"
)
c = c.replace(
    """      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-corpTextDark flex items-center gap-2">
            <IndianRupee className="w-8 h-8 text-corpGold" /> Payment Verifications
          </h1>
          <p className="text-corpTextLight mt-1">Verify manual payments submitted by members</p>
        </div>""",
    """      <div className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/admin/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-corpTextDark flex items-center gap-2">
              <IndianRupee className="w-8 h-8 text-corpGold" /> Payment Verifications
            </h1>
            <p className="text-corpTextLight mt-1">Verify manual payments submitted by members</p>
          </div>
        </div>"""
)

with open("../frontend/src/pages/admin/Payments.jsx", 'w', encoding='utf-8') as f:
    f.write(c)
print("Admin Payments.jsx updated!")

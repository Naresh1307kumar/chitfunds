import os

def apply_back_arrow_to_file(filepath, back_route, title_text, replacement_code):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add ArrowLeft to lucide-react import
    if 'ArrowLeft' not in content:
        content = content.replace(
            "import { ",
            "import { ArrowLeft, "
        )

    # 2. Add useNavigate to react-router-dom import if not present
    if 'useNavigate' not in content:
        if "from 'react-router-dom'" in content:
            content = content.replace(
                "import { ",
                "import { useNavigate, "
            )
        elif 'from "react-router-dom"' in content:
            content = content.replace(
                'import { ',
                'import { useNavigate, '
            )
        else:
            # Add import
            content = "import { useNavigate } from 'react-router-dom';\n" + content

    # 3. Add const navigate = useNavigate(); inside component
    component_name = filepath.split('/')[-1].replace('.jsx', '')
    # Handle files where component name is different or has specific signature
    sig_patterns = [
        f"const {component_name} = () => {{",
        f"const {component_name} = ({{",
        "const MemberPayments = () => {",
        "const AdminPayments = () => {"
    ]
    
    sig_found = False
    for pat in sig_patterns:
        if pat in content:
            if 'const navigate = useNavigate();' not in content:
                content = content.replace(pat, pat + "\n  const navigate = useNavigate();")
            sig_found = True
            break
            
    if not sig_found:
        # Fallback search for any const XXX = () => {
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if " = () => {" in line or " = ({" in line:
                if 'const navigate = useNavigate();' not in content:
                    lines[i] = line + "\n  const navigate = useNavigate();"
                    content = '\n'.join(lines)
                break

    # 4. Replace the title pattern with the back arrow wrapper
    if title_text in content:
        content = content.replace(title_text, replacement_code)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully processed back arrow for: {filepath}")
    else:
        print(f"Title text '{title_text}' not found in {filepath}")

# 1. KYCUpload
apply_back_arrow_to_file(
    "../frontend/src/pages/member/KYCUpload.jsx",
    "/member/dashboard",
    '<h2 className="text-2xl font-bold text-gray-900">KYC Verification</h2>',
    """<button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white mr-2"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <h2 className="text-2xl font-bold text-gray-900">KYC Verification</h2>"""
)

# 2. GuarantorForm
apply_back_arrow_to_file(
    "../frontend/src/pages/member/GuarantorForm.jsx",
    "/member/dashboard",
    '<UserPlus className="w-6 h-6 text-blue-600" />',
    """<button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white mr-2"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <UserPlus className="w-6 h-6 text-blue-600" />"""
)

# 3. ExplorePlans
apply_back_arrow_to_file(
    "../frontend/src/pages/member/ExplorePlans.jsx",
    "/member/dashboard",
    """      <div className="mb-8">
        <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Explore Schemes</h1>""",
    """      <div className="flex items-center gap-4 mb-8">
        <button 
          onClick={() => navigate('/member/dashboard')}
          className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
          title="Go Back"
        >
          <ArrowLeft className="w-4 h-4" />
        </button>
        <div>
          <h1 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Explore Schemes</h1>"""
)

# 4. Member Payments
apply_back_arrow_to_file(
    "../frontend/src/pages/member/Payments.jsx",
    "/member/dashboard",
    """        <h1 className="text-3xl font-bold text-corpTextDark mb-2">My Dues & Payments</h1>""",
    """        <div className="flex items-center gap-4 mb-6">
          <button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-corpTextDark mb-2">My Dues & Payments</h1>"""
)

# Fix trailing tags in Payments.jsx
with open("../frontend/src/pages/member/Payments.jsx", 'r', encoding='utf-8') as f:
    c = f.read()
target_footer = """        <h1 className="text-3xl font-bold text-corpTextDark mb-2">My Dues & Payments</h1>
        <p className="text-corpTextLight mb-8">View your pending installments and submit payment proofs.</p>"""
new_footer = """        <div className="flex items-center gap-4 mb-6">
          <button 
            onClick={() => navigate('/member/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-corpTextDark mb-2">My Dues & Payments</h1>
            <p className="text-corpTextLight mb-0">View your pending installments and submit payment proofs.</p>
          </div>
        </div>"""
if target_footer in c:
    c = c.replace(target_footer, new_footer)
    with open("../frontend/src/pages/member/Payments.jsx", 'w', encoding='utf-8') as f:
        f.write(c)

# 5. Admin Payments
apply_back_arrow_to_file(
    "../frontend/src/pages/admin/Payments.jsx",
    "/admin/dashboard",
    """        <h1 className="text-3xl font-bold text-corpTextDark mb-2">Installment Collections</h1>""",
    """        <div className="flex items-center gap-4 mb-6">
          <button 
            onClick={() => navigate('/admin/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-corpTextDark mb-2">Installment Collections</h1>"""
)

# Fix trailing tags in admin Payments.jsx
with open("../frontend/src/pages/admin/Payments.jsx", 'r', encoding='utf-8') as f:
    c = f.read()
target_footer = """        <h1 className="text-3xl font-bold text-corpTextDark mb-2">Installment Collections</h1>
        <p className="text-corpTextLight mb-8">Review and verify member payment receipts.</p>"""
new_footer = """        <div className="flex items-center gap-4 mb-6">
          <button 
            onClick={() => navigate('/admin/dashboard')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h1 className="text-3xl font-bold text-corpTextDark mb-2">Installment Collections</h1>
            <p className="text-corpTextLight mb-0">Review and verify member payment receipts.</p>
          </div>
        </div>"""
if target_footer in c:
    c = c.replace(target_footer, new_footer)
    with open("../frontend/src/pages/admin/Payments.jsx", 'w', encoding='utf-8') as f:
        f.write(c)

# 6. MembersList
apply_back_arrow_to_file(
    "../frontend/src/pages/admin/MembersList.jsx",
    "/admin/dashboard",
    """      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Member Management</h2>""",
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
            <h2 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Member Management</h2>"""
)

# 7. MemberDetails
apply_back_arrow_to_file(
    "../frontend/src/pages/admin/MemberDetails.jsx",
    "/admin/members",
    """        <div className="flex items-center gap-4 mb-6">
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">""",
    """        <div className="flex items-center gap-4 mb-6">
          <button 
            onClick={() => navigate('/admin/members')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">"""
)

# 8. ManagePlans
apply_back_arrow_to_file(
    "../frontend/src/pages/admin/ManagePlans.jsx",
    "/admin/dashboard",
    """      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Chit Plan Management</h2>""",
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
            <h2 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Chit Plan Management</h2>"""
)

# 9. PlanMembers
apply_back_arrow_to_file(
    "../frontend/src/pages/admin/PlanMembers.jsx",
    "/admin/plans",
    """      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Plan Members</h2>""",
    """      <div className="flex justify-between items-center mb-8">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/admin/plans')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div>
            <h2 className="text-3xl font-bold" style={{ color: '#1A2B49' }}>Plan Members</h2>"""
)

# 10. ConductDraw
apply_back_arrow_to_file(
    "../frontend/src/pages/admin/ConductDraw.jsx",
    "/admin/plans",
    """        <div className="flex items-center gap-4 mb-8">
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">""",
    """        <div className="flex items-center gap-4 mb-8">
          <button 
            onClick={() => navigate('/admin/plans')}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0 bg-white shadow-sm"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>
          <div className="w-12 h-12 bg-blue-50 rounded-xl flex items-center justify-center">"""
)

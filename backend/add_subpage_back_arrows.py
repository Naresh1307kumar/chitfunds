import os

def add_back_arrow_to_file(filepath, back_route, header_pattern, replacement_pattern):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Add ArrowLeft import if missing
    if 'ArrowLeft' not in content:
        # Find where lucide-react is imported
        import_marker = "import { "
        if import_marker in content:
            # We locate lucide-react import
            parts = content.split("} from 'lucide-react';")
            if len(parts) > 1:
                # Append ArrowLeft to the first import group
                content = parts[0] + ", ArrowLeft } from 'lucide-react';" + "} from 'lucide-react';".join(parts[1:])
            else:
                # try double quotes
                parts = content.split('} from "lucide-react";')
                if len(parts) > 1:
                    content = parts[0] + ', ArrowLeft } from "lucide-react";' + '} from "lucide-react";'.join(parts[1:])
                    
    # 2. Add useNavigate if missing (most subpages already have it)
    if 'useNavigate' not in content:
        if "import { " in content:
            content = content.replace(
                "import { Link,",
                "import { Link, useNavigate,"
            ).replace(
                "import { Routes,",
                "import { Routes, useNavigate,"
            )
            
    # 3. Add arrow button at the header pattern
    if header_pattern in content:
        back_button = f"""<button 
            onClick={{() => navigate('{back_route}')}}
            className="w-10 h-10 rounded-full border border-slate-200 hover:border-slate-355 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors flex-shrink-0"
            title="Go Back"
          >
            <ArrowLeft className="w-4 h-4" />
          </button>"""
          
        new_header = replacement_pattern.replace("ARROW_PLACEHOLDER", back_button)
        content = content.replace(header_pattern, new_header)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Successfully added back arrow to: {filepath}")
    else:
        print(f"Header pattern not found in {filepath}")

# Let's list all files and their configurations
configs = [
    # Member pages
    {
        "file": "../frontend/src/pages/member/KYCUpload.jsx",
        "route": "/member/dashboard",
        "pattern": '<div className="flex items-center gap-4 mb-6 pb-6 border-b border-gray-100">',
        "replace": '<div className="flex items-center gap-4 mb-6 pb-6 border-b border-gray-100">\n          ARROW_PLACEHOLDER'
    },
    {
        "file": "../frontend/src/pages/member/GuarantorForm.jsx",
        "route": "/member/dashboard",
        "pattern": '<div className="flex items-center gap-4 mb-6 pb-6 border-b border-gray-100">',
        "replace": '<div className="flex items-center gap-4 mb-6 pb-6 border-b border-gray-100">\n          ARROW_PLACEHOLDER'
    },
    {
        "file": "../frontend/src/pages/member/ExplorePlans.jsx",
        "route": "/member/dashboard",
        "pattern": '<div className="flex justify-between items-center mb-8 pb-6 border-b border-gray-200">',
        "replace": '<div className="flex justify-between items-center mb-8 pb-6 border-b border-gray-200">\n          <div className="flex items-center gap-4">\n            ARROW_PLACEHOLDER',
        "extra_replacement": ('<div>\n            <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">Explore Investment Plans</h2>', '<h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">Explore Investment Plans</h2>\n          </div>')
    },
    {
        "file": "../frontend/src/pages/member/Payments.jsx",
        "route": "/member/dashboard",
        "pattern": '<div className="flex items-center gap-4 mb-8">',
        "replace": '<div className="flex items-center gap-4 mb-8">\n          ARROW_PLACEHOLDER'
    },
    
    # Admin pages
    {
        "file": "../frontend/src/pages/admin/Payments.jsx",
        "route": "/admin/dashboard",
        "pattern": '<div className="flex items-center gap-4 mb-8">',
        "replace": '<div className="flex items-center gap-4 mb-8">\n          ARROW_PLACEHOLDER'
    },
    {
        "file": "../frontend/src/pages/admin/MembersList.jsx",
        "route": "/admin/dashboard",
        "pattern": '<div className="flex justify-between items-center mb-8">',
        "replace": '<div className="flex justify-between items-center mb-8">\n          <div className="flex items-center gap-4">\n            ARROW_PLACEHOLDER',
        "extra_replacement": ('<div>\n            <h2 className="text-3xl font-bold" style={{ color: \'#1A2B49\' }}>Member Management</h2>', '<h2 className="text-3xl font-bold" style={{ color: \'#1A2B49\' }}>Member Management</h2>\n          </div>')
    },
    {
        "file": "../frontend/src/pages/admin/MemberDetails.jsx",
        "route": "/admin/members",
        "pattern": '<div className="flex items-center gap-4 mb-6">',
        "replace": '<div className="flex items-center gap-4 mb-6">\n          ARROW_PLACEHOLDER'
    },
    {
        "file": "../frontend/src/pages/admin/ManagePlans.jsx",
        "route": "/admin/dashboard",
        "pattern": '<div className="flex justify-between items-center mb-8">',
        "replace": '<div className="flex justify-between items-center mb-8">\n          <div className="flex items-center gap-4">\n            ARROW_PLACEHOLDER',
        "extra_replacement": ('<div>\n            <h2 className="text-3xl font-bold" style={{ color: \'#1A2B49\' }}>Chit Plan Management</h2>', '<h2 className="text-3xl font-bold" style={{ color: \'#1A2B49\' }}>Chit Plan Management</h2>\n          </div>')
    },
    {
        "file": "../frontend/src/pages/admin/PlanMembers.jsx",
        "route": "/admin/plans",
        "pattern": '<div className="flex justify-between items-center mb-8">',
        "replace": '<div className="flex justify-between items-center mb-8">\n          <div className="flex items-center gap-4">\n            ARROW_PLACEHOLDER',
        "extra_replacement": ('<div>\n            <h2 className="text-3xl font-bold" style={{ color: \'#1A2B49\' }}>Plan Members</h2>', '<h2 className="text-3xl font-bold" style={{ color: \'#1A2B49\' }}>Plan Members</h2>\n          </div>')
    },
    {
        "file": "../frontend/src/pages/admin/ConductDraw.jsx",
        "route": "/admin/plans",
        "pattern": '<div className="flex items-center gap-4 mb-8">',
        "replace": '<div className="flex items-center gap-4 mb-8">\n          ARROW_PLACEHOLDER'
    }
]

for cfg in configs:
    add_back_arrow_to_file(cfg["file"], cfg["route"], cfg["pattern"], cfg["replace"])
    
    # Handle extra replacements for layout wrappers if present
    if "extra_replacement" in cfg and os.path.exists(cfg["file"]):
        with open(cfg["file"], 'r', encoding='utf-8') as f:
            c = f.read()
        target, replacement = cfg["extra_replacement"]
        if target in c:
            c = c.replace(target, replacement)
            with open(cfg["file"], 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Applied extra layout fix to: {cfg['file']}")

content = open('src/pages/admin/ManagePlans.jsx', 'r', encoding='utf-8').read()
lines = content.split('\n')

# 1. Insert "Chit Type" inside card details (around lines 169-170)
# Locate lines:
#                 <div className="flex justify-between text-sm">
#                   <span className="text-gray-500">Members:</span>
#                   <span className="font-semibold text-gray-900">{plan.current_members} / {plan.total_members}</span>
#                 </div>

idx_member = -1
for i, l in enumerate(lines):
    if '{plan.current_members} / {plan.total_members}' in l:
        idx_member = i
        break

if idx_member != -1:
    lines.insert(idx_member + 2, '                <div className="flex justify-between text-sm">')
    lines.insert(idx_member + 3, '                  <span className="text-gray-500">Chit Type:</span>')
    lines.insert(idx_member + 4, '                  <span className="font-semibold text-blue-600">{plan.chit_type === \'auction\' ? \'Auction (Yela)\' : \'Lucky Draw (Koolukal)\'}</span>')
    lines.insert(idx_member + 5, '                </div>')
    print('Inserted Chit Type in card view.')

# 2. Insert "Chit Type" dropdown inside form modal (above Monthly Amount, around lines 210)
idx_form_div = -1
for i, l in enumerate(lines):
    if '<div className="grid grid-cols-2 gap-4">' in l:
        idx_form_div = i
        break

if idx_form_div != -1:
    lines.insert(idx_form_div, '                <div>')
    lines.insert(idx_form_div + 1, '                  <label className="block text-sm font-semibold text-gray-700 mb-1">Chit Type</label>')
    lines.insert(idx_form_div + 2, '                  <select name="chit_type" value={formData.chit_type} onChange={handleInputChange} className="w-full px-4 py-2 border rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-blue-500">')
    lines.insert(idx_form_div + 3, '                    <option value="lucky_draw">Lucky Draw (Koolukal)</option>')
    lines.insert(idx_form_div + 4, '                    <option value="auction">Auction (Yela)</option>')
    lines.insert(idx_form_div + 5, '                  </select>')
    lines.insert(idx_form_div + 6, '                </div>')
    print('Inserted Chit Type select field in form.')

open('src/pages/admin/ManagePlans.jsx', 'w', encoding='utf-8').write('\n'.join(lines))
print('ManagePlans update completed.')

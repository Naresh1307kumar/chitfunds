content = open('src/pages/admin/ManagePlans.jsx', 'r', encoding='utf-8').read()
lines = content.split('\n')

# 1. Update initial formData (around lines 14-22)
lines[13:22] = [
    '  const [formData, setFormData] = useState({',
    '    plan_name: \'\',',
    '    plan_type: \'silver\',',
    '    chit_type: \'lucky_draw\',',
    '    monthly_amount: \'\',',
    '    total_members: \'\',',
    '    duration_months: \'\',',
    '    commission_rate: 5.0,',
    '    start_date: \'\'',
    '  });'
]

# 2. Update openCreateModal (around lines 45-50)
lines[44:50] = [
    '    setFormData({',
    '      plan_name: \'\', plan_type: \'silver\', chit_type: \'lucky_draw\', monthly_amount: \'\', total_members: \'\',',
    '      duration_months: \'\', commission_rate: 5.0, start_date: \'\'',
    '    });'
]

# 3. Update openEditModal (around lines 53-62)
lines[53:62] = [
    '    setFormData({',
    '      plan_name: plan.plan_name,',
    '      plan_type: plan.plan_type,',
    '      chit_type: plan.chit_type || \'lucky_draw\',',
    '      monthly_amount: plan.monthly_amount,',
    '      total_members: plan.total_members,',
    '      duration_months: plan.duration_months,',
    '      commission_rate: plan.commission_rate,',
    '      start_date: plan.start_date',
    '    });'
]

# Write out to verify the lines so far
open('src/pages/admin/ManagePlans.jsx', 'w', encoding='utf-8').write('\n'.join(lines))
print('Part 1 of ManagePlans update successful.')

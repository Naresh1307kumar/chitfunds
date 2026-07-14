content = open('src/App.jsx', 'r', encoding='utf-8').read()
lines = content.split('\n')

new_block = [
    '  // Bid % decreases linearly: 20% (month 1) -> 5% (last month)',
    '  const getBidPct = (month) => {',
    '    if (duration === 1) return 0.20;',
    '    const maxBid = 0.20, minBid = 0.05;',
    '    return maxBid - ((maxBid - minBid) / (duration - 1)) * (month - 1);',
    '  };',
    '',
    '  // Pre-calculate monthly data to get actual total paid including dividends',
    '  const monthlyData = Array.from({ length: duration }, (_, i) => {',
    '    const month = i + 1;',
    '    const bidPct = getBidPct(month);',
    '    const bidAmount = chitValue * bidPct;',
    '    const dividend = Math.max(0, (bidAmount - commissionPerMonth) / N);',
    '    const netPay = monthly - dividend;',
    '    return { month, bidPct, winnerPrize: chitValue - bidAmount, dividend, netPay };',
    '  });',
    '',
    '  const totalPaidByMember = monthlyData.reduce((sum, item) => sum + item.netPay, 0);',
    '',
    '  // Per-month dynamic calculation',
    '  const projections = monthlyData.map(item => {',
    '    const winnerNetInterest = totalPaidByMember - item.winnerPrize; // positive = interest cost',
    '    return {',
    '      month: item.month,',
    '      bidPct: Math.round(item.bidPct * 100),',
    '      winnerPrize: Math.round(item.winnerPrize),',
    '      winnerNetInterest: Math.round(winnerNetInterest),',
    '      dividend: Math.round(item.dividend),',
    '      netPay: Math.round(item.netPay),',
    '    };',
    '  });'
]

# Lines 521-546 (0-indexed: 520-545)
new_lines = lines[:520] + new_block + lines[546:]
open('src/App.jsx', 'w', encoding='utf-8').write('\n'.join(new_lines))
print('Success!')

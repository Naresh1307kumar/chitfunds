import sys

content = open('src/App.jsx', 'r', encoding='utf-8').read()
lines = content.split('\n')

new_block = [
    '          {/* Month-by-Month Breakdown Table */}',
    '          <div>',
    '            <h3 className="font-bold text-base text-slate-900 mb-1">Month-by-Month Prize Breakdown</h3>',
    '            <p className="text-xs text-slate-400 mb-3">',
    '              \u0b8e\u0ba8\u0bcd\u0ba4 \u0bae\u0bbe\u0b9a\u0bae\u0bcd draw \u0bb5\u0ba8\u0bcd\u0ba4\u0bbe\u0bb2\u0bc1\u0bae\u0bcd \u2014 winner-\u0b95\u0bcd\u0b95\u0bc1 \u0b8e\u0bb5\u0bcd\u0bb5\u0bb3\u0bcb \u0b95\u0bbf\u0b9f\u0bc8\u0b95\u0bcd\u0b95\u0bc1\u0bae\u0bcd, \u0b8e\u0bb5\u0bcd\u0bb5\u0bb3\u0bcb interest pay \u0baa\u0ba3\u0bcd\u0ba3\u0ba3\u0bc1\u0bae\u0bcd.',
    '            </p>',
    '            <div className="border border-slate-200 rounded-2xl overflow-hidden shadow-sm">',
    '              <div className="max-h-72 overflow-y-auto">',
    '                <table className="w-full text-left border-collapse">',
    '                  <thead className="sticky top-0 z-10">',
    '                    <tr className="bg-slate-50 border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-500">',
    '                      <th className="px-5 py-3">Month</th>',
    '                      <th className="px-5 py-3 text-blue-600">Winner \u0b95\u0bbf\u0b9f\u0bc8\u0b95\u0bcd\u0b95\u0bc1\u0bae\u0bcd Amount</th>',
    '                      <th className="px-5 py-3 text-red-500">Interest Pay \u0baa\u0ba3\u0bcd\u0ba3\u0ba3\u0bc1\u0bae\u0bcd</th>',
    '                    </tr>',
    '                  </thead>',
    '                  <tbody className="divide-y divide-slate-100">',
    '                    {projections.map((p) => (',
    '                      <tr key={p.month} className="hover:bg-blue-50/30 transition-colors">',
    '                        <td className="px-5 py-3 font-semibold text-slate-700">',
    '                          Month {p.month}',
    '                          {p.month === duration && (',
    '                            <span className="ml-2 text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded-full font-bold">Last</span>',
    '                          )}',
    '                        </td>',
    '                        <td className="px-5 py-3 font-bold text-blue-700 text-base">',
    '                          \u20b9{p.winnerPrize.toLocaleString()}',
    '                        </td>',
    '                        <td className="px-5 py-3">',
    '                          {p.winnerNetInterest > 0 ? (',
    '                            <span className="text-red-500 font-semibold">\u20b9{p.winnerNetInterest.toLocaleString()}</span>',
    '                          ) : (',
    '                            <span className="text-emerald-600 font-semibold">\u20b90 (No loss!)</span>',
    '                          )}',
    '                        </td>',
    '                      </tr>',
    '                    ))}',
    '                  </tbody>',
    '                </table>',
    '              </div>',
    '            </div>',
    '            <div className="mt-3 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 text-xs text-amber-800">',
    '              \U0001f4a1 <strong>Note:</strong> Early month-\u0bb2\u0bcd winner \u0b95\u0bae\u0bcd\u0bae\u0bbf prize, \u0b85\u0ba4\u0bbf\u0b95 interest. Last month-\u0bb2\u0bcd winner \u0b85\u0ba4\u0bbf\u0b95 prize, \u0b95\u0bae\u0bcd\u0bae\u0bbf interest.',
    '            </div>',
    '          </div>',
]

# Replace lines 600-644 (0-indexed: 599-643)
new_lines = lines[:599] + new_block + lines[644:]
open('src/App.jsx', 'w', encoding='utf-8').write('\n'.join(new_lines))
print('Done! Lines replaced successfully.')

import re

with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app = f.read()

# 1. Define PlanDetailsModal component
details_modal_code = """
const PlanDetailsModal = ({ plan, onClose, onJoin }) => {
  const totalValue = plan.monthlyAmount * 12;
  const commission = totalValue * 0.05;
  const netPrize = totalValue - commission;
  const maxDiscount = totalValue * 0.30;

  // Mock Dividend projections for 12 months
  const projections = [
    { month: 1, bid: "30% (Max)", dividend: (totalValue * 0.30) / 12, actualPay: plan.monthlyAmount - ((totalValue * 0.30) / 12) },
    { month: 2, bid: "25%", dividend: (totalValue * 0.25) / 12, actualPay: plan.monthlyAmount - ((totalValue * 0.25) / 12) },
    { month: 3, bid: "20%", dividend: (totalValue * 0.20) / 12, actualPay: plan.monthlyAmount - ((totalValue * 0.20) / 12) },
    { month: "4-12 (Avg)", bid: "15%", dividend: (totalValue * 0.15) / 12, actualPay: plan.monthlyAmount - ((totalValue * 0.15) / 12) }
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl border border-slate-100 flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="px-8 py-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center border border-blue-100">
              <plan.icon className="w-6 h-6 text-corpBlue" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-slate-900">{plan.name} Overview</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-50 text-blue-600 border border-blue-150 uppercase tracking-wider">{plan.badge}</span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 text-3xl font-light">&times;</button>
        </div>

        {/* Content */}
        <div className="p-8 overflow-y-auto flex-grow space-y-6 text-slate-700 text-sm">
          
          {/* Key Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div className="bg-slate-50 rounded-2xl p-4 border border-slate-150 text-center">
              <span className="text-xs text-slate-400 block mb-1">Monthly Dues</span>
              <strong className="text-lg font-bold text-slate-900">₹{plan.monthlyAmount.toLocaleString()}</strong>
            </div>
            <div className="bg-slate-50 rounded-2xl p-4 border border-slate-150 text-center">
              <span className="text-xs text-slate-400 block mb-1">Total Pool Value</span>
              <strong className="text-lg font-bold text-slate-900">₹{totalValue.toLocaleString()}</strong>
            </div>
            <div className="bg-slate-50 rounded-2xl p-4 border border-slate-150 text-center">
              <span className="text-xs text-slate-400 block mb-1">Net Prize Payout</span>
              <strong className="text-lg font-bold text-slate-900">₹{netPrize.toLocaleString()}</strong>
            </div>
            <div className="bg-slate-50 rounded-2xl p-4 border border-slate-150 text-center">
              <span className="text-xs text-slate-400 block mb-1">Commission (5%)</span>
              <strong className="text-lg font-bold text-slate-900">₹{commission.toLocaleString()}</strong>
            </div>
          </div>

          {/* About Scheme */}
          <div>
            <h3 className="font-bold text-base text-slate-900 mb-2">About This Scheme</h3>
            <p className="text-slate-500 leading-relaxed">
              This is a structured 12-month savings group consisting of 12 verified members. Every month, an auction is held. Members bid for the prize pool by offering a discount (up to 30%). The winning bidder gets the net prize money, and their offered discount is distributed equally among all members as a dividend, reducing the next installment payment.
            </p>
          </div>

          {/* Dividend Projections */}
          <div>
            <h3 className="font-bold text-base text-slate-900 mb-2">Estimated Dividend Projections</h3>
            <div className="border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-500">
                    <th className="px-6 py-3">Month</th>
                    <th className="px-6 py-3">Winning Bid</th>
                    <th className="px-6 py-3">Your Dividend Reward</th>
                    <th className="px-6 py-3">Your Net Pay</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-slate-600">
                  {projections.map((p, idx) => (
                    <tr key={idx} className="hover:bg-slate-50/50">
                      <td className="px-6 py-3 font-semibold text-slate-800">Month {p.month}</td>
                      <td className="px-6 py-3">{p.bid}</td>
                      <td className="px-6 py-3 text-emerald-600 font-medium">+₹{p.dividend.toLocaleString()}</td>
                      <td className="px-6 py-3 font-bold text-slate-900">₹{p.actualPay.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="text-[11px] text-slate-400 mt-2 italic">*Note: Bids vary based on mutual agreements and market competition. Higher bids result in bigger dividends for other members.</p>
          </div>

          {/* Protection & Insurance */}
          <div className="bg-blue-50 border border-blue-150 rounded-2xl p-4 flex gap-3 items-start">
            <span className="text-lg">🛡️</span>
            <div>
              <h4 className="font-bold text-slate-900 text-sm">Corporate Legal Protection</h4>
              <p className="text-xs text-slate-500 mt-0.5 leading-relaxed">
                All plans are legally registered under corporate chit laws. If any member defaults, corporate security funds cover the pool payouts immediately, ensuring absolute safety for your savings.
              </p>
            </div>
          </div>

        </div>

        {/* Footer */}
        <div className="px-8 py-5 border-t border-slate-100 bg-slate-50 flex justify-between items-center">
          <button onClick={onClose} className="px-5 py-2.5 border border-slate-300 text-slate-600 font-semibold rounded-xl text-sm hover:bg-slate-100 transition-colors">Close</button>
          <button onClick={() => { onJoin(plan); onClose(); }} className="px-6 py-2.5 bg-corpBlue text-white font-bold rounded-xl text-sm hover:bg-corpNavy transition-colors flex items-center gap-1.5 shadow-md">
            Proceed to Join Plan &rarr;
          </button>
        </div>

      </div>
    </div>
  );
};
"""

# Insert PlanDetailsModal before JoinPlanModal
app = app.replace('const JoinPlanModal = ', details_modal_code + '\nconst JoinPlanModal = ')

# Update LandingPage implementation to support details modal state
old_landing_states = """export const LandingPage = () => {
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [selectedPlan, setSelectedPlan] = React.useState(null);

  const handleJoinPlan = (plan) => {
    setSelectedPlan(plan);
    setIsModalOpen(true);
  };

  return ("""

new_landing_states = """export const LandingPage = () => {
  const [isModalOpen, setIsModalOpen] = React.useState(false);
  const [isDetailsOpen, setIsDetailsOpen] = React.useState(false);
  const [selectedPlan, setSelectedPlan] = React.useState(null);

  const handleJoinPlan = (plan) => {
    setSelectedPlan(plan);
    setIsModalOpen(true);
  };

  const handleViewDetails = (plan) => {
    setSelectedPlan(plan);
    setIsDetailsOpen(true);
  };

  return ("""

app = app.replace(old_landing_states, new_landing_states)

# Add Modal rendering near footer in LandingPage
old_footer_modal_block = """      {isModalOpen && <JoinPlanModal plan={selectedPlan} onClose={() => setIsModalOpen(false)} />}
    </div>
  );
};"""

new_footer_modal_block = """      {isModalOpen && <JoinPlanModal plan={selectedPlan} onClose={() => setIsModalOpen(false)} />}
      {isDetailsOpen && <PlanDetailsModal plan={selectedPlan} onClose={() => setIsDetailsOpen(false)} onJoin={handleJoinPlan} />}
    </div>
  );
};"""

app = app.replace(old_footer_modal_block, new_footer_modal_block)

# Update ChitPlans call and inside button trigger
old_chit_plans_instance = "<ChitPlans onJoinPlan={handleJoinPlan} />"
new_chit_plans_instance = "<ChitPlans onJoinPlan={handleJoinPlan} onViewDetails={handleViewDetails} />"
app = app.replace(old_chit_plans_instance, new_chit_plans_instance)

# Update ChitPlans signature
old_chit_plans_sig = "const ChitPlans = ({ onJoinPlan }) => {"
new_chit_plans_sig = "const ChitPlans = ({ onJoinPlan, onViewDetails }) => {"
app = app.replace(old_chit_plans_sig, new_chit_plans_sig)

# Update View Details button action
old_view_details_btn = """                  <button className="w-full py-3 rounded font-bold transition-colors bg-cardBg text-slate-700 border border-cardBorder hover:bg-bgAlt1" onClick={() => alert('View Details clicked')}>
                    View Details
                  </button>"""

new_view_details_btn = """                  <button className="w-full py-3 rounded font-bold transition-colors bg-cardBg text-slate-700 border border-cardBorder hover:bg-bgAlt1" onClick={() => onViewDetails(plan)}>
                    View Details
                  </button>"""

app = app.replace(old_view_details_btn, new_view_details_btn)

with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app)

print("App.jsx successfully updated with PlanDetailsModal!")

with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app = f.read()

# 1. Update JoinPlanModal instantiation in LandingPage to pass onBackToDetails
old_modal_instantiation = "{isModalOpen && <JoinPlanModal plan={selectedPlan} onClose={() => setIsModalOpen(false)} />}"
new_modal_instantiation = "{isModalOpen && <JoinPlanModal plan={selectedPlan} onClose={() => setIsModalOpen(false)} onBackToDetails={() => { setIsModalOpen(false); setIsDetailsOpen(true); }} />}"

if old_modal_instantiation in app:
    app = app.replace(old_modal_instantiation, new_modal_instantiation)
else:
    # Just in case spacing is different
    app = app.replace(
        "isModalOpen && <JoinPlanModal plan={selectedPlan} onClose={() => setIsModalOpen(false)} />",
        "isModalOpen && <JoinPlanModal plan={selectedPlan} onClose={() => setIsModalOpen(false)} onBackToDetails={() => { setIsModalOpen(false); setIsDetailsOpen(true); }} />"
    )

# 2. Update JoinPlanModal component signature to accept onBackToDetails
old_modal_signature = "const JoinPlanModal = ({ plan, onClose }) => {"
new_modal_signature = "const JoinPlanModal = ({ plan, onClose, onBackToDetails }) => {"

app = app.replace(old_modal_signature, new_modal_signature)

# 3. Add Back button to Step 0 in JoinPlanModal pointing to onBackToDetails
old_step0_buttons = """              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
                <button 
                  onClick={() => { onClose(); navigate('/login'); }}
                  className="px-6 py-3 border border-slate-350 hover:bg-slate-50 text-slate-700 font-bold rounded-xl text-sm transition-colors"
                >
                  Yes, I have an account (Log In)
                </button>
                <button 
                  onClick={() => setStep(1)}
                  className="px-6 py-3 bg-corpBlue hover:bg-corpNavy text-white font-bold rounded-xl text-sm transition-colors shadow-md"
                >
                  No, I need to register
                </button>
              </div>"""

new_step0_buttons = """              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
                <button 
                  onClick={() => { onClose(); navigate('/login'); }}
                  className="px-6 py-3 border border-slate-350 hover:bg-slate-50 text-slate-700 font-bold rounded-xl text-sm transition-colors"
                >
                  Yes, I have an account (Log In)
                </button>
                <button 
                  onClick={() => setStep(1)}
                  className="px-6 py-3 bg-corpBlue hover:bg-corpNavy text-white font-bold rounded-xl text-sm transition-colors shadow-md"
                >
                  No, I need to register
                </button>
              </div>
              <div className="pt-2">
                <button 
                  onClick={onBackToDetails}
                  className="text-xs text-slate-500 hover:text-corpBlue font-bold underline transition-colors"
                >
                  &larr; Back to Plan Details
                </button>
              </div>"""

app = app.replace(old_step0_buttons, new_step0_buttons)

with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
    f.write(app)

print("JoinPlanModal back navigation to Details Modal successfully implemented!")

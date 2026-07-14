with open('../frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    app = f.read()

landing_page_code = """
export const LandingPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [selectedPlan, setSelectedPlan] = useState(null);

  const handleJoinPlan = (plan) => {
    setSelectedPlan(plan);
    setIsModalOpen(true);
  };

  const handleViewDetails = (plan) => {
    setSelectedPlan(plan);
    setIsDetailsOpen(true);
  };

  return (
    <div className="min-h-screen flex flex-col font-sans bg-[#F8FAFC] text-slate-800 relative">
      {/* Background Pattern Overlay */}
      <div 
        className="fixed inset-0 bg-cover bg-center pointer-events-none z-0" 
        style={{ 
          backgroundImage: "url('/images/bg_abstract_finance.png')", 
          opacity: 0.04,
        }}
      ></div>
      <Navbar />
      <main className="flex-grow relative z-10">
        <HeroSection />
        <AboutUsSection />
        <ChitPlans onJoinPlan={handleJoinPlan} onViewDetails={handleViewDetails} />
        <Features />
        <Rules />
        <Testimonials />
        <Contact />
      </main>
      <Footer />

      {isModalOpen && <JoinPlanModal plan={selectedPlan} onClose={() => setIsModalOpen(false)} />}
      {isDetailsOpen && <PlanDetailsModal plan={selectedPlan} onClose={() => setIsDetailsOpen(false)} onJoin={handleJoinPlan} />}
    </div>
  );
};
"""

target = "const ScrollToTop = () => {"

if target in app:
    app = app.replace(target, landing_page_code + "\n\n" + target)
    with open('../frontend/src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(app)
    print("LandingPage component successfully restored!")
else:
    print("Error: ScrollToTop target not found in App.jsx!")

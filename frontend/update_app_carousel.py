import sys

file_path = "src/App.jsx"
content = open(file_path, "r", encoding="utf-8").read()

# 1. Add ChevronLeft, Coins to lucide-react imports if missing
if "ChevronLeft" not in content:
    content = content.replace("ChevronRight, CheckCircle", "ChevronRight, ChevronLeft, Coins, CheckCircle")

# 2. Update Plans component in App.jsx
old_plans_section = """const Plans = ({ onJoinPlan, onViewDetails }) => {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPublicPlans = async () => {
      try {
        const res = await api.get('/api/v1/plans/public');
        const mappedPlans = res.data.map(p => {
          let IconComp = Shield;
          let badgeText = "Standard";
          let isPopular = false;

          if (p.plan_type === 'gold') {
            IconComp = Crown;
            badgeText = "Premium";
          } else if (p.plan_type === 'silver') {
            IconComp = Zap;
            badgeText = "Most Popular";
            isPopular = true;
          }

          return {
            id: p.id,
            name: p.plan_name,
            monthlyAmount: p.monthly_amount,
            duration: p.duration_months,
            totalMembers: p.total_members,
            commissionRate: p.commission_rate,
            return: p.total_value,
            chitType: p.chit_type,
            icon: IconComp,
            badge: badgeText,
            popular: isPopular
          };
        });
        setPlans(mappedPlans);
      } catch (err) {
        console.error('Failed to fetch public plans:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPublicPlans();
  }, []);

  if (loading) {
    return (
      <section className="section-gray" id="plans">
        <div className="text-center py-10 text-slate-500 font-medium">Loading investment plans...</div>
      </section>
    );
  }

  if (plans.length === 0) {
    return (
      <section className="section-gray" id="plans">
        <div className="max-w-7xl mx-auto px-4 text-center py-10">
          <h2 className="text-3xl font-bold text-corpNavy mb-2">Investment Plans</h2>
          <p className="text-slate-500">No active investment plans available at the moment. Please check back later!</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section-gray" id="plans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="text-center mb-10" data-aos="fade-up">
          <h2 className="text-4xl md:text-5xl font-bold text-corpNavy mb-6 tracking-tight">Investment Plans</h2>
          <p className="text-lg text-corpTextLight">Choose from our most rewarding investment plans tailored for your growth.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
          {plans.map((plan, index) => (
            <div key={index} data-aos="fade-up" data-aos-delay={index * 150} className="plan-card-popular shadow-md hover:shadow-xl transition-all duration-300 relative overflow-hidden rounded-3xl border border-slate-100 flex flex-col bg-white">
              
              <div className={`${plan.chitType === 'auction' ? 'bg-corpGold' : 'bg-blue-600'} text-white text-center py-2.5 text-xs font-extrabold uppercase tracking-widest`}>
                {plan.chitType === 'auction' ? 'Auction Plan' : 'Lucky Draw Plan'}
              </div>

              <div className="p-8 border-b border-gray-100 flex-grow">
                <div className="flex justify-between items-start mb-6">
                  <div className="w-12 h-12 rounded bg-bgAlt2 flex items-center justify-center border border-cardBorder">
                    {(() => { const PlanIcon = plan.icon || Shield; return <PlanIcon className="w-6 h-6 text-corpBlue" />; })()}
                  </div>
                  <span className="px-3 py-1 rounded text-xs font-bold uppercase tracking-wider bg-bgAlt2 text-corpTextLight border border-cardBorder">
                    {plan.badge}
                  </span>
                </div>

                <h3 className="text-2xl font-bold text-slate-800 mb-4">{plan.name}</h3>
                
                <div className="flex items-baseline gap-1">
                  <span className="text-5xl font-extrabold text-corpBlue tracking-tight">₹{plan.monthlyAmount.toLocaleString()}</span>
                  <span className="font-medium text-corpTextLight">/month</span>
                </div>
              </div>

              <div className="p-8">
                <ul className="space-y-5 mb-6 text-slate-700">
                  <li className="flex items-center gap-4">
                    <CheckCircle2 className="w-5 h-5 text-corpBlue" />
                    <span>Duration: <strong className="font-semibold">{plan.duration} Months</strong></span>
                  </li>
                  <li className="flex items-center gap-4">
                    <CheckCircle2 className="w-5 h-5 text-corpBlue" />
                    <span>Est. Return: <strong className="font-semibold">₹{plan.return.toLocaleString()}</strong></span>
                  </li>
                </ul>
                <div className="space-y-4">
                  <button className="w-full py-3 rounded font-bold transition-colors bg-cardBg text-slate-700 border border-cardBorder hover:bg-bgAlt1" onClick={() => onViewDetails(plan)}>
                    View Details
                  </button>
                  <button className={`w-full py-3 rounded font-bold transition-colors flex justify-center items-center gap-2 ${plan.popular ? 'btn-primary' : 'bg-bgAlt2 text-corpBlue hover:bg-bgAlt1 border border-cardBorder'}`} onClick={() => onJoinPlan(plan)}>
                    Join Plan <ChevronRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};"""

new_plans_section = """const Plans = ({ onJoinPlan, onViewDetails }) => {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const scrollRef = React.useRef(null);

  const scroll = (direction) => {
    if (scrollRef.current) {
      const { scrollLeft, clientWidth } = scrollRef.current;
      const scrollAmount = clientWidth * 0.8;
      scrollRef.current.scrollTo({
        left: direction === 'left' ? scrollLeft - scrollAmount : scrollLeft + scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  useEffect(() => {
    const fetchPublicPlans = async () => {
      try {
        const res = await api.get('/api/v1/plans/public');
        const mappedPlans = res.data.map(p => {
          let IconComp = Shield;
          let badgeText = "Standard";
          let isPopular = false;

          if (p.plan_type === 'gold') {
            IconComp = Crown;
            badgeText = "Premium";
          } else if (p.plan_type === 'silver') {
            IconComp = Zap;
            badgeText = "Most Popular";
            isPopular = true;
          }

          return {
            id: p.id,
            name: p.plan_name,
            monthlyAmount: p.monthly_amount,
            duration: p.duration_months,
            totalMembers: p.total_members,
            commissionRate: p.commission_rate,
            return: p.total_value,
            chitType: 'auction',
            icon: IconComp,
            badge: badgeText,
            popular: isPopular
          };
        });
        setPlans(mappedPlans);
      } catch (err) {
        console.error('Failed to fetch public plans:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchPublicPlans();
  }, []);

  if (loading) {
    return (
      <section className="section-gray" id="plans">
        <div className="text-center py-10 text-slate-500 font-medium">Loading investment plans...</div>
      </section>
    );
  }

  if (plans.length === 0) {
    return (
      <section className="section-gray" id="plans">
        <div className="max-w-7xl mx-auto px-4 text-center py-10">
          <h2 className="text-3xl font-bold text-corpNavy mb-2">Investment Plans</h2>
          <p className="text-slate-500">No active investment plans available at the moment. Please check back later!</p>
        </div>
      </section>
    );
  }

  return (
    <section className="section-gray py-16" id="plans">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        
        {/* Section Header with Left / Right Scroll Buttons */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8" data-aos="fade-up">
          <div>
            <span className="text-xs font-extrabold uppercase tracking-widest text-amber-600 bg-amber-50 px-3 py-1 rounded-full border border-amber-200 mb-2 inline-block">
              Auction Chit Schemes
            </span>
            <h2 className="text-3xl md:text-5xl font-bold text-corpNavy tracking-tight">Available Chit Plans</h2>
            <p className="text-slate-500 text-sm md:text-base mt-2">Scroll horizontally to explore our high-yield auction investment schemes.</p>
          </div>

          <div className="flex items-center gap-3 mt-4 md:mt-0">
            <button 
              onClick={() => scroll('left')}
              className="w-11 h-11 rounded-full border border-slate-200 hover:border-corpBlue bg-white hover:bg-blue-50 text-slate-600 hover:text-corpBlue flex items-center justify-center transition-all shadow-sm active:scale-95"
              title="Previous Plans"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button 
              onClick={() => scroll('right')}
              className="w-11 h-11 rounded-full border border-slate-200 hover:border-corpBlue bg-white hover:bg-blue-50 text-slate-600 hover:text-corpBlue flex items-center justify-center transition-all shadow-sm active:scale-95"
              title="Next Plans"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Horizontal Carousel Track */}
        <div 
          ref={scrollRef} 
          className="flex gap-6 overflow-x-auto snap-x snap-mandatory scrollbar-none pb-8 pt-2 px-1 scroll-smooth"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {plans.map((plan, index) => (
            <div 
              key={index} 
              className="min-w-[300px] sm:min-w-[350px] max-w-[360px] flex-shrink-0 snap-start shadow-sm hover:shadow-xl transition-all duration-300 relative overflow-hidden rounded-3xl border border-slate-200 flex flex-col bg-white group hover:-translate-y-1"
            >
              <div className="bg-gradient-to-r from-amber-500 to-orange-500 text-white text-center py-2.5 text-xs font-extrabold uppercase tracking-widest flex items-center justify-center gap-1.5 shadow-inner">
                <Coins className="w-4 h-4" /> Auction Scheme
              </div>

              <div className="p-7 border-b border-slate-100 flex-grow">
                <div className="flex justify-between items-start mb-5">
                  <div className="w-12 h-12 rounded-2xl bg-amber-50 flex items-center justify-center border border-amber-100 shadow-sm">
                    {(() => { const PlanIcon = plan.icon || Shield; return <PlanIcon className="w-6 h-6 text-amber-600" />; })()}
                  </div>
                  <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-200">
                    {plan.badge}
                  </span>
                </div>

                <h3 className="text-xl font-bold text-slate-900 mb-3 group-hover:text-corpBlue transition-colors">{plan.name}</h3>
                
                <div className="flex items-baseline gap-1 mb-2">
                  <span className="text-4xl font-extrabold text-corpBlue tracking-tight">₹{plan.monthlyAmount.toLocaleString()}</span>
                  <span className="font-medium text-slate-500 text-sm">/month</span>
                </div>
                <p className="text-xs text-slate-400 font-medium">Total Value: <strong className="text-slate-700">₹{plan.return.toLocaleString()}</strong></p>
              </div>

              <div className="p-7 bg-slate-50/50">
                <ul className="space-y-3.5 mb-6 text-slate-700 text-xs">
                  <li className="flex items-center gap-3">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                    <span>Duration: <strong className="font-semibold text-slate-900">{plan.duration} Months</strong></span>
                  </li>
                  <li className="flex items-center gap-3">
                    <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                    <span>Total Pool: <strong className="font-semibold text-slate-900">₹{plan.return.toLocaleString()}</strong></span>
                  </li>
                </ul>
                <div className="space-y-2.5">
                  <button 
                    className="w-full py-2.5 rounded-xl text-xs font-bold transition-all bg-white text-slate-700 border border-slate-200 hover:bg-slate-100 shadow-sm" 
                    onClick={() => onViewDetails(plan)}
                  >
                    View Details
                  </button>
                  <button 
                    className="w-full py-2.5 rounded-xl text-xs font-bold transition-all flex justify-center items-center gap-2 bg-gradient-to-r from-blue-600 to-corpBlue text-white hover:from-blue-700 hover:to-blue-900 shadow-md hover:shadow-lg" 
                    onClick={() => onJoinPlan(plan)}
                  >
                    Join Scheme <ChevronRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};"""

if old_plans_section in content:
    content = content.replace(old_plans_section, new_plans_section)
    open(file_path, "w", encoding="utf-8").write(content)
    print("App.jsx Plans section updated to horizontal carousel!")
else:
    print("Could not match exact snippet in App.jsx. Manual update required.")

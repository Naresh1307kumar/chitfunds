import React, { useState, useEffect } from 'react';
import { Routes, Route, Link, useLocation, useNavigate } from 'react-router-dom';
import api from './services/api';
import Login from './pages/public/Login';
import Register from './pages/public/Register';
import AdminLogin from './pages/public/AdminLogin';
import ForgotPassword from './pages/public/ForgotPassword';
import ResetPassword from './pages/public/ResetPassword';
import MemberDashboard from './pages/member/Dashboard';
import KYCUpload from './pages/member/KYCUpload';
import GuarantorForm from './pages/member/GuarantorForm';
import AdminDashboard from './pages/admin/Dashboard';
import MembersList from './pages/admin/MembersList';
import MemberDetails from './pages/admin/MemberDetails';
import ManagePlans from './pages/admin/ManagePlans';
import PlanMembers from './pages/admin/PlanMembers';
import ConductDraw from './pages/admin/ConductDraw';
import ExplorePlans from './pages/member/ExplorePlans';
import MemberPayments from './pages/member/Payments';
import AdminPayments from './pages/admin/Payments';
import PronoteManagement from './pages/admin/PronoteManagement';
import { MemberLayout } from './components/MemberLayout';
import { AdminLayout } from './components/AdminLayout';
import { ProtectedRoute, RoleRoute } from './components/ProtectedRoute';
import { useAuth } from './context/AuthContext';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { 
  ShieldCheck, Menu, X, ArrowRight, ArrowLeft, Users, CalendarDays, 
  BellRing, BarChart3, CheckCircle2, Phone, Mail, MapPin,
  Star, Lock, TrendingUp, HeartHandshake, Zap, Crown, Shield,
  Globe, Clock, Award, ChevronRight, ChevronLeft, Coins, CheckCircle, Github, Twitter, Linkedin
} from 'lucide-react';

const Loader = ({ onComplete }) => {
  useEffect(() => {
    const timer = setTimeout(onComplete, 1200);
    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div className="fixed inset-0 z-[100] flex flex-col items-center justify-center bg-bgAlt1">
      <div className="relative">
        <ShieldCheck className="w-20 h-20 text-corpBlue relative z-10" />
        <div className="absolute top-0 left-0 w-full h-full border-4 border-transparent border-t-corpGold rounded-full animate-spin-slow"></div>
      </div>
      <h2 className="mt-8 text-2xl font-bold text-corpBlue tracking-wide">
        SecureChit
      </h2>
    </div>
  );
};

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { user } = useAuth();
  const navLinks = ['Home', 'Plans', 'Features', 'Rules', 'Contact'];

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  const dashboardPath = user?.role === 'admin' ? '/admin/dashboard' : '/member/dashboard';

  return (
    <nav className={`fixed w-full z-50 top-0 transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md py-3 sm:py-4 shadow-md border-b border-slate-200/60' : 'bg-transparent py-4 sm:py-6 border-b border-transparent'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2" data-aos="fade-right">
            <ShieldCheck className="h-7 w-7 sm:h-8 sm:w-8 text-corpBlue" />
            <span className="text-xl sm:text-2xl font-bold text-corpNavy tracking-tight">
              SecureChit
            </span>
          </div>
          <div className="hidden md:flex items-center space-x-8 lg:space-x-10" data-aos="fade-down">
            {navLinks.map((link) => (
              <a key={link} href={`#${link.toLowerCase()}`} className="text-corpTextLight hover:text-corpBlue transition-colors text-base lg:text-lg font-bold tracking-wide">
                {link}
              </a>
            ))}
            {user ? (
              <Link to={dashboardPath} className="btn-primary py-2.5 px-6 lg:py-3 lg:px-8 text-base font-bold inline-block text-center shadow-lg">
                Dashboard
              </Link>
            ) : (
              <Link to="/login" className="btn-primary py-2.5 px-6 lg:py-3 lg:px-8 text-base font-bold inline-block text-center shadow-lg">
                Login
              </Link>
            )}
          </div>
          <div className="md:hidden flex items-center">
            <button onClick={() => setIsOpen(!isOpen)} className="text-slate-700 hover:text-corpBlue p-2 rounded-lg focus:outline-none" aria-label="Toggle navigation">
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>
      {isOpen && (
        <div className="fixed inset-0 z-[100] bg-white flex flex-col h-screen w-screen overflow-hidden animate-fade-in font-sans [ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          {/* Mobile Full Screen Header */}
          <div className="flex items-center justify-between px-6 py-5 border-b border-slate-100 bg-white">
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-8 w-8 text-corpBlue" />
              <span className="text-2xl font-bold text-corpNavy tracking-tight">
                SecureChit
              </span>
            </div>
            <button 
              onClick={() => setIsOpen(false)}
              className="w-10 h-10 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-700 flex items-center justify-center transition-colors"
              aria-label="Close navigation"
            >
              <X className="h-6 w-6 text-slate-800" />
            </button>
          </div>

          {/* Full Screen Menu Body */}
          <div className="flex-1 flex flex-col justify-between px-6 py-8 bg-white overflow-y-auto [ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
            <div className="space-y-4">
              <p className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-2">Navigation Menu</p>
              {navLinks.map((link) => (
                <a 
                  key={link} 
                  href={`#${link.toLowerCase()}`} 
                  className="block text-2xl font-extrabold text-slate-900 hover:text-corpBlue py-3 border-b border-slate-100 transition-colors" 
                  onClick={() => setIsOpen(false)}
                >
                  {link}
                </a>
              ))}
            </div>

            <div className="space-y-4 pt-6 border-t border-slate-100">
              {user ? (
                <Link 
                  to={dashboardPath} 
                  className="block w-full text-center py-4 bg-gradient-to-r from-blue-600 to-corpBlue text-white text-lg font-bold rounded-2xl shadow-lg transition-all flex items-center justify-center gap-2" 
                  onClick={() => setIsOpen(false)}
                >
                  <ArrowLeft className="w-5 h-5" /> Return to {user.role === 'admin' ? 'Admin' : 'Member'} Dashboard
                </Link>
              ) : (
                <Link 
                  to="/login" 
                  className="block w-full text-center py-4 bg-gradient-to-r from-blue-600 to-corpBlue text-white text-lg font-bold rounded-2xl shadow-lg transition-all" 
                  onClick={() => setIsOpen(false)}
                >
                  Login to Account
                </Link>
              )}

              <div className="flex justify-center gap-4 text-xs font-semibold text-slate-400 pt-2">
                <span>🛡️ 256-Bit SSL Secured</span>
                <span>•</span>
                <span>Governed Chit Fund</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
};

const HeroSection = () => {
  const [stats, setStats] = useState({
    activeCustomers: "...",
    successfulPlans: "..."
  });

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/public/stats')
      .then(res => res.json())
      .then(data => {
        setStats({
          activeCustomers: data.active_customers.toString(),
          successfulPlans: data.successful_plans.toString()
        });
      })
      .catch(err => console.error("Failed to fetch public stats", err));
  }, []);

  return (
    <div className="section-gray pt-20 pb-10 sm:pt-28 sm:pb-16 lg:pt-36 lg:pb-16 flex flex-col justify-center min-h-screen" id="home">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
          
          <div className="flex flex-col items-start text-left" data-aos="fade-right" data-aos-duration="1000">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 sm:px-4 sm:py-2 rounded-full bg-cardBg text-corpBlue text-xs sm:text-sm font-semibold mb-6 sm:mb-8 border border-cardBorder shadow-md">
              <span className="flex h-2 w-2 rounded-full bg-corpGold animate-pulse"></span>
              Professional Chit Fund Management
            </div>
            
            <h1 className="text-3xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-corpNavy mb-4 sm:mb-6 tracking-tight leading-tight">
              Secure Chit Fund <br className="hidden sm:block" />
              <span className="text-corpBlue">
                Management System
              </span>
            </h1>
            <p className="mt-2 sm:mt-6 text-base sm:text-xl text-corpTextLight mb-6 leading-relaxed max-w-lg">
              Safe, Transparent and Smart Chit Fund Management built for the modern investor.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 w-full sm:w-auto">
              <Link to="/register" className="btn-primary flex items-center justify-center gap-2 text-base sm:text-lg w-full sm:w-auto">
                Join Now <ArrowRight className="w-5 h-5" />
              </Link>
              <a href="#plans" className="btn-secondary flex items-center justify-center gap-2 text-base sm:text-lg w-full sm:w-auto">
                View Plans
              </a>
            </div>
          </div>

          <div className="relative w-full mt-6 lg:mt-0" data-aos="fade-left" data-aos-duration="1200">
            <div className="relative p-2 bg-cardBg border border-cardBorder rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.06)]">
              <img src="/images/hero.png" alt="Secure Digital Chit Fund" className="rounded-xl object-cover object-center w-full h-[240px] sm:h-[350px] lg:h-[400px]" />
            </div>
          </div>

        </div>
      </div>

      {/* Statistics Section */}
      <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-12 sm:mt-24 relative z-10">
        <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-6">
          {[
            { label: "Active Customers", value: stats.activeCustomers, icon: Users, delay: "0" },
            { label: "Successful Plans", value: stats.successfulPlans, icon: Award, delay: "100" },
            { label: "Satisfaction", value: "99%", icon: Star, delay: "200" },
            { label: "Support", value: "24/7", icon: Clock, delay: "300" }
          ].map((stat, idx) => (
            <div key={idx} data-aos="fade-up" data-aos-delay={stat.delay} className="corp-card p-4 sm:p-6 flex flex-col items-center text-center">
              <div className="w-10 h-10 sm:w-12 sm:h-12 bg-bgAlt2 rounded-full flex items-center justify-center mb-3 sm:mb-4">
                 <stat.icon className="w-5 h-5 sm:w-6 sm:h-6 text-corpBlue" />
              </div>
              <h4 className="text-2xl sm:text-3xl font-bold text-slate-900 mb-1 sm:mb-2">{stat.value}</h4>
              <p className="text-corpTextLight text-xs sm:text-sm uppercase tracking-wider font-semibold">{stat.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

const AboutUsSection = () => {
  const points = [
    { icon: Globe, title: "Trusted Platform", desc: "Recognized digital chit fund platform." },
    { icon: Lock, title: "Secure Tracking", desc: "End-to-end encrypted payment history." },
    { icon: TrendingUp, title: "Transparent Process", desc: "No hidden fees, complete visibility." },
    { icon: HeartHandshake, title: "Customer Friendly", desc: "Dedicated support for all members." }
  ];

  return (
    <section className="bg-transparent py-10 lg:py-12 relative overflow-hidden" id="about">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 items-center">
          
          <div className="relative order-2 lg:order-1" data-aos="fade-right" data-aos-duration="1000">
            <div className="p-2 bg-cardBg border border-cardBorder rounded-[16px] shadow-[0_8px_30px_rgb(0,0,0,0.06)] relative z-10">
               <img src="/images/about.png" alt="Trust and Transparency" className="w-full rounded-xl object-cover object-center h-[400px] animate-float" />
            </div>
          </div>

          <div className="order-1 lg:order-2" data-aos="fade-left" data-aos-duration="1000">
            <h2 className="text-4xl md:text-5xl font-bold text-corpNavy mb-6 tracking-tight">About Us</h2>
            <p className="text-lg text-corpTextLight mb-6 leading-relaxed">Revolutionizing the traditional chit fund industry by bringing it online with complete transparency and top-notch security.</p>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {points.map((point, index) => (
                <div key={index} className="corp-card p-6" data-aos="fade-up" data-aos-delay={index * 100}>
                  <div className="w-12 h-12 bg-bgAlt2 rounded flex items-center justify-center mb-4">
                    <point.icon className="w-6 h-6 text-corpBlue" />
                  </div>
                  <h3 className="text-lg font-bold text-slate-800 mb-2">{point.title}</h3>
                  <p className="text-corpTextLight text-sm leading-relaxed">{point.desc}</p>
                </div>
              ))}
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

const ChitPlans = ({ onJoinPlan, onViewDetails }) => {
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
        const res = await api.get('/api/v1/public/plans');
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
            <span className="text-xs font-extrabold uppercase tracking-widest text-amber-700 bg-amber-50 px-3 py-1 rounded-full border border-amber-200 mb-2 inline-block">
              Auction Chit Schemes ({plans.length} Available)
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
          className="flex flex-row flex-nowrap gap-6 overflow-x-auto snap-x snap-mandatory pb-8 pt-2 px-1 scroll-smooth"
          style={{ display: 'flex', flexDirection: 'row', flexWrap: 'nowrap', overflowX: 'auto', WebkitOverflowScrolling: 'touch', scrollbarWidth: 'thin' }}
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
};

const Features = () => {
  const features = [
    { icon: ShieldCheck, title: "KYC Verification" },
    { icon: Users, title: "Guarantor Management" },
    { icon: CalendarDays, title: "Monthly Tracking" },
    { icon: BellRing, title: "Automated Reminders" },
    { icon: CheckCircle, title: "Eligibility Validation" },
    { icon: BarChart3, title: "Reports & Analytics" }
  ];

  return (
    <section className="bg-transparent py-10 lg:py-12 relative overflow-hidden" id="features">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-6" data-aos="fade-up">
          <h2 className="text-4xl md:text-5xl font-bold text-corpNavy mb-6 tracking-tight">Platform Features</h2>
          <p className="text-lg text-corpTextLight">Everything you need to manage your investments seamlessly.</p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {features.map((feature, index) => (
            <div key={index} data-aos="fade-up" data-aos-delay={index * 100} className="corp-card p-8 flex flex-col items-start">
              <div className="w-14 h-14 bg-corpBlue border border-transparent rounded flex items-center justify-center mb-6 shadow-sm">
                <feature.icon className="w-7 h-7 text-white" />
              </div>
              <h3 className="text-xl font-bold text-slate-800 mb-3 tracking-wide">{feature.title}</h3>
              <p className="text-corpTextLight leading-relaxed text-sm">Advanced tools to ensure security and transparency for every transaction.</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

const Rules = () => {
  const rules = [
    "Monthly installment must be paid before the 10th.",
    "Reminder notifications will be sent until the 15th.",
    "KYC verification is mandatory.",
    "Guarantor details are mandatory.",
    "Minimum 6 installments required for eligibility.",
    "Admin verification required.",
    "False information may result in account suspension."
  ];

  return (
    <section className="section-gray" id="rules">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 items-center">
          
          <div data-aos="fade-right" data-aos-duration="1000">
            <h2 className="text-4xl md:text-5xl font-bold text-corpNavy mb-6 tracking-tight">Important Rules</h2>
            <p className="text-lg text-corpTextLight mb-6">Please read our terms carefully to ensure a smooth experience.</p>
            
            <div className="corp-card p-8">
              <ul className="space-y-6">
                {rules.map((rule, idx) => (
                  <li key={idx} className="flex items-start gap-4">
                    <CheckCircle2 className="w-6 h-6 text-corpBlue flex-shrink-0 mt-0.5" />
                    <span className="text-slate-800 text-base md:text-lg leading-relaxed">{rule}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="relative hidden lg:block" data-aos="fade-left" data-aos-duration="1000">
            <div className="p-2 bg-cardBg border border-cardBorder rounded-[16px] shadow-[0_8px_30px_rgb(0,0,0,0.06)] relative z-10">
               <img src="/images/rules.png" alt="Corporate Compliance" className="w-full rounded-xl object-cover object-center h-[400px] animate-float" />
            </div>
          </div>

        </div>
      </div>
    </section>
  );
};

const Testimonials = () => {
  const reviews = [
    { name: "Rahul Sharma", role: "Investor", text: "SecureChit completely changed how I manage my savings. It is incredibly transparent and easy to track.", rating: 5, avatar: "https://api.dicebear.com/7.x/notionists/svg?seed=Rahul&backgroundColor=e2e8f0" },
    { name: "Priya Desai", role: "Business Owner", text: "The automated reminders and digital KYC made everything so smooth. Highly recommend for safe investments.", rating: 5, avatar: "https://api.dicebear.com/7.x/notionists/svg?seed=Priya&backgroundColor=e2e8f0" },
    { name: "Amit Kumar", role: "Freelancer", text: "Customer service is top notch. The app layout is clean and I always know exactly where my money is.", rating: 5, avatar: "https://api.dicebear.com/7.x/notionists/svg?seed=Amit&backgroundColor=e2e8f0" }
  ];

  return (
    <section className="bg-transparent py-10 lg:py-12 relative overflow-hidden" id="testimonials">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-6" data-aos="fade-up">
          <h2 className="text-4xl md:text-5xl font-bold text-corpNavy mb-6 tracking-tight">Customer Reviews</h2>
          <p className="text-lg text-corpTextLight">Hear from our satisfied members.</p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {reviews.map((review, idx) => (
            <div key={idx} data-aos="fade-up" data-aos-delay={idx * 150} className="corp-card p-8 flex flex-col">
              <div className="flex gap-1 mb-6">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} className={`w-5 h-5 ${i < review.rating ? 'text-corpBlue fill-corpGold' : 'text-gray-200'}`} />
                ))}
              </div>
              <p className="text-corpTextLight italic mb-8 leading-relaxed flex-grow">"{review.text}"</p>
              
              <div className="flex items-center gap-4 pt-6 border-t border-gray-100">
                <div className="w-14 h-14 rounded-full overflow-hidden bg-bgAlt2 border border-cardBorder">
                    <img src={review.avatar} alt={review.name} className="w-full h-full object-cover" />
                </div>
                <div>
                  <h4 className="font-bold text-base text-slate-800 tracking-wide">{review.name}</h4>
                  <p className="text-corpTextLight text-sm">{review.role}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

const Contact = () => {
  return (
    <section className="section-gray" id="contact">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 items-center">
          
          <div data-aos="fade-right" data-aos-duration="1000">
            <h2 className="text-4xl md:text-5xl font-bold text-corpNavy mb-6 tracking-tight">Get in Touch</h2>
            <p className="text-lg text-corpTextLight mb-12 leading-relaxed">Our professional support team is available 24/7. Reach out to us through any of the channels below.</p>
            
            <div className="space-y-6">
              <div className="corp-card p-6 flex items-center gap-6">
                <div className="w-14 h-14 bg-corpBlue rounded border border-transparent flex items-center justify-center shadow-sm">
                   <Phone className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-lg mb-1 text-slate-800 tracking-wide">Phone</h3>
                  <a href="tel:+919489771511" className="text-corpTextLight hover:text-corpBlue transition-colors font-medium">+91 94897 71511</a>
                </div>
              </div>
              
              <div className="corp-card p-6 flex items-center gap-6">
                <div className="w-14 h-14 bg-corpBlue rounded border border-transparent flex items-center justify-center shadow-sm">
                   <Mail className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-lg mb-1 text-slate-800 tracking-wide">Email</h3>
                  <a href="mailto:naresk1213@gmail.com" className="text-corpTextLight hover:text-corpBlue transition-colors font-medium">naresk1213@gmail.com</a>
                </div>
              </div>
              
              <div className="corp-card p-6 flex items-center gap-6">
                <div className="w-14 h-14 bg-corpBlue rounded border border-transparent flex items-center justify-center shadow-sm">
                   <MapPin className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-lg mb-1 text-slate-800 tracking-wide">Office</h3>
                  <p className="text-corpTextLight">123 Financial District, Tech City</p>
                </div>
              </div>
            </div>
          </div>

          <div className="relative hidden lg:block" data-aos="fade-left" data-aos-duration="1200">
             <div className="p-2 bg-cardBg border border-cardBorder rounded-[16px] shadow-[0_8px_30px_rgb(0,0,0,0.06)] relative z-10">
                 <img src="/images/contact.png" alt="Customer Support" className="w-full rounded-xl object-cover object-center h-[400px] animate-float" />
             </div>
          </div>

        </div>
      </div>
    </section>
  );
};

const Footer = () => (
  <footer className="bg-corpNavy text-slate-400 py-16 border-t border-cardBorder">
    <div className="max-w-7xl mx-auto px-4 flex flex-col items-center">
      <div className="flex justify-center items-center gap-3 mb-8">
        <ShieldCheck className="h-10 w-10 text-corpGold" />
        <span className="text-3xl font-bold tracking-tight text-corpGold">
          SecureChit
        </span>
      </div>
      <p className="mb-6 text-lg max-w-md text-center font-light leading-relaxed text-slate-400">Empowering your financial journey with trust, transparency, and modern security.</p>
      
      <div className="flex gap-6 mb-12">
        <a href="#" className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center hover:bg-corpBlue hover:text-white transition-all border border-slate-700 hover:border-corpBlue"><Twitter className="w-5 h-5" /></a>
        <a href="#" className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center hover:bg-corpBlue hover:text-white transition-all border border-slate-700 hover:border-corpBlue"><Linkedin className="w-5 h-5" /></a>
        <a href="#" className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center hover:bg-corpBlue hover:text-white transition-all border border-slate-700 hover:border-corpBlue"><Github className="w-5 h-5" /></a>
      </div>

      <div className="w-full border-t border-cardBorder pt-8 text-center flex flex-col md:flex-row justify-between items-center text-base md:text-lg text-slate-400 font-medium">
        <p className="text-sm md:text-base text-slate-500">&copy; {new Date().getFullYear()} Secure Chit Fund Management System. All rights reserved.</p>
        <div className="flex gap-4 mt-6 md:mt-0">
          <Link to="/admin/login" className="hover:text-white transition-colors text-corpGold font-bold">Admin Portal</Link>
          <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
          <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
        </div>
      </div>
    </div>
  </footer>
);

const PlanDetailsModal = ({ plan, onClose, onJoin }) => {
  const N = plan.totalMembers || plan.duration || 12;
  const duration = plan.duration || plan.durationMonths || N;
  const monthly = plan.monthlyAmount || 0;
  const commissionRate = (plan.commissionRate || 5) / 100;
  const chitValue = monthly * N;            // Total pool per month
  const commissionPerMonth = chitValue * commissionRate;
  const totalCommission = commissionPerMonth * duration;

  // Bid % decreases linearly: 20% (month 1) -> 5% (last month)
  const getBidPct = (month) => {
    if (duration === 1) return 0.20;
    const maxBid = 0.20, minBid = 0.05;
    return maxBid - ((maxBid - minBid) / (duration - 1)) * (month - 1);
  };

  const isAuction = plan.chitType === 'auction' || plan.chit_type === 'auction';

  // Calculate real auction month-by-month schedule
  const monthlyData = Array.from({ length: duration }, (_, i) => {
    const month = i + 1;
    if (month === 1) {
      // Month 1: Foreman Company
      return {
        month: 1,
        winnerPrize: chitValue,
        discount: 0,
        commission: 0,
        dividend: 0,
        netPay: monthly,
        winnerName: 'COMPANY (Foreman)'
      };
    } else if (month === duration) {
      // Month N: Last Member
      return {
        month,
        winnerPrize: chitValue,
        discount: 0,
        commission: 0,
        dividend: 0,
        netPay: monthly,
        winnerName: 'Last Member'
      };
    } else {
      // Month 2 to Month N-1: Auction bidding
      // Winning bid scales from 70% to 98% of chit value
      const bidRatio = 0.70 + (month - 2) * (0.28 / Math.max(1, duration - 2));
      const winningBid = Math.round(chitValue * bidRatio);
      const disc = chitValue - winningBid;
      const comm = Math.round(disc * (commissionRate || 0.05));
      const netDisc = Math.max(0, disc - comm);
      const div = Math.round((netDisc / N) * 100) / 100;
      const netPay = Math.round((monthly - div) * 100) / 100;
      return {
        month,
        winnerPrize: winningBid,
        discount: disc,
        commission: comm,
        dividend: div,
        netPay,
        winnerName: 'Auction Winner'
      };
    }
  });

  const totalPaidByMember = Math.round(monthlyData.reduce((sum, item) => sum + item.netPay, 0));
  const PlanIcon = plan.icon || Shield;

  if (!monthly || monthly <= 0) return null; // guard against bad data

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 font-sans">
      <div className="bg-white rounded-3xl w-full max-w-3xl overflow-hidden shadow-2xl border border-slate-100 flex flex-col max-h-[92vh]">
        
        {/* Header */}
        <div className="px-8 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-900 text-white">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center border border-white/20">
              <PlanIcon className="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <h2 className="text-xl font-bold">{plan.name} Schedule & Calculations</h2>
              <span className="px-2 py-0.5 rounded text-[10px] font-extrabold bg-amber-500 text-slate-950 uppercase tracking-wider">
                {isAuction ? 'Auction Scheme (Discount + Dividend)' : 'Lucky Draw Scheme'}
              </span>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-3xl font-light">&times;</button>
        </div>

        {/* Content */}
        <div className="p-6 overflow-y-auto flex-grow space-y-6 text-slate-700 text-xs">
          
          {/* Key Metrics */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-slate-50 rounded-2xl p-3.5 border border-slate-200 text-center">
              <span className="text-[11px] text-slate-400 block mb-0.5">Gross Monthly Dues</span>
              <strong className="text-base font-extrabold text-slate-900">₹{monthly.toLocaleString()}</strong>
            </div>
            <div className="bg-slate-50 rounded-2xl p-3.5 border border-slate-200 text-center">
              <span className="text-[11px] text-slate-400 block mb-0.5">Total Chit Value</span>
              <strong className="text-base font-extrabold text-corpBlue">₹{chitValue.toLocaleString()}</strong>
            </div>
            <div className="bg-slate-50 rounded-2xl p-3.5 border border-slate-200 text-center">
              <span className="text-[11px] text-slate-400 block mb-0.5">Duration & Members</span>
              <strong className="text-base font-extrabold text-slate-900">{duration} Months / {N} Members</strong>
            </div>
            <div className="bg-emerald-50 rounded-2xl p-3.5 border border-emerald-200 text-center">
              <span className="text-[11px] text-emerald-700 font-bold block mb-0.5">Est. Total Paid / Member</span>
              <strong className="text-base font-extrabold text-emerald-800">₹{totalPaidByMember.toLocaleString()}</strong>
            </div>
          </div>

          {/* Month-by-Month Schedule Table */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="font-bold text-sm text-slate-900">Month-by-Month Auction Schedule & Net Dues Table</h3>
              <span className="text-[10px] font-bold bg-blue-50 text-corpBlue px-2.5 py-1 rounded-full border border-blue-200">
                5% Foreman Commission Applied
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mb-3">
              Early bidders bid higher discounts (receiving lower prize money early, but giving higher dividends to everyone). Late bidders receive full prize money.
            </p>

            <div className="border border-slate-200 rounded-2xl overflow-hidden shadow-sm bg-white">
              <div className="max-h-72 overflow-y-auto">
                <table className="w-full text-left border-collapse text-xs">
                  <thead className="sticky top-0 z-10 bg-slate-100 text-slate-700 font-bold border-b border-slate-200 uppercase tracking-wider text-[10px]">
                    <tr>
                      <th className="px-4 py-3">Month</th>
                      <th className="px-4 py-3 text-emerald-700">🏆 Winner Payout</th>
                      <th className="px-4 py-3 text-amber-700">🏷️ Discount</th>
                      <th className="px-4 py-3 text-blue-700">💰 Dividend / Member</th>
                      <th className="px-4 py-3 text-indigo-900 text-right">💳 Net Payable</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100 font-medium text-slate-800">
                    {monthlyData.map((m) => (
                      <tr key={m.month} className={`hover:bg-blue-50/50 transition-colors ${m.month === 1 ? 'bg-amber-50/40 font-bold' : ''}`}>
                        <td className="px-4 py-2.5 font-bold">
                          Month {m.month}
                          {m.month === 1 && <span className="ml-1.5 text-[9px] bg-amber-200 text-amber-900 px-1.5 py-0.2 rounded font-extrabold">COMPANY</span>}
                          {m.month === duration && <span className="ml-1.5 text-[9px] bg-emerald-200 text-emerald-900 px-1.5 py-0.2 rounded font-extrabold">LAST</span>}
                        </td>
                        <td className="px-4 py-2.5 font-bold text-emerald-700">
                          ₹{m.winnerPrize.toLocaleString()}
                        </td>
                        <td className="px-4 py-2.5 text-amber-700 font-semibold">
                          ₹{m.discount.toLocaleString()}
                        </td>
                        <td className="px-4 py-2.5 text-blue-700 font-bold">
                          +₹{m.dividend.toLocaleString()}
                        </td>
                        <td className="px-4 py-2.5 text-right font-extrabold text-indigo-900 text-sm">
                          ₹{m.netPay.toLocaleString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            <div className="mt-3 bg-blue-50 border border-blue-200 rounded-xl p-3.5 text-xs text-blue-900 flex items-center justify-between">
              <div>
                <strong className="block font-bold">🧮 How Net Payable is Calculated:</strong>
                <span>Gross Monthly Dues (₹{monthly.toLocaleString()}) - Member Dividend = <strong>Net Payable</strong></span>
              </div>
            </div>
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

const JoinPlanModal = ({ plan, onClose, onBackToDetails }) => {
  const [step, setStep] = useState(0); // Start at Step 0: Account Check
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    username: '',
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: '',
    
    // Guarantor
    g_name: '',
    g_phone: '',
    g_address: '',
    g_relationship: ''
  });

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
    setError('');
  };

  const handleNext = () => {
    if (step === 1) {
      if (!formData.username || !formData.name || !formData.email || !formData.phone || !formData.password) {
        setError('Please fill in all account details.');
        return;
      }
      if (formData.password !== formData.confirmPassword) {
        setError('Passwords do not match.');
        return;
      }
      if (formData.phone.length !== 10 || !/^\d+$/.test(formData.phone)) {
        setError('Phone Number must be exactly 10 digits.');
        return;
      }
    }
    setStep(step + 1);
  };

  const handleBack = () => {
    setStep(step - 1);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.g_name || !formData.g_phone || !formData.g_address || !formData.g_relationship) {
      setError('Please fill in all guarantor details.');
      return;
    }
    if (formData.g_phone.length !== 10 || !/^\d+$/.test(formData.g_phone)) {
      setError('Guarantor phone must be 10 digits.');
      return;
    }

    setLoading(true);
    try {
      await api.post('/api/v1/auth/register', {
        username: formData.username,
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        password: formData.password,
        aadhar_number: null
      });
      setStep(3);
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-3xl w-full max-w-xl overflow-hidden shadow-2xl border border-slate-100 flex flex-col max-h-[90vh]">
        <div className="px-8 py-5 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div className="flex items-center gap-3">
            {step > 0 && step < 3 && (
              <button 
                onClick={handleBack} 
                className="w-8 h-8 rounded-full border border-slate-200 hover:border-slate-350 hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center transition-colors"
                title="Go Back"
              >
                <ArrowLeft className="w-4 h-4" />
              </button>
            )}
            <div>
              <h2 className="text-xl font-bold text-slate-900">Join Plan: {plan?.name}</h2>
              <p className="text-xs text-slate-500 mt-0.5">Monthly Installment: ₹{plan?.monthlyAmount}</p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 text-2xl font-semibold">&times;</button>
        </div>

        {/* Step Indicator */}
        {step > 0 && (
          <div className="flex justify-between items-center px-8 py-4 bg-slate-50/50 border-b border-slate-100 text-xs font-semibold text-slate-400">
            <div className={`flex items-center gap-2 ${step >= 1 ? 'text-corpBlue' : ''}`}>
              <span className={`w-5 h-5 rounded-full flex items-center justify-center border ${step >= 1 ? 'border-corpBlue bg-blue-50' : 'border-slate-300'}`}>1</span>
              <span>Account Details</span>
            </div>
            <div className="w-12 h-0.5 bg-slate-200"></div>
            <div className={`flex items-center gap-2 ${step >= 2 ? 'text-corpBlue' : ''}`}>
              <span className={`w-5 h-5 rounded-full flex items-center justify-center border ${step >= 2 ? 'border-corpBlue bg-blue-50' : 'border-slate-300'}`}>2</span>
              <span>Guarantor Info</span>
            </div>
            <div className="w-12 h-0.5 bg-slate-200"></div>
            <div className={`flex items-center gap-2 ${step >= 3 ? 'text-corpBlue' : ''}`}>
              <span className={`w-5 h-5 rounded-full flex items-center justify-center border ${step >= 3 ? 'border-corpBlue bg-blue-50' : 'border-slate-300'}`}>3</span>
              <span>Success</span>
            </div>
          </div>
        )}

        <div className="p-8 overflow-y-auto flex-grow text-slate-700">
          {error && (
            <div className="bg-red-50 text-red-600 px-4 py-3 rounded-xl text-sm mb-6 flex items-center gap-2 border border-red-100">
              <p className="font-medium">⚠️ {error}</p>
            </div>
          )}

          {step === 0 && (
            <div className="text-center py-6 space-y-6">
              <div className="w-16 h-16 rounded-full bg-blue-50 border border-blue-100 flex items-center justify-center mx-auto text-corpBlue">
                <span className="text-3xl font-bold">👤</span>
              </div>
              <div>
                <h3 className="text-xl font-bold text-slate-900">Do you have a SecureChit Account?</h3>
                <p className="text-slate-500 text-sm mt-2 max-w-sm mx-auto">Please let us know if you already have an account with us to proceed correctly.</p>
              </div>
              <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
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
              </div>
            </div>
          )}

          {step === 1 && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Full Name</label>
                  <input type="text" name="name" value={formData.name} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Ramesh Kumar" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Username</label>
                  <input type="text" name="username" value={formData.username} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="ramesh123" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Email Address</label>
                  <input type="email" name="email" value={formData.email} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="name@email.com" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Phone Number</label>
                  <input type="text" name="phone" value={formData.phone} onChange={handleInputChange} maxLength="10" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="10-digit number" />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Password</label>
                  <input type="password" name="password" value={formData.password} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Min 8 chars" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Confirm Password</label>
                  <input type="password" name="confirmPassword" value={formData.confirmPassword} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Repeat password" />
                </div>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Guarantor Name</label>
                  <input type="text" name="g_name" value={formData.g_name} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Guarantor Full Name" />
                </div>
                <div>
                  <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Guarantor Phone</label>
                  <input type="text" name="g_phone" value={formData.g_phone} onChange={handleInputChange} maxLength="10" required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="10-digit number" />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Relationship</label>
                <input type="text" name="g_relationship" value={formData.g_relationship} onChange={handleInputChange} required className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="e.g. Father, Friend" />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-600 mb-1 uppercase tracking-wider">Guarantor Address</label>
                <textarea name="g_address" value={formData.g_address} onChange={handleInputChange} required rows="3" className="w-full px-4 py-2.5 border border-slate-200 rounded-xl focus:border-blue-500 focus:outline-none" placeholder="Full residential address of guarantor"></textarea>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="text-center py-6">
              <div className="w-20 h-20 rounded-full bg-emerald-50 border border-emerald-200 flex items-center justify-center mx-auto mb-6 text-emerald-500">
                <span className="text-3xl font-bold">✓</span>
              </div>
              <h3 className="text-2xl font-bold text-slate-900 mb-2">Onboarding Successful!</h3>
              <p className="text-slate-500 text-sm max-w-sm mx-auto leading-relaxed">
                Your application to join the <strong>{plan?.name}</strong> has been submitted. Admin will review and approve your account shortly. 
              </p>
              <p className="text-slate-400 text-xs max-w-xs mx-auto mt-4 leading-relaxed">
                Once approved, you can login to upload your official KYC documents.
              </p>
            </div>
          )}
        </div>

        {step > 0 && step < 3 && (
          <div className="px-8 py-4 border-t border-slate-100 bg-slate-50 flex justify-end items-center">
            {step === 1 ? (
              <button onClick={handleNext} className="px-6 py-2.5 bg-corpBlue text-white font-semibold rounded-xl text-sm hover:bg-corpNavy transition-colors shadow-md">Continue</button>
            ) : (
              <button onClick={handleSubmit} disabled={loading} className="px-6 py-2.5 bg-emerald-600 text-white font-semibold rounded-xl text-sm hover:bg-emerald-700 transition-colors disabled:opacity-50 shadow-md">
                {loading ? 'Submitting...' : 'Submit Application'}
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};



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

      {isModalOpen && <JoinPlanModal plan={selectedPlan} onClose={() => setIsModalOpen(false)} onBackToDetails={() => { setIsModalOpen(false); setIsDetailsOpen(true); }} />}
      {isDetailsOpen && <PlanDetailsModal plan={selectedPlan} onClose={() => setIsDetailsOpen(false)} onJoin={handleJoinPlan} />}
    </div>
  );
};


const ScrollToTop = () => {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);
  return null;
};

function App() {
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    AOS.init({
      once: true,
      offset: 50,
      duration: 800,
      easing: 'ease-out-cubic',
    });
  }, []);

  return (
    <>
      <ScrollToTop />
      <Routes>
        <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/admin/login" element={<AdminLogin />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/member/dashboard" element={
        <ProtectedRoute>
          <MemberLayout><MemberDashboard /></MemberLayout>
        </ProtectedRoute>
      } />
      <Route path="/member/kyc" element={
        <ProtectedRoute>
          <MemberLayout><KYCUpload /></MemberLayout>
        </ProtectedRoute>
      } />
      <Route path="/member/guarantor" element={
        <ProtectedRoute>
          <MemberLayout><GuarantorForm /></MemberLayout>
        </ProtectedRoute>
      } />
      <Route path="/admin/dashboard" element={
        <RoleRoute role="admin">
          <AdminLayout><AdminDashboard /></AdminLayout>
        </RoleRoute>
      } />
      <Route path="/admin/members" element={
        <RoleRoute role="admin">
          <AdminLayout><MembersList /></AdminLayout>
        </RoleRoute>
      } />
      <Route path="/admin/members/:id" element={
        <RoleRoute role="admin">
          <AdminLayout><MemberDetails /></AdminLayout>
        </RoleRoute>
      } />
      <Route path="/admin/plans" element={
        <RoleRoute role="admin">
          <AdminLayout><ManagePlans /></AdminLayout>
        </RoleRoute>
      } />
      <Route path="/admin/plans/:id/members" element={
        <RoleRoute role="admin">
          <AdminLayout><PlanMembers /></AdminLayout>
        </RoleRoute>
      } />
      <Route path="/admin/plans/:id/draws" element={
        <RoleRoute role="admin">
          <AdminLayout><ConductDraw /></AdminLayout>
        </RoleRoute>
      } />
      <Route path="/member/plans" element={
        <ProtectedRoute>
          <MemberLayout><ExplorePlans /></MemberLayout>
        </ProtectedRoute>
      } />
      <Route path="/member/payments" element={
        <ProtectedRoute>
          <MemberLayout><MemberPayments /></MemberLayout>
        </ProtectedRoute>
      } />
      <Route path="/admin/payments" element={
        <RoleRoute role="admin">
          <AdminLayout><AdminPayments /></AdminLayout>
        </RoleRoute>
      } />
      <Route path="/admin/pronotes" element={
        <RoleRoute role="admin">
          <AdminLayout><PronoteManagement /></AdminLayout>
        </RoleRoute>
      } />
    </Routes>
    </>
  );
}

export default App;

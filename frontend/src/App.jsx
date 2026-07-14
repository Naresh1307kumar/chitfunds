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
import { ProtectedRoute, RoleRoute } from './components/ProtectedRoute';
import AOS from 'aos';
import 'aos/dist/aos.css';
import { 
  ShieldCheck, Menu, X, ArrowRight, ArrowLeft, Users, CalendarDays, 
  BellRing, BarChart3, CheckCircle2, Phone, Mail, MapPin,
  Star, Lock, TrendingUp, HeartHandshake, Zap, Crown, Shield,
  Globe, Clock, Award, ChevronRight, CheckCircle, Github, Twitter, Linkedin
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
  const navLinks = ['Home', 'Plans', 'Features', 'Rules', 'Contact'];

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed w-full z-50 top-0 transition-all duration-300 ${scrolled ? 'bg-white/95 backdrop-blur-md py-4 shadow-md border-b border-slate-200/60' : 'bg-transparent py-6 border-b border-transparent'}`}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <div className="flex items-center gap-2" data-aos="fade-right">
            <ShieldCheck className="h-8 w-8 text-corpBlue" />
            <span className="text-2xl font-bold text-corpNavy tracking-tight">
              SecureChit
            </span>
          </div>
          <div className="hidden md:flex items-center space-x-10" data-aos="fade-down">
            {navLinks.map((link) => (
              <a key={link} href={`#${link.toLowerCase()}`} className="text-corpTextLight hover:text-corpBlue transition-colors text-lg font-bold tracking-wide">
                {link}
              </a>
            ))}
            <Link to="/login" className="btn-primary py-3 px-8 text-base font-bold inline-block text-center shadow-lg">
              Login
            </Link>
          </div>
          <div className="md:hidden flex items-center">
            <button onClick={() => setIsOpen(!isOpen)} className="text-slate-600 hover:text-corpBlue">
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>
      {isOpen && (
        <div className="md:hidden bg-white mt-4 border-t border-slate-200 shadow-xl absolute w-full">
          <div className="px-4 py-4 space-y-2">
            {navLinks.map((link) => (
              <a key={link} href={`#${link.toLowerCase()}`} className="block px-4 py-3 text-base font-medium text-slate-600 hover:text-corpBlue hover:bg-slate-800 rounded-md transition-colors" onClick={() => setIsOpen(false)}>
                {link}
              </a>
            ))}
            <Link to="/login" className="block w-full text-center mt-6 py-3 btn-primary text-white">
              Login
            </Link>
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
    <div className="section-gray pt-24 pb-12 lg:pt-36 lg:pb-16 flex flex-col justify-center min-h-screen" id="home">
      <div className="max-w-7xl mx-auto px-4 relative z-10 w-full">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-center">
          
          <div className="flex flex-col items-start text-left" data-aos="fade-right" data-aos-duration="1000">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-cardBg text-corpBlue text-sm font-semibold mb-8 border border-cardBorder shadow-md">
              <span className="flex h-2 w-2 rounded-full bg-corpGold"></span>
              Professional Financial Management
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold text-corpNavy mb-6 tracking-tight leading-tight">
              Secure Chit Fund <br className="hidden md:block" />
              <span className="text-corpBlue">
                Management System
              </span>
            </h1>
            <p className="mt-6 text-xl text-corpTextLight mb-6 leading-relaxed max-w-lg">
              Safe, Transparent and Smart Chit Fund Management built for the modern investor.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
              <button className="btn-primary flex items-center justify-center gap-2 text-lg" onClick={() => alert('Join functionality disabled.')}>
                Join Now <ArrowRight className="w-5 h-5" />
              </button>
              <a href="#plans" className="btn-secondary flex items-center justify-center gap-2 text-lg">
                View Plans
              </a>
            </div>
          </div>

          <div className="relative hidden lg:block" data-aos="fade-left" data-aos-duration="1200">
            <div className="relative p-2 bg-cardBg border border-cardBorder rounded-[16px] shadow-[0_8px_30px_rgb(0,0,0,0.06)]">
              <img src="/images/hero.png" alt="Secure Digital Chit Fund" className="rounded-xl object-cover object-center w-full h-[400px]" />
            </div>
          </div>

        </div>
      </div>

      {/* Statistics Section */}
      <div className="w-full max-w-7xl mx-auto px-4 mt-24 relative z-10">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {[
            { label: "Active Customers", value: stats.activeCustomers, icon: Users, delay: "0" },
            { label: "Successful Plans", value: stats.successfulPlans, icon: Award, delay: "100" },
            { label: "Satisfaction", value: "99%", icon: Star, delay: "200" },
            { label: "Support", value: "24/7", icon: Clock, delay: "300" }
          ].map((stat, idx) => (
            <div key={idx} data-aos="fade-up" data-aos-delay={stat.delay} className="corp-card p-6 flex flex-col items-center text-center">
              <div className="w-12 h-12 bg-bgAlt2 rounded-full flex items-center justify-center mb-4">
                 <stat.icon className="w-6 h-6 text-corpBlue" />
              </div>
              <h4 className="text-3xl font-bold text-slate-900 mb-2">{stat.value}</h4>
              <p className="text-corpTextLight text-sm uppercase tracking-wider font-semibold">{stat.label}</p>
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

  useEffect(() => {
    const fetchPublicPlans = async () => {
      try {
        const res = await api.get('/api/v1/public/plans');
        // Map backend schema to frontend expectations
        const mappedPlans = res.data.map(p => {
          let IconComp = Shield;
          let badgeText = "Bronze";
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
            <div key={index} data-aos="fade-up" data-aos-delay={index * 150} className={plan.popular ? 'plan-card-popular shadow-lg hover:shadow-xl transition-shadow' : 'plan-card hover:shadow-md transition-shadow'}>
              
              {plan.popular && (
                <div className="bg-corpGold text-white text-center py-2 text-sm font-bold uppercase tracking-wider">
                  Most Popular
                </div>
              )}

              <div className="p-8 border-b border-gray-100">
                <div className="flex justify-between items-start mb-6">
                  <div className="w-12 h-12 rounded bg-bgAlt2 flex items-center justify-center border border-cardBorder">
                    {(() => { const PlanIcon = plan.icon || Shield; return <PlanIcon className="w-6 h-6 text-corpBlue" />; })()}
                  </div>
                  {!plan.popular && (
                    <span className="px-3 py-1 rounded text-xs font-bold uppercase tracking-wider bg-bgAlt2 text-corpTextLight border border-cardBorder">
                      {plan.badge}
                    </span>
                  )}
                </div>

                <h3 className="text-2xl font-bold text-slate-800 mb-2">{plan.name}</h3>
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
                  <p className="text-corpTextLight">+91 1800 123 4567</p>
                </div>
              </div>
              
              <div className="corp-card p-6 flex items-center gap-6">
                <div className="w-14 h-14 bg-corpBlue rounded border border-transparent flex items-center justify-center shadow-sm">
                   <Mail className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h3 className="font-bold text-lg mb-1 text-slate-800 tracking-wide">Email</h3>
                  <p className="text-corpTextLight">support@securechit.com</p>
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

  // Pre-calculate monthly data to get actual total paid including dividends
  const monthlyData = Array.from({ length: duration }, (_, i) => {
    const month = i + 1;
    const bidPct = getBidPct(month);
    const bidAmount = chitValue * bidPct;
    const dividend = Math.max(0, (bidAmount - commissionPerMonth) / N);
    const netPay = monthly - dividend;
    return { month, bidPct, winnerPrize: chitValue - bidAmount, dividend, netPay };
  });

  const totalPaidByMember = monthlyData.reduce((sum, item) => sum + item.netPay, 0);

  // Per-month dynamic calculation
  const projections = monthlyData.map(item => {
    const winnerNetInterest = totalPaidByMember - item.winnerPrize; // positive = interest cost
    return {
      month: item.month,
      bidPct: Math.round(item.bidPct * 100),
      winnerPrize: Math.round(item.winnerPrize),
      winnerNetInterest: Math.round(winnerNetInterest),
      dividend: Math.round(item.dividend),
      netPay: Math.round(item.netPay),
    };
  });

  const netPrize = chitValue - commissionPerMonth;
  const commission = commissionPerMonth;
  const totalValue = chitValue;

  // Safe icon render - plan.icon may be undefined when coming from API
  const PlanIcon = plan.icon || Shield;

  if (!monthly || monthly <= 0) return null; // guard against bad data

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
      <div className="bg-white rounded-3xl w-full max-w-2xl overflow-hidden shadow-2xl border border-slate-100 flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="px-8 py-6 border-b border-slate-100 flex justify-between items-center bg-slate-50">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center border border-blue-100">
              <PlanIcon className="w-6 h-6 text-corpBlue" />
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

          {/* Month-by-Month Breakdown Table */}
          <div>
            <h3 className="font-bold text-base text-slate-900 mb-1">Month-by-Month Prize Breakdown</h3>
            <p className="text-xs text-slate-400 mb-3">
              See how much the winner receives and how much interest they pay, depending on which month they win the draw.
            </p>
            <div className="border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
              <div className="max-h-72 overflow-y-auto">
                <table className="w-full text-left border-collapse">
                  <thead className="sticky top-0 z-10">
                    <tr className="bg-slate-50 border-b border-slate-200 text-xs font-bold uppercase tracking-wider text-slate-500">
                      <th className="px-5 py-3">Month</th>
                      <th className="px-5 py-3 text-blue-600">Winner Payout (Prize Amount)</th>
                      <th className="px-5 py-3 text-red-500">Interest Cost to Pay</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-100">
                    {projections.map((p) => (
                      <tr key={p.month} className="hover:bg-blue-50/30 transition-colors">
                        <td className="px-5 py-3 font-semibold text-slate-700">
                          Month {p.month}
                          {p.month === duration && (
                            <span className="ml-2 text-[10px] bg-emerald-100 text-emerald-700 px-1.5 py-0.5 rounded-full font-bold">Last</span>
                          )}
                        </td>
                        <td className="px-5 py-3 font-bold text-blue-700 text-base">
                          ₹{p.winnerPrize.toLocaleString()}
                        </td>
                        <td className="px-5 py-3">
                          {p.winnerNetInterest > 0 ? (
                            <span className="text-red-500 font-semibold">₹{p.winnerNetInterest.toLocaleString()}</span>
                          ) : (
                            <span className="text-emerald-600 font-semibold">₹0 (No interest!)</span>
                          )}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            <div className="mt-3 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 text-xs text-amber-800">
              💡 <strong>Note:</strong> Early month winners receive a lower prize and pay more interest. Late month winners receive a higher prize and pay less interest.
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
          <MemberDashboard />
        </ProtectedRoute>
      } />
      <Route path="/member/kyc" element={
        <ProtectedRoute>
          <KYCUpload />
        </ProtectedRoute>
      } />
      <Route path="/member/guarantor" element={
        <ProtectedRoute>
          <GuarantorForm />
        </ProtectedRoute>
      } />
      <Route path="/admin/dashboard" element={
        <RoleRoute role="admin">
          <AdminDashboard />
        </RoleRoute>
      } />
      <Route path="/admin/members" element={
        <RoleRoute role="admin">
          <MembersList />
        </RoleRoute>
      } />
      <Route path="/admin/members/:id" element={
        <RoleRoute role="admin">
          <MemberDetails />
        </RoleRoute>
      } />
      <Route path="/admin/plans" element={
        <RoleRoute role="admin">
          <ManagePlans />
        </RoleRoute>
      } />
      <Route path="/admin/plans/:id/members" element={
        <RoleRoute role="admin">
          <PlanMembers />
        </RoleRoute>
      } />
      <Route path="/admin/plans/:id/draws" element={
        <RoleRoute role="admin">
          <ConductDraw />
        </RoleRoute>
      } />
      <Route path="/member/plans" element={
        <ProtectedRoute>
          <ExplorePlans />
        </ProtectedRoute>
      } />
      <Route path="/member/payments" element={
        <ProtectedRoute>
          <MemberPayments />
        </ProtectedRoute>
      } />
      <Route path="/admin/payments" element={
        <RoleRoute role="admin">
          <AdminPayments />
        </RoleRoute>
      } />
    </Routes>
    </>
  );
}

export default App;

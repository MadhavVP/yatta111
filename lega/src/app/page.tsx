"use client";

import React, { useState, useEffect, Suspense } from "react";
import { ArrowRight, MapPin, Briefcase, Sparkles } from "lucide-react";
import { useRouter, useSearchParams } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";

function LandingContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const isEditing = searchParams.get("edit") === "true";

  const [sector, setSector] = useState("Healthcare");
  const [region, setRegion] = useState("Indiana");
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    setIsLoaded(true);
    // If user already has settings and NOT in edit mode, redirect to feed
    if (!isEditing) {
      const storedSector = localStorage.getItem("lega_user_sector");
      const storedRegion = localStorage.getItem("lega_user_state");
      if (storedSector && storedRegion) {
        router.push("/feed");
      }
    } else {
      // In edit mode, pre-fill with current settings
      const storedSector = localStorage.getItem("lega_user_sector");
      const storedRegion = localStorage.getItem("lega_user_state");
      if (storedSector) setSector(storedSector);
      if (storedRegion) setRegion(storedRegion);
    }
  }, [router, isEditing]);

  const handleStart = () => {
    localStorage.setItem("lega_user_sector", sector);
    localStorage.setItem("lega_user_state", region);
    router.push("/feed");
  };

  if (!isLoaded) return null;

  return (
    <div className="min-h-screen bg-brand-cream/30 flex flex-col justify-center px-6 relative overflow-hidden font-sans">
      {/* Dynamic Background Elements */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-brand-magenta/20 rounded-full blur-[120px] opacity-60" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-brand-gold/20 rounded-full blur-[120px] opacity-60" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="max-w-md mx-auto w-full relative z-10"
      >
        <div className="text-center mb-10">
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className="inline-flex items-center space-x-2 bg-white px-4 py-1.5 rounded-full shadow-sm border border-brand-darkblue/5 mb-6"
          >
            <Sparkles className="w-4 h-4 text-brand-gold" />
            <span className="text-sm font-semibold text-brand-darkblue/80">
              Empowering Women in Labor
            </span>
          </motion.div>
          <h1 className="text-5xl font-extrabold text-brand-darkblue mb-4 tracking-tighter">
            Lega
          </h1>
          <p className="text-brand-darkblue/60 text-lg leading-relaxed">
            Personalized legal updates for the people who build our communities.
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.98 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white/80 backdrop-blur-xl p-8 rounded-[2rem] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-white"
        >
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-bold text-brand-darkblue mb-3 flex items-center">
                <Briefcase className="w-4 h-4 mr-2 text-brand-gold" />
                Profession
              </label>
              <div className="relative group">
                <select
                  value={sector}
                  onChange={(e) => setSector(e.target.value)}
                  className="w-full p-4 border border-brand-darkblue/10 rounded-2xl appearance-none focus:ring-4 focus:ring-brand-gold/20 focus:border-brand-gold transition-all bg-white font-medium text-brand-darkblue"
                >
                  <option value="Healthcare">
                    Healthcare (Nurse, Tech, etc.)
                  </option>
                  <option value="Education">Education (Teacher, Admin)</option>
                  <option value="Service">Service Industry</option>
                  <option value="Construction">Trades & Construction</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-brand-darkblue/40">
                  <ArrowRight className="w-4 h-4 rotate-90" />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-bold text-brand-darkblue mb-3 flex items-center">
                <MapPin className="w-4 h-4 mr-2 text-brand-gold" />
                Work Location
              </label>
              <div className="relative group">
                <select
                  value={region}
                  onChange={(e) => setRegion(e.target.value)}
                  className="w-full p-4 border border-brand-darkblue/10 rounded-2xl appearance-none focus:ring-4 focus:ring-brand-gold/20 focus:border-brand-gold transition-all bg-white font-medium text-brand-darkblue"
                >
                  <option value="Indiana">Indiana</option>
                  <option value="Illinois">Illinois</option>
                  <option value="Ohio">Ohio</option>
                  <option value="Kentucky">Kentucky</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-brand-darkblue/40">
                  <ArrowRight className="w-4 h-4 rotate-90" />
                </div>
              </div>
            </div>

            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleStart}
              className="w-full bg-brand-darkblue text-white py-4 rounded-2xl font-bold text-lg transition-all shadow-xl shadow-brand-darkblue/20 flex items-center justify-center group"
            >
              <span>{isEditing ? "Save Changes" : "Get Started"}</span>
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform text-brand-gold" />
            </motion.button>
          </div>
        </motion.div>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="text-center mt-8 text-brand-darkblue/40 text-sm font-medium"
        >
          Privacy First. Your data stays on your device.
        </motion.p>
      </motion.div>
    </div>
  );
}

export default function LandingPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-slate-50 flex items-center justify-center">
          Loading...
        </div>
      }
    >
      <LandingContent />
    </Suspense>
  );
}

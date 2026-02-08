"use client";

import React, { useEffect, useState } from "react";
import LawCard from "@/components/LawCard";
import { Settings, Heart } from "lucide-react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";

// Mock Data for scaffolding
const MOCK_BILLS = [
  {
    id: "1",
    title: "The Safe Staffing Act of 2024",
    impact_score: "High",
    summary_points: [
      "Sets mandatory nurse-to-patient ratios in all state hospitals.",
      "Prohibits mandatory overtime for nurses except in declared emergencies.",
      "Requires hospitals to post staffing plans publicly.",
    ],
    audio_url: "https://www.soundhelix.com/examples/mp3/Soundhelix-Song-1.mp3", // Placeholder audio
  },
  {
    id: "2",
    title: "Fair Scheduling & Wages Ordinance",
    impact_score: "Medium",
    summary_points: [
      "Requires 14-day advance notice for all shift schedules.",
      'Mandates "predictability pay" for last-minute schedule changes.',
      "Increases minimum wage for service workers to $18/hr by 2025.",
    ],
    audio_url: "",
  },
];

export default function FeedPage() {
  const router = useRouter();
  const [userSector, setUserSector] = useState<string | null>(null);
  const [userState, setUserState] = useState<string | null>(null);
  const [bills, setBills] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const sector = localStorage.getItem("lega_user_sector") || "Healthcare";
    const state = localStorage.getItem("lega_user_state") || "Indiana";

    setUserSector(sector);
    setUserState(state);

    // Fetch bills from API
    fetch(`http://127.0.0.1:5000/api/feed?sector=${sector}&state=${state}`)
      .then((res) => res.json())
      .then((data) => {
        setBills(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch bills:", err);
        setLoading(false);
      });
  }, []);

  const handleEditProfile = () => {
    router.push("/?edit=true");
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-brand-cream/30 flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-magenta"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#FDFDFF] pb-24 font-sans">
      {/* Header */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-brand-darkblue/5 px-6 py-4 shadow-[0_2px_15px_rgba(0,0,0,0.02)] flex justify-between items-center"
      >
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="cursor-pointer"
          onClick={() => router.push("/")}
        >
          <h1 className="text-2xl font-black text-brand-darkblue tracking-tighter">
            Lega
          </h1>
          <p className="text-[10px] text-brand-gold font-bold uppercase tracking-widest mt-[-2px]">
            {userState} • {userSector}
          </p>
        </motion.div>
        <div className="flex items-center space-x-2">
          <motion.button
            whileHover={{ scale: 1.1, rotate: 15 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleEditProfile}
            className="p-2.5 text-brand-darkblue/40 hover:text-brand-magenta rounded-2xl hover:bg-brand-magenta/5 transition-all border border-transparent hover:border-brand-magenta/10"
          >
            <Settings className="w-5 h-5" />
          </motion.button>
        </div>
      </motion.header>

      {/* Feed Content */}
      <main className="max-w-xl mx-auto px-6 py-10">
        <motion.div
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
          className="flex items-center justify-between mb-10"
        >
          <div>
            <h2 className="text-3xl font-extrabold text-brand-darkblue tracking-tight">
              Latest Updates
            </h2>
            <p className="text-brand-darkblue/40 text-sm mt-1 font-medium italic">
              {new Date().toLocaleDateString("en-US", {
                month: "long",
                day: "numeric",
                year: "numeric",
              })}
            </p>
          </div>
          <span className="text-[11px] font-bold text-brand-magenta bg-brand-magenta/10 px-3 py-1.5 rounded-full border border-brand-magenta/20 shadow-sm animate-pulse">
            {bills.length} NEW
          </span>
        </motion.div>

        <div className="space-y-8">
          <AnimatePresence>
            {bills.map((bill, index) => (
              <motion.div
                key={bill.id}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.1 * index }}
              >
                <LawCard
                  title={bill.title}
                  impact_score={bill.impact_score as "High" | "Medium" | "Low"}
                  summary_points={bill.summary_points}
                  audio_url={bill.audio_url}
                />
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          className="mt-20 text-center py-10 border-t border-brand-darkblue/5"
        >
          <div className="flex justify-center mb-4">
            <Heart className="w-6 h-6 text-brand-darkblue/20" />
          </div>
          <p className="text-brand-darkblue/40 text-sm font-medium">
            You are all caught up for today.
          </p>
          <p className="text-brand-darkblue/30 text-xs mt-2 italic">
            Lega is checking for new updates in {userState}...
          </p>
        </motion.div>
      </main>
    </div>
  );
}

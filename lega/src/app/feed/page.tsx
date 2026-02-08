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
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    const sector = localStorage.getItem("lega_user_sector");
    const state = localStorage.getItem("lega_user_state");

    if (sector) setUserSector(sector);
    else setUserSector("Healthcare");

    if (state) setUserState(state);
    else setUserState("Indiana");

    setIsLoaded(true);
  }, []);

  const handleEditProfile = () => {
    router.push("/?edit=true");
  };

  if (!isLoaded) return null;

  return (
    <div className="min-h-screen bg-[#FDFDFF] pb-24 font-sans">
      {/* Header */}
      <motion.header
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        className="bg-white/80 backdrop-blur-md sticky top-0 z-50 border-b border-slate-100 px-6 py-4 shadow-[0_2px_15px_rgba(0,0,0,0.02)] flex justify-between items-center"
      >
        <motion.div
          whileHover={{ scale: 1.02 }}
          className="cursor-pointer"
          onClick={() => router.push("/")}
        >
          <h1 className="text-2xl font-black text-slate-900 tracking-tighter">
            Lega
          </h1>
          <p className="text-[10px] text-indigo-500 font-bold uppercase tracking-widest mt-[-2px]">
            {userState || "Local"} • {userSector || "Labor"}
          </p>
        </motion.div>
        <div className="flex items-center space-x-2">
          <motion.button
            whileHover={{ scale: 1.1, rotate: 15 }}
            whileTap={{ scale: 0.9 }}
            onClick={handleEditProfile}
            className="p-2.5 text-slate-400 hover:text-indigo-600 rounded-2xl hover:bg-indigo-50 transition-all border border-transparent hover:border-indigo-100"
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
            <h2 className="text-3xl font-extrabold text-slate-900 tracking-tight">
              Latest Updates
            </h2>
            <p className="text-slate-400 text-sm mt-1 font-medium italic">
              {new Date().toLocaleDateString("en-US", {
                month: "long",
                day: "numeric",
                year: "numeric",
              })}
            </p>
          </div>
          <span className="text-[11px] font-bold text-emerald-600 bg-emerald-50 px-3 py-1.5 rounded-full border border-emerald-100 shadow-sm animate-pulse">
            2 NEW
          </span>
        </motion.div>

        <div className="space-y-8">
          <AnimatePresence>
            {MOCK_BILLS.map((bill, index) => (
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
          className="mt-20 text-center py-10 border-t border-slate-50"
        >
          <div className="flex justify-center mb-4">
            <Heart className="w-6 h-6 text-slate-200" />
          </div>
          <p className="text-slate-400 text-sm font-medium">
            You are all caught up for today.
          </p>
          <p className="text-slate-300 text-xs mt-2 italic">
            Lega is checking for new updates in {userState}...
          </p>
        </motion.div>
      </main>
    </div>
  );
}

"use client";

import React, { useState, useRef } from "react";
import { Play, Pause, FileText, Activity, ArrowUpRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

interface LawCardProps {
  title: string;
  impact_score: "High" | "Medium" | "Low";
  summary_points: string[];
  audio_url?: string;
}

export default function LawCard({
  title,
  impact_score,
  summary_points,
  audio_url,
}: LawCardProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const toggleAudio = () => {
    if (!audioRef.current) return;
    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  const getImpactStyles = (score: string) => {
    switch (score) {
      case "High":
        return {
          bg: "bg-brand-magenta/10",
          text: "text-brand-magenta",
          border: "border-brand-magenta/20",
          dot: "bg-brand-magenta",
        };
      case "Medium":
        return {
          bg: "bg-brand-gold/10",
          text: "text-brand-gold",
          border: "border-brand-gold/20",
          dot: "bg-brand-gold",
        };
      case "Low":
        return {
          bg: "bg-brand-darkblue/10",
          text: "text-brand-darkblue",
          border: "border-brand-darkblue/20",
          dot: "bg-brand-darkblue",
        };
      default:
        return {
          bg: "bg-brand-cream",
          text: "text-brand-darkgrey",
          border: "border-brand-darkgrey/10",
          dot: "bg-brand-darkgrey",
        };
    }
  };

  const styles = getImpactStyles(impact_score);

  return (
    <motion.div
      whileHover={{ y: -4, boxShadow: "0 20px 25px -5px rgb(0 0 0 / 0.1)" }}
      className="bg-white rounded-[2rem] shadow-[0_4px_20px_rgba(0,0,0,0.03)] border border-slate-100 p-8 transition-all"
    >
      <div className="flex justify-between items-start mb-6">
        <div className="flex-1 mr-6">
          <div className="flex items-center space-x-2 mb-3">
            <span className={`flex h-2 w-2 rounded-full ${styles.dot}`} />
            <span
              className={`text-[10px] font-black uppercase tracking-[0.2em] ${styles.text}`}
            >
              {impact_score} Impact
            </span>
          </div>
          <h3 className="text-2xl font-bold text-slate-900 leading-tight tracking-tight">
            {title}
          </h3>
        </div>
        <motion.div
          whileHover={{ rotate: 45 }}
          className="p-3 bg-slate-50 rounded-2xl text-slate-400"
        >
          <ArrowUpRight className="w-5 h-5" />
        </motion.div>
      </div>

      <div className="space-y-4 mb-8">
        {summary_points.map((point, idx) => (
          <div key={idx} className="flex items-start group">
            <div className="w-6 h-6 rounded-lg bg-indigo-50 flex items-center justify-center mr-4 mt-0.5 flex-shrink-0 group-hover:bg-indigo-100 transition-colors">
              <Activity className="w-3.5 h-3.5 text-brand-darkblue" />
            </div>
            <p className="text-slate-600 text-[15px] leading-relaxed font-medium">
              {point}
            </p>
          </div>
        ))}
      </div>

      <div className="flex items-center justify-between pt-6 border-t border-slate-50">
        <motion.button
          whileHover={{ x: 3 }}
          onClick={toggleAudio}
          className={`flex items-center space-x-3 font-bold text-sm transition-colors ${
            audio_url
              ? "text-brand-magenta hover:text-brand-magenta/80"
              : "text-slate-300 cursor-not-allowed"
          }`}
          disabled={!audio_url}
        >
          <div
            className={`p-2 rounded-full ${audio_url ? "bg-brand-magenta/10" : "bg-slate-50"}`}
          >
            {isPlaying ? (
              <Pause className="w-4 h-4 fill-current" />
            ) : (
              <Play className="w-4 h-4 fill-current ml-0.5" />
            )}
          </div>
          <span>{isPlaying ? "Pause Summary" : "Listen to Summary"}</span>
        </motion.button>

        {audio_url && (
          <audio
            ref={audioRef}
            src={audio_url}
            onEnded={() => setIsPlaying(false)}
            className="hidden"
          />
        )}

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="bg-brand-darkblue text-white px-6 py-3 rounded-2xl text-sm font-bold shadow-lg shadow-brand-darkblue/20"
        >
          Take Action
        </motion.button>
      </div>
    </motion.div>
  );
}

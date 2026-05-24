"use client";

import { motion } from "framer-motion";

export default function HeroSection() {
  return (
    <section className="relative flex min-h-screen items-center justify-center overflow-hidden px-6">
      {/* Background Glow */}
      <div className="absolute top-1/2 left-1/2 h-[500px] w-[500px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-[#D4B483]/10 blur-3xl" />

      <div className="relative z-10 mx-auto max-w-6xl text-center">
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-6 text-sm tracking-[0.4em] text-[#D4B483]"
        >
          تجربه لوکس زیبایی
        </motion.p>

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="text-5xl leading-tight font-semibold tracking-tight md:text-8xl"
        >
          زیبایی مدرن،
          <br />
          تجربه‌ای فراتر از انتظار
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="mx-auto mt-8 max-w-2xl text-lg leading-8 text-zinc-400"
        >
          خدمات حرفه‌ای زیبایی با رزرو آنلاین، فضای لوکس و تجربه‌ای متفاوت برای
          کسانی که به جزئیات اهمیت می‌دهند.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="mt-12 flex items-center justify-center gap-4"
        >
          <button className="rounded-full bg-[#D4B483] px-8 py-4 text-sm font-medium text-black transition hover:scale-[1.03]">
            رزرو آنلاین
          </button>

          <button className="rounded-full border border-white/10 bg-white/5 px-8 py-4 text-sm font-medium backdrop-blur-xl transition hover:border-white/20">
            مشاهده خدمات
          </button>
        </motion.div>
      </div>
    </section>
  );
}
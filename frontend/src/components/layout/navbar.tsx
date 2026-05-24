"use client";

import { motion } from "framer-motion";

export default function Navbar() {
  return (
    <motion.header
      initial={{ opacity: 0, y: -30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.7 }}
      className="fixed top-0 left-0 z-50 w-full px-6 py-6"
    >
      <div className="mx-auto flex max-w-7xl items-center justify-between rounded-full border border-white/10 bg-white/5 px-6 py-4 backdrop-blur-xl">
        <div>
          <h2 className="text-lg font-semibold tracking-wide">
            سالن زیبایی
          </h2>
        </div>

        <nav className="hidden items-center gap-8 text-sm text-zinc-300 md:flex">
          <a
            href="#"
            className="transition hover:text-white"
          >
            خدمات
          </a>

          <a
            href="#"
            className="transition hover:text-white"
          >
            گالری
          </a>

          <a
            href="#"
            className="transition hover:text-white"
          >
            درباره ما
          </a>

          <a
            href="#"
            className="transition hover:text-white"
          >
            تماس
          </a>
        </nav>

        <button className="rounded-full bg-[#D4B483] px-5 py-2 text-sm font-medium text-black transition hover:scale-[1.02]">
          رزرو نوبت
        </button>
      </div>
    </motion.header>
  );
}
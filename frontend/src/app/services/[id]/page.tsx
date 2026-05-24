"use client";

import { useState } from "react";
import { motion } from "framer-motion";

const mockService = {
  id: 1,
  title: "کوتاهی مو حرفه‌ای",
  description: "خدمات حرفه‌ای با استایل مدرن و متناسب با فرم صورت",
};

const mockStaff = [
  { id: 1, name: "آرایشگر ۱" },
  { id: 2, name: "آرایشگر ۲" },
];

const mockSlots = [
  "09:00",
  "10:30",
  "12:00",
  "14:00",
  "16:00",
];

export default function ServiceDetailPage() {
  const [selectedStaff, setSelectedStaff] = useState<number | null>(null);
  const [selectedSlot, setSelectedSlot] = useState<string | null>(null);

  return (
    <main className="min-h-screen bg-[#0B0B0B] text-white px-6 py-32">
      <div className="mx-auto max-w-5xl">
        {/* Header */}
        <div className="mb-16 text-center">
          <p className="text-sm tracking-[0.3em] text-[#D4B483]">
            رزرو خدمات
          </p>

          <h1 className="mt-4 text-5xl font-semibold">
            {mockService.title}
          </h1>

          <p className="mt-6 text-zinc-400">
            {mockService.description}
          </p>
        </div>

        {/* Staff Selection */}
        <section className="mb-16">
          <h2 className="mb-6 text-xl font-medium">انتخاب آرایشگر</h2>

          <div className="grid gap-4 md:grid-cols-2">
            {mockStaff.map((staff) => (
              <motion.button
                key={staff.id}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelectedStaff(staff.id)}
                className={`rounded-2xl border p-6 text-right transition ${
                  selectedStaff === staff.id
                    ? "border-[#D4B483] bg-[#D4B483]/10"
                    : "border-white/10 bg-white/5"
                }`}
              >
                {staff.name}
              </motion.button>
            ))}
          </div>
        </section>

        {/* Slot Selection */}
        <section className="mb-16">
          <h2 className="mb-6 text-xl font-medium">انتخاب زمان</h2>

          <div className="grid grid-cols-3 gap-4 md:grid-cols-5">
            {mockSlots.map((slot) => (
              <motion.button
                key={slot}
                whileTap={{ scale: 0.98 }}
                onClick={() => setSelectedSlot(slot)}
                className={`rounded-xl border py-3 text-sm transition ${
                  selectedSlot === slot
                    ? "border-[#D4B483] bg-[#D4B483]/10 text-[#D4B483]"
                    : "border-white/10 bg-white/5 text-white"
                }`}
              >
                {slot}
              </motion.button>
            ))}
          </div>
        </section>

        {/* CTA */}
        <div className="flex justify-center">
          <button
            disabled={!selectedStaff || !selectedSlot}
            className="rounded-full bg-[#D4B483] px-10 py-4 text-sm font-medium text-black disabled:opacity-40"
          >
            تایید و رزرو نوبت
          </button>
        </div>
      </div>
    </main>
  );
}
"use client";

import { motion } from "framer-motion";

const services = [
  {
    title: "کوتاهی مو",
    desc: "استایل حرفه‌ای متناسب با فرم صورت",
  },
  {
    title: "رنگ و هایلایت",
    desc: "رنگ‌های تخصصی با تکنیک‌های مدرن",
  },
  {
    title: "میکاپ حرفه‌ای",
    desc: "آرایش مناسب مراسم و استایل شخصی",
  },
  {
    title: "مراقبت پوست",
    desc: "فیشیال و درمان‌های تخصصی پوست",
  },
];

export default function ServicesSection() {
  return (
    <section className="relative px-6 py-32">
      <div className="mx-auto max-w-6xl">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mb-16 text-center"
        >
          <p className="mb-4 text-sm tracking-[0.3em] text-[#D4B483]">
            خدمات ما
          </p>

          <h2 className="text-4xl font-semibold md:text-6xl">
            تجربه‌ای کامل از زیبایی
          </h2>

          <p className="mx-auto mt-6 max-w-2xl text-zinc-400">
            مجموعه‌ای از خدمات حرفه‌ای با بالاترین کیفیت برای تجربه‌ای لوکس و
            متفاوت
          </p>
        </motion.div>

        {/* Grid */}
        <div className="grid gap-6 md:grid-cols-2">
          {services.map((service, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
              className="group rounded-3xl border border-white/10 bg-white/5 p-8 backdrop-blur-xl transition hover:border-white/20"
            >
              <h3 className="text-xl font-semibold group-hover:text-[#D4B483] transition">
                {service.title}
              </h3>

              <p className="mt-3 text-zinc-400 leading-7">
                {service.desc}
              </p>

              <div className="mt-6 text-sm text-[#D4B483] opacity-0 transition group-hover:opacity-100">
                رزرو این خدمت →
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
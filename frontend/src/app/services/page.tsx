"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";
import Link from "next/link";

import { getServices } from "@/lib/api/services";

type Service = {
  id: number;
  title: string;
  duration: number;
  reserve_fee: number;
};

type Category = {
  id: number;
  title: string;
  services: Service[];
};

const containerVariants = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: 0.14,
    },
  },
};

const cardVariants = {
  hidden: {
    opacity: 0,
    y: 60,
  },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.8,
      ease: "easeOut",
    },
  },
};

export default function ServicesPage() {
  const [categories, setCategories] = useState<Category[]>([]);

  useEffect(() => {
    const load = async () => {
      const data = await getServices();
      setCategories(data);
    };

    load();
  }, []);

  return (
    <main className="min-h-screen overflow-hidden bg-[#070707] text-white">
      {/* BACKGROUND GLOW */}
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute left-1/2 top-0 h-[500px] w-[500px] -translate-x-1/2 rounded-full bg-[#D4B483]/10 blur-[140px]" />
      </div>

      {/* HERO */}
      <section className="relative border-b border-white/10 px-6 py-40">
        <div className="mx-auto max-w-7xl">
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="mb-6 text-sm tracking-[0.5em] text-[#D4B483]"
          >
            SERVICES
          </motion.p>

          <motion.h1
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1 }}
            className="max-w-5xl text-6xl font-semibold leading-[1.1] tracking-tight md:text-8xl"
          >
            تجربه‌ای لوکس
            <br />
            برای زیبایی مدرن
          </motion.h1>

          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 0.7 }}
            transition={{ delay: 0.5 }}
            className="mt-10 max-w-2xl text-lg leading-8 text-zinc-400"
          >
            خدمات تخصصی زیبایی با استاندارد حرفه‌ای، فضای آرام و
            تجربه‌ای متفاوت برای افرادی که به جزئیات اهمیت می‌دهند.
          </motion.p>
        </div>
      </section>

      {/* CONTENT */}
      <section className="relative px-6 py-24">
        <div className="mx-auto max-w-7xl space-y-36">
          {categories.map((category) => (
            <div key={category.id}>
              {/* CATEGORY HEADER */}
              <div className="mb-16 flex items-end justify-between border-b border-white/10 pb-6">
                <div>
                  <p className="mb-3 text-xs tracking-[0.4em] text-zinc-500">
                    CATEGORY
                  </p>

                  <h2 className="text-4xl font-semibold tracking-tight md:text-5xl">
                    {category.title}
                  </h2>
                </div>
              </div>

              {/* SERVICES GRID */}
              <motion.div
                variants={containerVariants}
                initial="hidden"
                whileInView="show"
                viewport={{ once: true }}
                className="grid gap-8 md:grid-cols-2 xl:grid-cols-3"
              >
                {category.services.map((service) => (
                  <motion.div
                    key={service.id}
                    variants={cardVariants}
                    whileHover={{
                      y: -10,
                    }}
                    transition={{
                      type: "spring",
                      stiffness: 120,
                    }}
                  >
                    <Link
                      href={`/services/${service.id}`}
                      className="group relative flex h-full min-h-[340px] flex-col overflow-hidden rounded-[2.5rem] border border-white/10 bg-white/[0.03] p-8 backdrop-blur-xl transition duration-500 hover:border-[#D4B483]/30 hover:bg-white/[0.05]"
                    >
                      {/* gradient glow */}
                      <div className="absolute inset-0 opacity-0 transition duration-700 group-hover:opacity-100">
                        <div className="absolute left-1/2 top-0 h-72 w-72 -translate-x-1/2 rounded-full bg-[#D4B483]/10 blur-3xl" />
                      </div>

                      {/* top line */}
                      <div className="relative z-10 mb-12 flex items-center justify-between">
                        <span className="text-sm tracking-wide text-zinc-500">
                          {service.duration} دقیقه
                        </span>

                        <span className="rounded-full border border-white/10 px-4 py-1 text-xs text-zinc-400">
                          Premium
                        </span>
                      </div>

                      {/* title */}
                      <motion.h3
                        whileHover={{
                          x: -4,
                        }}
                        className="relative z-10 text-3xl font-semibold leading-tight tracking-tight transition group-hover:text-[#D4B483]"
                      >
                        {service.title}
                      </motion.h3>

                      {/* divider */}
                      <div className="relative z-10 my-10 h-px bg-gradient-to-r from-transparent via-white/10 to-transparent" />

                      {/* footer */}
                      <div className="relative z-10 mt-auto flex items-end justify-between">
                        <div>
                          <p className="text-2xl font-medium tracking-tight">
                            {service.reserve_fee.toLocaleString()}
                          </p>

                          <span className="text-sm text-zinc-500">
                            تومان
                          </span>
                        </div>

                        <div className="flex items-center gap-2 text-sm text-[#D4B483]">
                          رزرو

                          <motion.span
                            animate={{
                              x: [0, 4, 0],
                            }}
                            transition={{
                              duration: 1.8,
                              repeat: Infinity,
                            }}
                          >
                            →
                          </motion.span>
                        </div>
                      </div>

                      {/* glass reflection */}
                      <div className="absolute inset-0 opacity-0 transition duration-700 group-hover:opacity-100">
                        <div className="absolute -left-20 top-0 h-full w-20 rotate-12 bg-white/5 blur-2xl" />
                      </div>
                    </Link>
                  </motion.div>
                ))}
              </motion.div>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}
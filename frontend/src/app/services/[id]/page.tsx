"use client";

import { use, useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

import { getAvailableSlots } from "@/lib/api/booking";

import {
  getServices,
  getServiceStaff,
} from "@/lib/api/services";

type Props = {
  params: Promise<{
    id: string;
  }>;
};

type Service = {
  id: number;
  title: string;
  duration: number;
  reserve_fee: number;
};

type Staff = {
  id: number;
  first_name: string;
  last_name: string;
};

type Slot = {
  start_time: string;
  end_time: string;
  is_available: boolean;
};

type SlotDay = {
  date: string;
  slots: Slot[];
};

export default function ServiceDetailPage({
  params,
}: Props) {
  const { id } = use(params);

  const [service, setService] =
    useState<Service | null>(null);

  const [staff, setStaff] = useState<Staff[]>([]);

  const [staffId, setStaffId] =
    useState<number | null>(null);

  const [slots, setSlots] = useState<SlotDay[]>([]);

  const [selectedSlot, setSelectedSlot] =
    useState<{
      date: string;
      start_time: string;
      end_time: string;
    } | null>(null);

  const [loading, setLoading] = useState(true);

  const [slotsLoading, setSlotsLoading] =
    useState(false);

  // LOAD SERVICE + STAFF
  useEffect(() => {
    const load = async () => {
      try {
        setLoading(true);

        const categories =
          await getServices();

        const allServices =
          categories.flatMap(
            (category: any) =>
              category.services
          );

        const currentService =
          allServices.find(
            (item: Service) =>
              item.id === Number(id)
          );

        setService(currentService || null);

        const staffData =
          await getServiceStaff(
            Number(id)
          );

        setStaff(staffData);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [id]);

  // LOAD SLOTS
  useEffect(() => {
    if (!staffId) return;

    const loadSlots = async () => {
      try {
        setSlotsLoading(true);

        const data =
          await getAvailableSlots(
            Number(id),
            staffId
          );

        setSlots(data);
      } catch (error) {
        console.error(
          "SLOTS ERROR:",
          error
        );
      } finally {
        setSlotsLoading(false);
      }
    };

    loadSlots();
  }, [staffId, id]);

  // LOADING
  if (loading) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#0B0B0B] text-white">
        <div className="animate-pulse text-zinc-400">
          در حال بارگذاری...
        </div>
      </main>
    );
  }

  // NOT FOUND
  if (!service) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-[#0B0B0B] text-white">
        <div className="text-zinc-400">
          سرویس پیدا نشد
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-[#0B0B0B] text-white">
      {/* HERO */}
      <section className="relative overflow-hidden border-b border-white/10 px-6 py-32">
        {/* glow */}
        <div className="absolute top-0 left-1/2 h-[500px] w-[500px] -translate-x-1/2 rounded-full bg-[#D4B483]/10 blur-[140px]" />

        <div className="relative mx-auto max-w-7xl">
          <motion.div
            initial={{
              opacity: 0,
              y: 30,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            transition={{
              duration: 0.7,
            }}
          >
            <p className="mb-6 text-sm tracking-[0.35em] text-[#D4B483]">
              SERVICE DETAIL
            </p>

            <h1 className="max-w-4xl text-5xl leading-tight font-semibold md:text-7xl">
              {service.title}
            </h1>

            <div className="mt-10 flex flex-wrap items-center gap-4 text-zinc-400">
              <div className="rounded-full border border-white/10 bg-white/[0.03] px-5 py-3">
                {service.duration} دقیقه
              </div>

              <div className="rounded-full border border-white/10 bg-white/[0.03] px-5 py-3">
                {service.reserve_fee.toLocaleString()}

                <span className="mr-2 text-zinc-500">
                  تومان
                </span>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* STAFF */}
      <section className="px-6 py-24">
        <div className="mx-auto max-w-7xl">
          <div className="mb-14">
            <p className="mb-4 text-sm tracking-[0.3em] text-[#D4B483]">
              SPECIALISTS
            </p>

            <h2 className="text-4xl font-semibold">
              انتخاب متخصص
            </h2>
          </div>

          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
            {staff.map((item, index) => (
              <motion.button
                key={item.id}
                initial={{
                  opacity: 0,
                  y: 30,
                }}
                animate={{
                  opacity: 1,
                  y: 0,
                }}
                transition={{
                  delay: index * 0.08,
                }}
                onClick={() => {
                  setStaffId(item.id);
                  setSelectedSlot(null);
                }}
                className={`group relative overflow-hidden rounded-[2rem] border p-8 text-right transition duration-500 ${
                  staffId === item.id
                    ? "border-[#D4B483] bg-[#D4B483]/10"
                    : "border-white/10 bg-white/[0.03] hover:border-white/20 hover:bg-white/[0.05]"
                }`}
              >
                {/* glow */}
                <div className="absolute inset-0 opacity-0 transition duration-500 group-hover:opacity-100">
                  <div className="absolute top-0 left-1/2 h-40 w-40 -translate-x-1/2 rounded-full bg-[#D4B483]/10 blur-3xl" />
                </div>

                <div className="relative z-10 flex items-center justify-between">
                  <div>
                    <h3 className="text-2xl font-semibold">
                      {item.first_name}
                    </h3>

                    <p className="mt-2 text-zinc-400">
                      {item.last_name}
                    </p>
                  </div>

                  <div
                    className={`h-3 w-3 rounded-full transition ${
                      staffId === item.id
                        ? "bg-[#D4B483]"
                        : "bg-zinc-700"
                    }`}
                  />
                </div>
              </motion.button>
            ))}
          </div>
        </div>
      </section>

      {/* SLOTS */}
      <AnimatePresence mode="wait">
        {staffId && (
          <motion.section
            key={staffId}
            initial={{
              opacity: 0,
              y: 40,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            exit={{
              opacity: 0,
            }}
            transition={{
              duration: 0.5,
            }}
            className="border-t border-white/10 px-6 py-24"
          >
            <div className="mx-auto max-w-7xl">
              <div className="mb-14">
                <p className="mb-4 text-sm tracking-[0.3em] text-[#D4B483]">
                  AVAILABLE TIMES
                </p>

                <h2 className="text-4xl font-semibold">
                  زمان‌های خالی
                </h2>
              </div>

              {slotsLoading ? (
                <div className="text-zinc-500">
                  در حال دریافت زمان‌ها...
                </div>
              ) : slots.length === 0 ? (
                <div className="rounded-[2rem] border border-white/10 bg-white/[0.03] p-10 text-zinc-400">
                  زمانی برای این متخصص پیدا نشد.
                </div>
              ) : (
                <div className="space-y-14">
                  {slots.map(
                    (
                      day,
                      dayIndex
                    ) => (
                      <motion.div
                        key={day.date}
                        initial={{
                          opacity: 0,
                          y: 20,
                        }}
                        animate={{
                          opacity: 1,
                          y: 0,
                        }}
                        transition={{
                          delay:
                            dayIndex *
                            0.08,
                        }}
                      >
                        {/* DATE */}
                        <div className="mb-6 flex items-center gap-4">
                          <div className="h-px flex-1 bg-white/10" />

                          <h3 className="text-lg font-medium text-[#D4B483]">
                            {day.date}
                          </h3>

                          <div className="h-px flex-1 bg-white/10" />
                        </div>

                        {/* TIMES */}
                        <div className="flex flex-wrap gap-4">
                          {day.slots.map(
                            (
                              slot,
                              slotIndex
                            ) => {
                              const isSelected =
                                selectedSlot?.date ===
                                  day.date &&
                                selectedSlot?.start_time ===
                                  slot.start_time;

                              return (
                                <motion.button
                                  key={
                                    slotIndex
                                  }
                                  whileHover={{
                                    y: -4,
                                  }}
                                  whileTap={{
                                    scale: 0.97,
                                  }}
                                  disabled={
                                    !slot.is_available
                                  }
                                  onClick={() =>
                                    setSelectedSlot(
                                      {
                                        date: day.date,
                                        start_time:
                                          slot.start_time,
                                        end_time:
                                          slot.end_time,
                                      }
                                    )
                                  }
                                  className={`rounded-full border px-6 py-4 transition duration-300 ${
                                    isSelected
                                      ? "border-[#D4B483] bg-[#D4B483]/15 text-white"
                                      : slot.is_available
                                      ? "border-white/10 bg-white/[0.03] hover:border-[#D4B483] hover:bg-[#D4B483]/10"
                                      : "cursor-not-allowed border-red-500/20 bg-red-500/10 text-red-300 opacity-50"
                                  }`}
                                >
                                  {slot.start_time.slice(
                                    0,
                                    5
                                  )}
                                </motion.button>
                              );
                            }
                          )}
                        </div>
                      </motion.div>
                    )
                  )}
                </div>
              )}

              {/* SELECTED SLOT */}
              {selectedSlot && (
                <motion.div
                  initial={{
                    opacity: 0,
                    y: 20,
                  }}
                  animate={{
                    opacity: 1,
                    y: 0,
                  }}
                  className="mt-16 rounded-[2rem] border border-[#D4B483]/20 bg-[#D4B483]/10 p-8"
                >
                  <p className="text-zinc-300">
                    زمان انتخاب شده:
                  </p>

                  <div className="mt-4 flex flex-wrap items-center gap-4">
                    <div className="rounded-full bg-black/30 px-5 py-3">
                      {selectedSlot.date}
                    </div>

                    <div className="rounded-full bg-black/30 px-5 py-3">
                      {selectedSlot.start_time.slice(
                        0,
                        5
                      )}
                    </div>
                  </div>

                  <button className="mt-8 rounded-full bg-[#D4B483] px-8 py-4 font-medium text-black transition hover:scale-[1.02]">
                    ادامه رزرو
                  </button>
                </motion.div>
              )}
            </div>
          </motion.section>
        )}
      </AnimatePresence>
    </main>
  );
}
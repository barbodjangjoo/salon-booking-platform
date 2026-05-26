"use client";

import { use, useEffect, useState } from "react";

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

export default function ServiceDetailPage({ params }: Props) {
  const { id } = use(params);

  const [service, setService] = useState<any>(null);
  const [staff, setStaff] = useState<any[]>([]);
  const [staffId, setStaffId] = useState<number | null>(null);
  const [slots, setSlots] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      try {
        // پیدا کردن اطلاعات سرویس
        const categories = await getServices();

        const allServices = categories.flatMap(
          (category: any) => category.services
        );

        const currentService = allServices.find(
          (item: any) => item.id === Number(id)
        );

        setService(currentService);

        // گرفتن استاف ها
        const staffData = await getServiceStaff(Number(id));

        setStaff(staffData);
      } catch (error) {
        console.error(error);
      }
    };

    load();
  }, [id]);

  useEffect(() => {
    if (!staffId) return;

    const loadSlots = async () => {
      try {
        const data = await getAvailableSlots(
          Number(id),
          staffId
        );

        setSlots(data);
      } catch (error) {
        console.error(error);
      }
    };

    loadSlots();
  }, [staffId, id]);

  return (
    <main className="min-h-screen bg-[#0B0B0B] px-6 py-32 text-white">
      <div className="mx-auto max-w-7xl">
        {/* HERO */}
        <div className="border-b border-white/10 pb-12">
          <p className="mb-5 text-sm tracking-[0.3em] text-[#D4B483]">
            SERVICE DETAIL
          </p>

          <h1 className="text-5xl font-semibold md:text-7xl">
            {service?.title}
          </h1>

          <div className="mt-8 flex items-center gap-5 text-zinc-400">
            <span>
              {service?.duration} دقیقه
            </span>

            <span className="h-1 w-1 rounded-full bg-zinc-600" />

            <span>
              {service?.reserve_fee?.toLocaleString()}
              {" "}
              تومان
            </span>
          </div>
        </div>

        {/* STAFF */}
        <div className="mt-20">
          <h2 className="mb-10 text-3xl font-semibold">
            انتخاب متخصص
          </h2>

          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
            {staff.map((item) => (
              <button
                key={item.id}
                onClick={() => setStaffId(item.id)}
                className={`group rounded-[2rem] border p-8 text-right transition duration-300 ${
                  staffId === item.id
                    ? "border-[#D4B483] bg-[#D4B483]/10"
                    : "border-white/10 bg-white/[0.03] hover:border-white/20 hover:bg-white/[0.05]"
                }`}
              >
                <div className="flex items-center justify-between">
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
                        : "bg-zinc-700 group-hover:bg-zinc-500"
                    }`}
                  />
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* SLOTS */}
        {slots.length > 0 && (
          <div className="mt-24">
            <h2 className="mb-10 text-3xl font-semibold">
              زمان‌های خالی
            </h2>

            <div className="flex flex-wrap gap-4">
              {slots.map((slot: any, index) => (
                <button
                  key={index}
                  className="rounded-full border border-white/10 bg-white/[0.03] px-6 py-4 transition hover:border-[#D4B483] hover:bg-[#D4B483]/10"
                >
                  {slot.start_time}
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </main>
  );
}
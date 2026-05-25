"use client";

import { useEffect, useState } from "react";
import { getAvailableSlots } from "@/lib/api/booking";
import { getServiceDetail } from "@/lib/api/services"

export default function ServiceDetailPage({ params }: any) {
  const [service, setService] = useState<any>(null);
  const [staffId, setStaffId] = useState<number | null>(null);
  const [slots, setSlots] = useState<any[]>([]);

  useEffect(() => {
    const load = async () => {
      const data = await getServiceDetail(params.id);
      setService(data);
    };

    load();
  }, [params.id]);

  useEffect(() => {
    if (!staffId) return;

    const loadSlots = async () => {
      const data = await getAvailableSlots(params.id, staffId);
      setSlots(data);
    };

    loadSlots();
  }, [staffId]);

  return (
    <main className="min-h-screen bg-[#0B0B0B] text-white px-6 py-32">
      <h1 className="text-4xl">{service?.title}</h1>

      <div className="mt-10">
        <p className="text-zinc-400">
          انتخاب آرایشگر و زمان از API واقعی
        </p>

        {/* later UI */}
      </div>
    </main>
  );
}
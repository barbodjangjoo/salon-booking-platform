"use client";

import { useEffect, useState } from "react";

import {
  getAppointments,
  cancelAppointment,
} from "@/lib/api/booking";

export default function AppointmentsPage() {
  const [appointments, setAppointments] =
    useState<any[]>([]);

  useEffect(() => {
    loadAppointments();
  }, []);

  const loadAppointments =
    async () => {
      const data =
        await getAppointments();

      setAppointments(data);
    };

  const handleCancel = async (
    id: number
  ) => {
    await cancelAppointment(id);

    loadAppointments();
  };

  return (
    <main className="min-h-screen bg-black p-10 text-white">
      <h1 className="mb-10 text-4xl">
        نوبت‌های من
      </h1>

      <div className="space-y-4">
        {appointments.map(
          (appointment) => (
            <div
              key={appointment.id}
              className="rounded-3xl border border-white/10 p-6"
            >
              <p>
                سرویس:
                {" "}
                {appointment.service}
              </p>

              <p>
                تاریخ:
                {" "}
                {appointment.date}
              </p>

              <p>
                ساعت:
                {" "}
                {appointment.start_time}
              </p>

              <button
                onClick={() =>
                  handleCancel(
                    appointment.id
                  )
                }
                className="mt-4 rounded-full bg-red-500 px-5 py-2"
              >
                لغو نوبت
              </button>
            </div>
          )
        )}
      </div>
    </main>
  );
}
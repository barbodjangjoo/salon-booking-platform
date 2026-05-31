// lib/api/booking.ts

import api from "./client";

export const getAvailableSlots = async (
  serviceId: number,
  staffId: number
) => {
  const res = await api.get(
    `/core/services/${serviceId}/slots/?staff=${staffId}`
  );

  return res.data;
};

export const createAppointment = async (
  data: {
    staff: number;
    service: number;
    date: string;
    start_time: string;
  }
) => {
  const res = await api.post(
    "/appointment/booking/",
    data
  );

  return res.data;
};

export const getAppointments =
  async () => {
    const res = await api.get(
      "/appointment/"
    );

    return res.data;
  };

export const cancelAppointment =
  async (id: number) => {
    const res = await api.delete(
      `/appointment/${id}/`
    );

    return res.data;
  };
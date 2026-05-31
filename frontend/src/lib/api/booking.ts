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
  data: any
) => {
  const res = await api.post(
    "/appointment/booking/",
    data
  );

  return res.data;
};
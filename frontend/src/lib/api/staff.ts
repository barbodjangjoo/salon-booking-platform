import api from "./client";

export const getStaffByService = async (serviceId: number) => {
  const res = await api.get(`/core/service/${serviceId}/`);
  return res.data;
};
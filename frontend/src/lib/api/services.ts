import api from "./client";

export const getServices = async () => {
  const res = await api.get("/core/categories/");
  return res.data;
};

export const getServiceStaff = async (id: number) => {
  const res = await api.get(`/core/service/${id}/`);
  return res.data;
};
// lib/api/auth.ts

import api from "./client";

export const login = async (
  username: string,
  password: string
) => {
  const res = await api.post(
    "/core/token/",
    {
      username,
      password,
    }
  );

  return res.data;
};

export const register = async (
  data: {
    first_name: string;
    last_name: string;
    phone_number: string;
    username: string;
    email: string;
    password: string;
    password2: string;
  }
) => {
  const res = await api.post(
    "/core/registration/",
    data
  );

  return res.data;
};
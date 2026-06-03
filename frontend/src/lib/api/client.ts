
import axios from "axios";

const api = axios.create({
  baseURL:
    process.env.NEXT_PUBLIC_API_URL,
});

api.interceptors.request.use(
  (config) => {
    const token =
      localStorage.getItem(
        "access_token"
      );

    if (token) {
      config.headers.Authorization =
        `JWT ${token}`;
    }

    return config;
  }
);

export default api;
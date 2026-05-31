export const saveTokens = (
  access: string,
  refresh: string
) => {
  localStorage.setItem("access_token", access);
  localStorage.setItem("refresh_token", refresh);
};

export const isAuthenticated = () => {
  if (typeof window === "undefined") {
    return false;
  }

  return !!localStorage.getItem(
    "access_token"
  );
};

export const logout = () => {
  localStorage.removeItem(
    "access_token"
  );

  localStorage.removeItem(
    "refresh_token"
  );
};
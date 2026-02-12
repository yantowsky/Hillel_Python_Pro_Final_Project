const getToken = (key) => localStorage.getItem(key) || "";

export const projectA = async (path, options = {}) => {
  const baseUrl = import.meta.env.VITE_PROJECTA_API_URL;
  const token = getToken("tokenA");

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const res = await fetch(`${baseUrl}${path}`, { ...options, headers });
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    throw new Error(data?.detail || `ProjectA error ${res.status}`);
  }
  return data;
};

export const projectB = async (path, options = {}) => {
  const baseUrl = import.meta.env.VITE_PROJECTB_API_URL;
  const token = getToken("tokenB");

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const res = await fetch(`${baseUrl}${path}`, { ...options, headers });
  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    throw new Error(data?.detail || `ProjectB error ${res.status}`);
  }
  return data;
};
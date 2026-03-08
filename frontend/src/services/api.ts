import axios from "axios"

const API_BASE = "http://localhost:5173"

/* ---------------- GLOBAL AXIOS INSTANCE ---------------- */

const api = axios.create({
  baseURL: API_BASE
})

/* ---------------- TOKEN INTERCEPTOR ---------------- */

api.interceptors.request.use((config) => {

  const token = localStorage.getItem("token")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config

})

/* ---------------- AUTH APIs ---------------- */

export const authApi = {

  login: (email: string, password: string) =>
    api.post("/api/auth/login", { email, password }),

  register: (data: any) =>
    api.post("/api/auth/register", data),

  getProfile: () =>
    api.get("/api/auth/me")

}

/* ---------------- AI CHAT API ---------------- */

export const chatApi = async (message: string) => {

  const res = await api.post("/api/ai/chat", {
    message
  })

  return res.data

}

export default api
import axios from "axios"

export const fetchDashboardStats = async () => {

  const token = localStorage.getItem("token")

  const response = await axios.get(
    "http://localhost:5173/api/dashboard",
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  return response.data

}
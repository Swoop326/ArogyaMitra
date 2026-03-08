import axios from "axios"

export const fetchDashboardStats = async () => {

  const token = localStorage.getItem("token")

  const response = await axios.get(
    "https://1560-103-97-104-149.ngrok-free.app/api/dashboard",
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  return response.data

}
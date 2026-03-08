import { Navigate } from "react-router-dom"
import { useAuthStore } from "../../stores/authStore"

function ProtectedRoute({ children }: any) {

  const user = useAuthStore((state) => state.user)

  if (!user) {
    return <Navigate to="/login" />
  }

  return children
}

export default ProtectedRoute
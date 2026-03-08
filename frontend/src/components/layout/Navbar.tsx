import { Link, useNavigate } from "react-router-dom"
import { useAuthStore } from "../../stores/authStore"

function Navbar() {

  const navigate = useNavigate()

  const logout = useAuthStore((state) => state.logout)

  const handleLogout = () => {

    logout()

    navigate("/login")

  }

  return (

    <div className="flex justify-between items-center px-10 py-4 bg-slate-800 border-b border-slate-700">

      <h1 className="text-emerald-400 font-bold text-xl">
        ArogyaMitra
      </h1>

      <div className="flex gap-6 items-center">

        <Link to="/dashboard">Dashboard</Link>
        <Link to="/workouts">Workouts</Link>
        <Link to="/nutrition">Nutrition</Link>
        <Link to="/progress">Progress</Link>

        <button
          onClick={handleLogout}
          className="bg-red-500 px-4 py-2 rounded-lg hover:bg-red-600"
        >
          Logout
        </button>

      </div>

    </div>

  )

}

export default Navbar
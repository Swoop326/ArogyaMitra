import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"

import { useAuthStore } from "../../stores/authStore"

function Login() {

  const navigate = useNavigate()

  const login = useAuthStore((state) => state.login)
  const loading = useAuthStore((state) => state.loading)

  const [email,setEmail] = useState("")
  const [password,setPassword] = useState("")
  const [remember,setRemember] = useState(false)
  const [error,setError] = useState("")

  const handleSubmit = async (e:any) => {

  e.preventDefault()

  try{

    await login(email,password)

    console.log("Login successful")

    navigate("/dashboard")

  }
  catch(err:any){

    console.log("Login error:", err)

    if(err.response){
      setError(err.response.data.detail || "Login failed")
    }else{
      setError("Server error. Please try again.")
    }

  }

}
  return (

    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-slate-900 via-slate-950 to-slate-900 text-white px-6">

      {/* Branding */}

      <div className="text-center mb-10">

        <h1 className="text-5xl font-bold text-emerald-400 tracking-wide">
          AROGYAMITRA
        </h1>

        <p className="text-gray-400 mt-3 text-lg">
          AI Powered Fitness Platform
        </p>

      </div>

      {/* Login Card */}

      <motion.div
        initial={{opacity:0, scale:0.95}}
        animate={{opacity:1, scale:1}}
        transition={{duration:0.4}}
        className="w-full max-w-xl bg-slate-800 border border-slate-700 rounded-2xl p-10 shadow-2xl shadow-emerald-500/10"
      >

        <h2 className="text-4xl font-bold text-center mb-3">
          Welcome Back
        </h2>

        <p className="text-gray-400 text-center text-lg mb-8">
          Login to your ArogyaMitra account
        </p>

        <form onSubmit={handleSubmit}>

          {/* Email */}

          <div className="mb-6">

            <label className="text-gray-300 text-sm">
              Email
            </label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
              required
              className="w-full mt-2 p-4 text-lg bg-slate-700 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500"
            />

          </div>

          {/* Password */}

          <div className="mb-6">

            <label className="text-gray-300 text-sm">
              Password
            </label>

            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
              required
              className="w-full mt-2 p-4 text-lg bg-slate-700 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500"
            />

          </div>

          {/* Remember + Forgot */}

          <div className="flex justify-between items-center mb-8 text-sm">

            <label className="flex items-center gap-2 text-gray-400">

              <input
                type="checkbox"
                checked={remember}
                onChange={()=>setRemember(!remember)}
              />

              Remember me

            </label>

            <button
              type="button"
              className="text-emerald-400 hover:underline"
            >
              Forgot password?
            </button>

          </div>

          {/* Error */}

          {error && (
            <p className="text-red-400 mb-4">
              {error}
            </p>
          )}

          {/* Login Button */}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-emerald-500 py-4 text-lg font-semibold rounded-lg hover:bg-emerald-600 transition"
          >

            {loading ? "Logging in..." : "Login"}

          </button>

        </form>

        {/* Register */}

        <p className="text-center text-gray-400 mt-8 text-lg">

          Don't have an account?{" "}

          <Link
            to="/register"
            className="text-emerald-400 hover:underline"
          >
            Register
          </Link>

        </p>

      </motion.div>

    </div>
  )

}

export default Login
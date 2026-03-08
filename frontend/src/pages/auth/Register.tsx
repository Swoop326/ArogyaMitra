import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import axios from "axios";
import { motion } from "framer-motion";

function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async (e: any) => {
    e.preventDefault();

    try {
      await axios.post(
        "http://localhost:5173/api/auth/register",
        {
          name,
          email,
          password,
          age,
          gender,
        },
      );

      alert("Account created successfully");

      navigate("/login");
    } catch (err) {
      setError("Registration failed");
    }
  };

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

      {/* Register Card */}

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-xl bg-slate-800 border border-slate-700 rounded-2xl p-10 shadow-2xl shadow-emerald-500/10"
      >
        <h2 className="text-4xl font-bold text-center mb-3">Create Account</h2>

        <p className="text-gray-400 text-center text-lg mb-8">
          Register to start your fitness journey
        </p>

        <form onSubmit={handleRegister}>
          {/* Name */}

          <div className="mb-5">
            <label className="text-gray-300 text-sm">Full Name</label>

            <input
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full mt-2 p-4 text-lg bg-slate-700 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500"
            />
          </div>

          {/* Email */}

          <div className="mb-5">
            <label className="text-gray-300 text-sm">Email</label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full mt-2 p-4 text-lg bg-slate-700 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500"
            />
          </div>

          {/* Password */}

          <div className="mb-5">
            <label className="text-gray-300 text-sm">Password</label>

            <input
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full mt-2 p-4 text-lg bg-slate-700 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500"
            />
          </div>

          {/* Age */}

          <div className="mb-5">
            <label className="text-gray-300 text-sm">Age</label>

            <input
              type="number"
              placeholder="Enter your age"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              className="w-full mt-2 p-4 text-lg bg-slate-700 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500"
            />
          </div>

          {/* Gender */}

          <div className="mb-6">
            <label className="text-gray-300 text-sm">Gender</label>

            <select
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              className="w-full mt-2 p-4 text-lg bg-slate-700 rounded-lg border border-slate-600 focus:outline-none focus:border-emerald-500"
            >
              <option value="">Select gender</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>

          {/* Error */}

          {error && <p className="text-red-400 mb-4">{error}</p>}

          {/* Register Button */}

          <button
            type="submit"
            className="w-full bg-emerald-500 py-4 text-lg font-semibold rounded-lg hover:bg-emerald-600 transition"
          >
            Register
          </button>
        </form>

        {/* Login Link */}

        <p className="text-center text-gray-400 mt-8 text-lg">
          Already have an account?{" "}
          <Link to="/login" className="text-emerald-400 hover:underline">
            Login
          </Link>
        </p>
      </motion.div>
    </div>
  );
}

export default Register;

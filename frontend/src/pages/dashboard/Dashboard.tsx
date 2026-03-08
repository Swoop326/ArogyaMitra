import { motion } from "framer-motion"
import { useEffect, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"

import Navbar from "../../components/layout/Navbar"

import StatCard from "../../components/ui/StatCard"
import ProgressRing from "../../components/ui/ProgressRing"
import WeeklyActivity from "../../components/ui/WeeklyActivity"

import { useFitnessStore } from "../../stores/fitnessStore"
import { fetchDashboardStats } from "../../services/dashboardApi"
import api from "../../services/api"

interface WeeklyActivityItem {
  day: string
  value: number
}

interface DashboardStats {
  calories: number
  streak: number
  steps: number
  activeMinutes: number
  charityImpact: number

  weightProgress: number
  cardioProgress: number
  strengthProgress: number

  weeklyActivity: WeeklyActivityItem[]
}

function Dashboard() {

  const navigate = useNavigate()

  const updateCalories = useFitnessStore((state) => state.updateCalories)
  const updateSteps = useFitnessStore((state) => state.updateSteps)

  const [showHealthPopup, setShowHealthPopup] = useState(false)

  /* Greeting */

  const hour = new Date().getHours()

  let greeting = "Good Evening"

  if (hour < 12) greeting = "Good Morning"
  else if (hour < 17) greeting = "Good Afternoon"
  else if (hour < 21) greeting = "Good Evening"
  else greeting = "Good Night"

  /* Safe user */

  let user = { name: "User" }

  try {

    const storedUser = localStorage.getItem("user")

    if (storedUser) {
      user = JSON.parse(storedUser)
    }

  } catch {

    console.log("Invalid user JSON")

  }

  /* Dashboard API */

  const { data, isLoading, isError } = useQuery<DashboardStats>({
    queryKey: ["dashboardStats"],
    queryFn: fetchDashboardStats,
    refetchInterval: 30000
  })

  useEffect(() => {

    if (data) {

      updateCalories(data.calories)
      updateSteps(data.steps)

    }

  }, [data, updateCalories, updateSteps])

  /* -------------------------
     CHECK HEALTH PROFILE
  --------------------------*/

  useEffect(() => {

    const checkHealthProfile = async () => {

      try {

        const res = await api.get("/api/health/profile")

        if (!res.data.profile_completed) {

          setShowHealthPopup(true)

        }

      } catch (err) {

        console.log("Health profile check failed")

      }

    }

    checkHealthProfile()

  }, [])

  /* Start Workout */

  const startTodayWorkout = async () => {

  try {

    const res = await api.get("/api/workouts/today")

    const today = res.data

    navigate(`/exercise/${today.day}/0`)

  } catch (err) {

    console.log(err)
    alert("Unable to start today's workout")

  }

}

  

  /* Go to Health Assessment */

  const goToHealthAssessment = () => {

    setShowHealthPopup(false)

    navigate("/health-assessment")

  }

  /* Loading */

  if (isLoading) {

    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-900 text-white">
        Loading dashboard...
      </div>
    )

  }

  /* Error */

  if (isError || !data) {

    return (
      <div className="flex items-center justify-center min-h-screen bg-slate-900 text-red-400">
        Failed to load dashboard
      </div>
    )

  }

  return (

    <div className="min-h-screen bg-slate-900 text-white">

      <Navbar />

      <div className="p-10">

        {/* Greeting Banner */}

        <motion.div
          initial={{ opacity: 0, y: -40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="bg-gradient-to-r from-emerald-600 to-teal-500 rounded-2xl p-10 mb-12 shadow-lg"
        >

          <p className="text-md text-green-100">
            {greeting} 🌿
          </p>

          <h1 className="text-4xl font-bold mt-3 leading-snug">

            {user?.name ? `${user.name}` : "User"}, you're on a{" "}

            <span className="text-green-200">
              {data.streak}-day streak!
            </span>

          </h1>

          <p className="text-green-100 mt-3 text-lg">
            Your body weight goal is {data.weightProgress}% complete.
            Keep going!
          </p>

          <div className="mt-6 flex gap-4">

            <button
              onClick={startTodayWorkout}
              className="bg-white text-teal-700 px-5 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
            >
              Start Today's Workout
            </button>

            <button
              onClick={() => navigate("/workouts")}
              className="border border-white px-5 py-3 rounded-lg hover:bg-white hover:text-teal-700 transition"
            >
              View Plan
            </button>

            <button
              onClick={() => navigate("/health-assessment")}
              className="bg-emerald-700 px-5 py-3 rounded-lg font-semibold hover:bg-emerald-800 transition"
            >
              Take Health Assessment
            </button>

          </div>

        </motion.div>

        {/* Stats */}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 mb-12">

          <StatCard
            title="Calories Burned"
            value={data.calories.toLocaleString()}
            subtitle="Today"
          />

          <StatCard
            title="Workout Streak"
            value={data.streak.toString()}
            subtitle="Days in a row 🔥"
          />

          <StatCard
            title="Steps Today"
            value={data.steps.toLocaleString()}
            subtitle="Goal 10,000"
          />

          <StatCard
            title="Active Minutes"
            value={data.activeMinutes.toString()}
            subtitle="This week"
          />

        </div>

        {/* Weekly Activity */}

        <div className="grid lg:grid-cols-2 gap-8 mb-12">

          <div className="bg-slate-800 border border-slate-700 rounded-xl p-8">

            <h2 className="text-xl font-semibold mb-6">
              Weekly Activity
            </h2>

            <WeeklyActivity data={data.weeklyActivity} />

          </div>

          <div className="bg-slate-800 border border-slate-700 rounded-xl p-6">

            <h2 className="text-xl font-semibold mb-8 text-center">
              Goal Progress
            </h2>

            <div className="flex justify-center gap-16">

              <ProgressRing
                progress={data.weightProgress}
                label="Weight Goal"
                color="#10b981"
              />

              <ProgressRing
                progress={data.cardioProgress}
                label="Cardio"
                color="#3b82f6"
              />

              <ProgressRing
                progress={data.strengthProgress}
                label="Strength"
                color="#a855f7"
              />

            </div>

          </div>

        </div>

        {/* Charity Impact */}

        <div className="bg-slate-800 border border-slate-700 rounded-xl p-8">

          <h2 className="text-xl font-semibold mb-3">
            Charity Impact
          </h2>

          <p className="text-gray-400 text-md">

            Through your workouts, you have contributed

            <span className="text-emerald-400 font-semibold">
              {" "}₹{data.charityImpact.toLocaleString()}
            </span>

            to health charities.

          </p>

        </div>

      </div>

      {/* HEALTH ASSESSMENT POPUP */}

      {showHealthPopup && (

        <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">

          <div className="bg-slate-800 p-8 rounded-xl border border-slate-700 w-[400px] text-center">

            <h2 className="text-2xl font-bold mb-4 text-emerald-400">
              Complete Health Assessment
            </h2>

            <p className="text-gray-300 mb-6">
              Before you begin your workout and nutrition journey,
              please complete your Health Assessment.
            </p>

            <button
              onClick={goToHealthAssessment}
              className="bg-emerald-500 px-6 py-3 rounded-lg font-semibold hover:bg-emerald-600"
            >
              Go to Health Assessment
            </button>

          </div>

        </div>

      )}

    </div>

  )

}

export default Dashboard
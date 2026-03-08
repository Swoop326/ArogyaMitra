import React, { useState, useMemo, useEffect } from "react"
import { motion } from "framer-motion"
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar
} from "recharts"

import Navbar from "../../components/layout/Navbar"
import BackgroundImage from "../../components/layout/BackgroundImage"
import StatCard from "../../components/ui/StatCard"
import api from "../../services/api"

interface Achievement {
  title: string
  description: string
  earned: boolean
}

const ProgressTracking: React.FC = () => {

  const [selectedPeriod,setSelectedPeriod] = useState<
    "week"|"month"|"3months"|"year"
  >("week")

  const [activeTab,setActiveTab] = useState<
    "workouts"|"nutrition"|"body"|"achievements"
  >("workouts")

  const [loading,setLoading] = useState(false)

  /* OVERVIEW */

  const [workoutCount,setWorkoutCount] = useState(0)
  const [caloriesBurned,setCaloriesBurned] = useState(0)
  const [mealTracked,setMealTracked] = useState(0)

  /* CHART DATA */

  const [workoutData,setWorkoutData] = useState<any[]>([])
  const [caloriesData,setCaloriesData] = useState<any[]>([])

  /* ACHIEVEMENTS */

  const [achievements,setAchievements] = useState<Achievement[]>([])

  /* BODY */

  const [height,setHeight] = useState(170)
  const [weight,setWeight] = useState(70)

  /* BMI */

  const bmi = useMemo(()=>{

    const h = height / 100
    if(!h) return 0

    return Number((weight/(h*h)).toFixed(1))

  },[height,weight])

  const bmiCategory = useMemo(()=>{

    if(bmi<18.5) return "Underweight"
    if(bmi<25) return "Healthy"
    if(bmi<30) return "Overweight"

    return "Obese"

  },[bmi])

  /* FETCH OVERVIEW */

  const fetchOverview = async ()=>{

    try{

      const res = await api.get(`/api/progress/overview?range=${selectedPeriod}`)

      setWorkoutCount(res.data?.workouts_completed ?? 0)
      setCaloriesBurned(res.data?.calories_burned ?? 0)
      setMealTracked(res.data?.meals_tracked ?? 0)

    }catch(err){

      console.log("overview error",err)

    }

  }

  /* FETCH WORKOUT CHART */

  const fetchWorkouts = async ()=>{

    try{

      const res = await api.get(`/api/progress/workouts?range=${selectedPeriod}`)

      setWorkoutData(res.data ?? [])

    }catch(err){

      console.log("workout chart error",err)

    }

  }

  /* FETCH CALORIES */

  const fetchCalories = async ()=>{

    try{

      const res = await api.get(`/api/progress/calories?range=${selectedPeriod}`)

      setCaloriesData(res.data ?? [])

    }catch(err){

      console.log("calories error",err)

    }

  }

  /* FETCH ACHIEVEMENTS */

  const fetchAchievements = async ()=>{

    try{

      const res = await api.get("/api/progress/achievements")

      setAchievements(res.data ?? [])

    }catch{

      console.log("Achievements API missing")
      setAchievements([])

    }

  }

  /* FETCH BODY */

  const fetchBody = async ()=>{

    try{

      const res = await api.get("/api/progress/body")

      setHeight(res.data?.height ?? 170)
      setWeight(res.data?.weight ?? 70)

    }catch{

      console.log("No body data")

    }

  }

  /* SAVE BODY */

  const saveMetrics = async ()=>{

    try{

      setLoading(true)

      await api.post("/api/progress/body",{
        height,
        weight,
        bmi
      })

      alert("Body metrics saved")

    }catch{

      alert("Save failed")

    }finally{

      setLoading(false)

    }

  }

  /* LOAD DATA */

  useEffect(()=>{

    fetchOverview()
    fetchWorkouts()
    fetchCalories()
    fetchAchievements()

  },[selectedPeriod])

  useEffect(()=>{

    fetchBody()

  },[])

  return(

    <div className="min-h-screen bg-slate-900 text-white">

      <BackgroundImage/>
      <Navbar/>

      <div className="max-w-[1200px] mx-auto py-12 px-8">

        <h1 className="text-4xl font-bold mb-10 bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
          Progress Tracking
        </h1>

        {/* PERIOD SELECTOR */}

        <div className="flex gap-4 mb-10">

          {["week","month","3months","year"].map(period=>(

            <button
              key={period}
              onClick={()=>setSelectedPeriod(period as any)}
              className={`px-5 py-2 rounded-lg border ${
                selectedPeriod===period
                ? "bg-emerald-500 border-emerald-500"
                : "bg-slate-800 border-slate-700"
              }`}
            >
              {period}
            </button>

          ))}

        </div>

        {/* OVERVIEW CARDS */}

        <div className="grid md:grid-cols-3 gap-6 mb-12">

          <StatCard
            title="Workouts Completed"
            value={String(workoutCount)}
            subtitle="This period"
          />

          <StatCard
            title="Calories Burned"
            value={String(caloriesBurned)}
            subtitle="Total"
          />

          <StatCard
            title="Meals Tracked"
            value={String(mealTracked)}
            subtitle="Nutrition consistency"
          />

        </div>

        {/* TAB NAVIGATION */}

        <div className="flex gap-6 mb-10 text-gray-400">

          {["workouts","nutrition","body","achievements"].map(tab=>(

            <button
              key={tab}
              onClick={()=>setActiveTab(tab as any)}
              className={`capitalize ${
                activeTab===tab ? "text-emerald-400" : ""
              }`}
            >
              {tab}
            </button>

          ))}

        </div>

        {/* WORKOUT CHART */}

        {activeTab==="workouts" && (

          <motion.div
            initial={{opacity:0}}
            animate={{opacity:1}}
            className="bg-slate-800 p-6 rounded-xl border border-slate-700 mb-10"
          >

            <h2 className="text-xl font-semibold mb-6">
              Workout Frequency
            </h2>

            <ResponsiveContainer width="100%" height={300}>

              <BarChart data={workoutData}>
                <XAxis dataKey="day"/>
                <YAxis/>
                <Tooltip/>
                <Bar dataKey="workouts" fill="#10b981"/>
              </BarChart>

            </ResponsiveContainer>

          </motion.div>

        )}

        {/* CALORIES CHART */}

        {activeTab==="nutrition" && (

          <motion.div
            initial={{opacity:0}}
            animate={{opacity:1}}
            className="bg-slate-800 p-6 rounded-xl border border-slate-700 mb-10"
          >

            <h2 className="text-xl font-semibold mb-6">
              Calories Burned Trend
            </h2>

            <ResponsiveContainer width="100%" height={300}>

              <LineChart data={caloriesData}>
                <XAxis dataKey="week"/>
                <YAxis/>
                <Tooltip/>

                <Line
                  type="monotone"
                  dataKey="calories"
                  stroke="#10b981"
                  strokeWidth={3}
                />

              </LineChart>

            </ResponsiveContainer>

          </motion.div>

        )}

        {/* BODY */}

        {activeTab==="body" && (

          <motion.div
            initial={{opacity:0}}
            animate={{opacity:1}}
            className="grid md:grid-cols-2 gap-6"
          >

            <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">

              <h2 className="text-lg mb-4 font-semibold">
                Body Metrics Input
              </h2>

              <div className="space-y-4">

                <input
                  type="number"
                  value={height}
                  onChange={(e)=>setHeight(Number(e.target.value))}
                  className="w-full p-3 bg-slate-700 rounded-lg"
                />

                <input
                  type="number"
                  value={weight}
                  onChange={(e)=>setWeight(Number(e.target.value))}
                  className="w-full p-3 bg-slate-700 rounded-lg"
                />

                <button
                  onClick={saveMetrics}
                  disabled={loading}
                  className="w-full bg-emerald-500 py-3 rounded-lg hover:bg-emerald-600"
                >
                  {loading ? "Saving..." : "Save Metrics"}
                </button>

              </div>

            </div>

            <div className="grid grid-cols-2 gap-4">

              <StatCard title="BMI" value={String(bmi)} subtitle={bmiCategory}/>
              <StatCard title="Weight" value={`${weight} kg`} subtitle="Current"/>
              <StatCard title="Height" value={`${height} cm`} subtitle="Body"/>
              <StatCard title="Status" value={bmiCategory} subtitle="Health"/>

            </div>

          </motion.div>

        )}

        {/* ACHIEVEMENTS */}

        {activeTab==="achievements" && (

          <motion.div
            initial={{opacity:0}}
            animate={{opacity:1}}
            className="grid md:grid-cols-2 gap-6"
          >

            {achievements.length===0 ? (

              <p className="text-gray-400">
                No achievements yet
              </p>

            ) : (

              achievements.map((ach,index)=>(

                <div
                  key={index}
                  className={`p-6 rounded-xl border ${
                    ach.earned
                    ? "bg-emerald-900 border-emerald-500"
                    : "bg-slate-800 border-slate-700"
                  }`}
                >

                  <h3 className="text-lg font-semibold mb-2">
                    {ach.title}
                  </h3>

                  <p className="text-gray-400 text-sm mb-2">
                    {ach.description}
                  </p>

                  <span
                    className={`text-sm font-semibold ${
                      ach.earned
                      ? "text-emerald-400"
                      : "text-gray-500"
                    }`}
                  >
                    {ach.earned ? "Unlocked 🎉" : "Locked 🔒"}
                  </span>

                </div>

              ))

            )}

          </motion.div>

        )}

      </div>

    </div>

  )

}

export default ProgressTracking
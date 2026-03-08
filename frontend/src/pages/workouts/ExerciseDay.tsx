import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"
import { motion } from "framer-motion"

import Navbar from "../../components/layout/Navbar"
import api from "../../services/api"

interface Exercise {
  name: string
  sets: number
  reps: number
  rest?: string
}

function WorkoutDay() {

  const navigate = useNavigate()

  const { day } = useParams()

  const [exercises, setExercises] = useState<Exercise[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  useEffect(() => {

    const fetchExercises = async () => {

      try {

        const res = await api.get(`/api/workouts/exercise/day/${day}`)

        setExercises(res.data)

      } catch {

        setError(true)

      } finally {

        setLoading(false)

      }

    }

    fetchExercises()

  }, [day])

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
        Loading exercises...
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-red-400">
        Failed to load exercises
      </div>
    )
  }

  return (

    <div className="min-h-screen bg-slate-900 text-white">

      <Navbar />

      <div className="max-w-4xl mx-auto p-10">

        <h1 className="text-4xl font-bold mb-10 text-emerald-400">
          Day {day} Workout
        </h1>

        <div className="space-y-6">

          {exercises.map((exercise, index) => (

            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-slate-800 border border-slate-700 rounded-xl p-6 flex justify-between items-center"
            >

              <div>

                <h3 className="text-lg font-semibold">
                  {exercise.name}
                </h3>

                <p className="text-gray-400 text-sm">
                  {exercise.sets} sets • {exercise.reps} reps
                </p>

              </div>

              <button
                onClick={() => navigate(`/exercise/${day}/${index}`)}
                className="bg-emerald-500 px-6 py-2 rounded-lg hover:bg-emerald-600 transition"
              >
                Start
              </button>

            </motion.div>

          ))}

        </div>

      </div>

    </div>

  )

}

export default WorkoutDay
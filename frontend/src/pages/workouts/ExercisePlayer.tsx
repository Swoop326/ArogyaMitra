import { useEffect, useState } from "react"
import { useParams, useNavigate } from "react-router-dom"
import { motion } from "framer-motion"

import Navbar from "../../components/layout/Navbar"
import api from "../../services/api"

interface Exercise {
  name: string
  sets: number
  reps: number
  rest?: string
  video?: string
  exercise_index: number
  total_exercises: number
}

function ExercisePlayer() {

  const { day, exerciseIndex } = useParams()

  const navigate = useNavigate()

  const [exercise, setExercise] = useState<Exercise | null>(null)
  const [loading, setLoading] = useState(true)
  const [completed, setCompleted] = useState(false)
  const [error, setError] = useState("")

  const dayNumber = Number(day)
  const indexNumber = Number(exerciseIndex)

  /* ---------------- LOAD EXERCISE ---------------- */

  useEffect(() => {

    async function loadExercise() {

      try {

        setLoading(true)

        const res = await api.get(
          `/api/workouts/exercise/${dayNumber}/${indexNumber}`
        )

        setExercise(res.data)

      } catch (err) {

        console.error(err)
        setError("Exercise not found")

      } finally {

        setLoading(false)

      }

    }

    if (!isNaN(dayNumber) && !isNaN(indexNumber)) {
      loadExercise()
    }

  }, [dayNumber, indexNumber])

  /* ---------------- NEXT EXERCISE ---------------- */

  const nextExercise = () => {

    if (!exercise) return

    const nextIndex = indexNumber + 1

    if (nextIndex < exercise.total_exercises) {

      navigate(`/exercise/${dayNumber}/${nextIndex}`)

    } else {

      alert("All exercises finished. Click Complete Workout!")

    }

  }

  /* ---------------- COMPLETE WORKOUT ---------------- */

  const completeWorkout = async () => {

    if (completed) return

    try {

      await api.post(`/api/workouts/complete-day/${dayNumber}`)

      setCompleted(true)

      alert("Workout completed!")

      /* get next workout day */

      const res = await api.get("/api/workouts/today")

      console.log("Next workout day:", res.data.day)

      navigate("/dashboard")

    } catch (err) {

      console.error(err)
      alert("Failed to complete workout")

    }

  }

  /* ---------------- LOADING ---------------- */

  if (loading) {

    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-white">
        Loading exercise...
      </div>
    )

  }

  /* ---------------- ERROR ---------------- */

  if (error || !exercise) {

    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900 text-red-400">
        {error}
      </div>
    )

  }

  /* ---------------- UI ---------------- */

  return (

    <div className="min-h-screen bg-slate-900 text-white">

      <Navbar />

      <div className="max-w-[900px] mx-auto p-10">

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-slate-800 border border-slate-700 rounded-xl p-8"
        >

          {/* Title */}

          <h1 className="text-3xl font-bold text-emerald-400 mb-6">
            Day {dayNumber} Workout
          </h1>

          {/* Exercise Name */}

          <h2 className="text-2xl font-semibold mb-3">
            {exercise.name}
          </h2>

          {/* Sets + Reps */}

          <p className="text-gray-400 mb-6">
            {exercise.sets} sets • {exercise.reps} reps
          </p>

          {/* Video */}

          {exercise.video && (

            <div className="aspect-video mb-6">

              <iframe
                src={exercise.video}
                className="w-full h-full rounded-lg"
                allowFullScreen
              />

            </div>

          )}

          {/* Buttons */}

          <div className="flex gap-4 flex-wrap">

            <button
              onClick={nextExercise}
              className="bg-blue-500 px-6 py-3 rounded-lg font-semibold hover:bg-blue-600"
            >
              Next Exercise
            </button>

            <button
              disabled={completed}
              onClick={completeWorkout}
              className={`px-6 py-3 rounded-lg font-semibold ${
                completed
                  ? "bg-gray-600 cursor-not-allowed"
                  : "bg-emerald-500 hover:bg-emerald-600"
              }`}
            >

              {completed ? "Workout Completed" : "Complete Workout"}

            </button>

          </div>

        </motion.div>

      </div>

    </div>

  )

}

export default ExercisePlayer
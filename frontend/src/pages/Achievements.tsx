import { Trophy } from "lucide-react"

const Achievements = () => {

  const achievements = [
    "7 Day Workout Streak",
    "First 5000 Calories Burned",
    "Completed 20 Workouts",
    "Tracked Meals for 7 Days"
  ]

  return (
    <div className="grid md:grid-cols-2 gap-6">

      {achievements.map((a, index) => (

        <div
          key={index}
          className="bg-slate-800 border border-slate-700 p-6 rounded-xl flex items-center gap-4"
        >
          <Trophy className="text-emerald-400" />

          <p className="text-lg">
            {a}
          </p>

        </div>

      ))}

    </div>
  )
}

export default Achievements
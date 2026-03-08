import { Trophy } from "lucide-react"

function Achievements() {
  const achievements = [
    "7 Day Workout Streak",
    "10000 Calories Burned",
    "30 Workouts Completed",
    "First Health Assessment"
  ]

  return (
    <div className="grid md:grid-cols-2 gap-6">

      {achievements.map((a, index) => (

        <div
          key={index}
          className="bg-slate-800 p-6 rounded-xl border border-slate-700 flex items-center gap-4"
        >
          <Trophy className="text-emerald-400" />
          <p>{a}</p>
        </div>

      ))}

    </div>
  )
}

export default Achievements
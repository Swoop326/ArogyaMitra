import { useState } from "react";
import { motion } from "framer-motion";
import Navbar from "../../components/layout/Navbar";
import api from "../../services/api";

interface Exercise {
  name: string;
  sets: number;
  reps: number | string;
  rest: string;
  difficulty: string;
}

interface WorkoutDay {
  day: string;
  workout: string;
  exercises: Exercise[];
}

function WorkoutPlans() {

  const [goal, setGoal] = useState("weight-loss");
  const [level, setLevel] = useState("beginner");
  const [days, setDays] = useState(3);

  const [plan, setPlan] = useState<WorkoutDay[]>([]);
  const [loading, setLoading] = useState(false);

  const generatePlan = async () => {

    try{

      setLoading(true);

      const res = await api.post("/api/workouts/plan",{
        goal,
        level,
        days
      });

      setPlan(res.data.plan);

    }catch(err){

      console.error("Failed to generate workout plan");

    }finally{

      setLoading(false);

    }

  };

  return (

    <div className="min-h-screen bg-slate-900 text-white">

      {/* Navbar */}
      <Navbar/>

      <div className="px-16 py-10">

        {/* Page Heading */}

        <h1 className="text-4xl font-bold mb-10 text-emerald-400 tracking-tight">
          AI Workout Planner
        </h1>

        {/* Planner Form */}

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="bg-slate-800 p-8 rounded-xl border border-slate-700 mb-12"
        >

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

            {/* Goal */}

            <div>

              <label className="text-gray-300 text-base font-medium">
                Fitness Goal
              </label>

              <select
                className="w-full mt-2 bg-slate-700 p-4 rounded-lg text-lg"
                value={goal}
                onChange={(e) => setGoal(e.target.value)}
              >
                <option value="weight-loss">Weight Loss</option>
                <option value="muscle-gain">Muscle Gain</option>
                <option value="endurance">Endurance</option>
              </select>

            </div>

            {/* Level */}

            <div>

              <label className="text-gray-300 text-base font-medium">
                Experience Level
              </label>

              <select
                className="w-full mt-2 bg-slate-700 p-4 rounded-lg text-lg"
                value={level}
                onChange={(e) => setLevel(e.target.value)}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>

            </div>

            {/* Days */}

            <div>

              <label className="text-gray-300 text-base font-medium">
                Workout Days / Week
              </label>

              <input
                type="number"
                min="1"
                max="7"
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
                className="w-full mt-2 bg-slate-700 p-4 rounded-lg text-lg"
              />

            </div>

          </div>

          <button
            onClick={generatePlan}
            className="mt-6 bg-emerald-500 px-8 py-3 rounded-xl font-semibold text-lg hover:bg-emerald-600 transition"
          >

            {loading ? "Generating..." : "Generate Workout Plan"}

          </button>

        </motion.div>

        {/* Workout Plan Cards */}

        {plan.length > 0 && (

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-10">

            {plan.map((dayPlan, index) => (

              <motion.div
                key={index}
                whileHover={{ scale: 1.03 }}
                className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-md hover:shadow-emerald-500/20 transition"
              >

                <h3 className="text-lg font-semibold text-white mb-1">
                  {dayPlan.day}
                </h3>

                <p className="text-emerald-400 font-medium mb-4">
                  {dayPlan.workout}
                </p>

                <div className="space-y-3">

                  {dayPlan.exercises.map((exercise, i) => (

                    <div
                      key={i}
                      className="bg-slate-700/80 p-4 rounded-lg hover:bg-slate-600 transition"
                    >

                      <p className="font-semibold text-white">
                        {exercise.name}
                      </p>

                      <div className="text-sm text-gray-300 mt-1">
                        Sets: {exercise.sets} | Reps: {exercise.reps}
                      </div>

                      <div className="text-sm text-gray-400">
                        Rest: {exercise.rest} | Difficulty: {exercise.difficulty}
                      </div>

                    </div>

                  ))}

                </div>

              </motion.div>

            ))}

          </div>

        )}

      </div>

    </div>

  );
}

export default WorkoutPlans;
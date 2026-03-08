import React, { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"

import {
  Calendar,
  Clock,
  ShoppingCart,
  Target,
  CheckCircle
} from "lucide-react"

import { toast } from "react-hot-toast"

import Navbar from "../../components/layout/Navbar"
import BackgroundImage from "../../components/layout/BackgroundImage"
import api from "../../services/api"

interface Meal {
  name: string
  recipe_id: number | null
  image: string
}

interface WeekDay {
  day: string
  meals: Meal[]
}

interface Macros {
  protein: string
  carbs: string
  fats: string
}

interface RecipeDetail {
  title: string
  image: string
  ingredients: string[]
  instructions: string
}

const mealMeta = [
  { type: "Breakfast", time: "8:00 AM" },
  { type: "Lunch", time: "1:00 PM" },
  { type: "Dinner", time: "7:30 PM" }
]

const NutritionPlans: React.FC = () => {

  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const [activeTab, setActiveTab] = useState<'today' | 'week' | 'grocery'>('today')

  const [healthPlan, setHealthPlan] = useState({
    calories: 2000,
    diet: "vegetarian",
    allergies: ""
  })

  const [loading, setLoading] = useState(false)

  const [macros, setMacros] = useState<Macros | null>(null)
  const [weeklyPlan, setWeeklyPlan] = useState<WeekDay[]>([])
  const [groceryList, setGroceryList] = useState<string[]>([])

  const [recipeDetail, setRecipeDetail] = useState<RecipeDetail | null>(null)
  const [showRecipe, setShowRecipe] = useState(false)

  const [completedMeals, setCompletedMeals] = useState<{ [key: string]: boolean }>({})

  /* ---------- Generate Nutrition Plan ---------- */

  const generatePlan = async () => {

    try {

      setLoading(true)

      const res = await api.post("/api/nutrition/plan", {
        calories: healthPlan.calories,
        diet: healthPlan.diet,
        allergies: healthPlan.allergies
      })

      const data = res.data

      setMacros(data.macros || null)
      setWeeklyPlan(data.weeklyPlan || [])
      setGroceryList(data.groceryList || [])

      toast.success("Nutrition plan generated!")

    } catch {

      toast.error("Failed to generate nutrition plan")

    } finally {

      setLoading(false)

    }

  }

  /* ---------- Open Recipe Modal ---------- */

  const openRecipe = async (recipe_id: number | null) => {

    if (!recipe_id) {
      toast("Recipe not available for this meal")
      return
    }

    try {

      const res = await api.get(`/api/nutrition/recipe/${recipe_id}`)

      setRecipeDetail(res.data)
      setShowRecipe(true)

    } catch {

      toast.error("Failed to load recipe")

    }

  }

  const toggleMeal = (mealName: string) => {

    setCompletedMeals(prev => ({
      ...prev,
      [mealName]: !prev[mealName]
    }))

    toast.success("Meal marked completed!")

    queryClient.invalidateQueries({
      queryKey: ["nutrition-progress"]
    })

  }

  const goToDashboard = () => navigate("/dashboard")

  const todayName = new Date().toLocaleDateString("en-US", { weekday: "long" })

  const todayPlan = weeklyPlan.find(
    day => day.day.toLowerCase() === todayName.toLowerCase()
  )

  const todayMeals = todayPlan?.meals || []

  return (

    <div className="min-h-screen bg-slate-900 text-white">

      <BackgroundImage />
      <Navbar />

      <div className="max-w-[1300px] mx-auto px-10 py-12">

        <h1 className="text-4xl font-bold mb-10 bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
          AI Nutrition Planner
        </h1>

        {/* Input Section */}

        <div className="bg-slate-800 p-6 rounded-xl border border-slate-700 mb-6 grid md:grid-cols-3 gap-6">

          <div>
            <label className="text-sm text-gray-400">Daily Calories</label>
            <input
              type="number"
              value={healthPlan.calories}
              onChange={(e) => setHealthPlan({ ...healthPlan, calories: Number(e.target.value) })}
              className="w-full mt-2 p-3 bg-slate-700 rounded-lg"
            />
          </div>

          <div>
            <label className="text-sm text-gray-400">Diet Type</label>
            <select
              value={healthPlan.diet}
              onChange={(e) => setHealthPlan({ ...healthPlan, diet: e.target.value })}
              className="w-full mt-2 p-3 bg-slate-700 rounded-lg"
            >
              <option value="vegetarian">Vegetarian</option>
              <option value="non-veg">Non-Veg</option>
              <option value="vegan">Vegan</option>
            </select>
          </div>

          <div>
            <label className="text-sm text-gray-400">Allergies</label>
            <input
              value={healthPlan.allergies}
              onChange={(e) => setHealthPlan({ ...healthPlan, allergies: e.target.value })}
              className="w-full mt-2 p-3 bg-slate-700 rounded-lg"
            />
          </div>

        </div>

        <button
          onClick={generatePlan}
          className="mb-10 bg-emerald-500 px-8 py-3 rounded-lg hover:bg-emerald-600"
        >
          {loading ? "Generating Plan..." : "Generate Nutrition Plan"}
        </button>

        {/* Tabs */}

        <div className="flex gap-6 mb-8">

          <button onClick={() => setActiveTab("today")} className="flex gap-2">
            <Calendar size={18} /> Today
          </button>

          <button onClick={() => setActiveTab("week")} className="flex gap-2">
            <Target size={18} /> Week Plan
          </button>

          <button onClick={() => setActiveTab("grocery")} className="flex gap-2">
            <ShoppingCart size={18} /> Grocery
          </button>

        </div>

        {/* TODAY */}

        {activeTab === "today" && (

          <div className="grid md:grid-cols-3 gap-6">

            {todayMeals.map((meal, index) => {

              const meta = mealMeta[index] || { type: "Meal", time: "Anytime" }

              return (

                <div
                  key={index}
                  className="bg-slate-800 rounded-xl border border-slate-700 overflow-hidden"
                >

                  <div className="p-6">

                    <h3 className="text-xl font-semibold mb-2">
                      {meal.name}
                    </h3>

                    <p className="text-emerald-400 text-sm mb-2">
                      {meta.type}
                    </p>

                    <p className="text-gray-400 text-sm mb-3">
                      <Clock size={14} className="inline mr-1" />
                      {meta.time}
                    </p>

                    <button
                      onClick={() => toggleMeal(meal.name)}
                      className="flex items-center gap-2 text-sm"
                    >
                      <CheckCircle size={16} />
                      {completedMeals[meal.name] ? "Completed" : "Mark Completed"}
                    </button>

                  </div>

                  <div className="border-t border-slate-700 p-4">

  <button
  type="button"
  onClick={() => openRecipe(meal.recipe_id)}
  className="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-2 rounded-lg cursor-pointer"
>
  View Recipe
</button>

</div>

                </div>

              )

            })}

          </div>

        )}

        {/* WEEK PLAN */}

        {activeTab === "week" && (

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">

            {weeklyPlan.map((day, index) => (

              <div
                key={index}
                className="bg-slate-800 p-6 rounded-xl border border-slate-700"
              >

                <h3 className="text-lg font-semibold mb-3">{day.day}</h3>

                {day.meals.map((meal, i) => (
                  <p key={i} className="text-gray-400">
                    • {meal.name}
                  </p>
                ))}

              </div>

            ))}

          </div>

        )}

        {/* GROCERY */}

        {activeTab === "grocery" && (

          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">

            <h3 className="text-xl font-semibold mb-4">
              Grocery List
            </h3>

            {groceryList.map((item, index) => (
              <p key={index} className="text-gray-400">
                • {item}
              </p>
            ))}

            <button
              onClick={goToDashboard}
              className="mt-6 bg-emerald-500 px-6 py-3 rounded-lg hover:bg-emerald-600"
            >
              Back to Dashboard
            </button>

          </div>

        )}

      </div>

      {/* Recipe Modal */}

      {showRecipe && recipeDetail && (

        <div className="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50">

          <div className="bg-slate-800 max-w-2xl w-full p-8 rounded-xl overflow-y-auto max-h-[80vh]">

            <h2 className="text-2xl font-bold mb-4">
              {recipeDetail.title}
            </h2>

            <img
              src={recipeDetail.image}
              className="w-full h-48 object-cover rounded-lg mb-4"
            />

            <h3 className="font-semibold mb-2">Ingredients</h3>

            <ul className="list-disc list-inside mb-4">
              {recipeDetail.ingredients.map((i, index) => (
                <li key={index}>{i}</li>
              ))}
            </ul>

            <h3 className="font-semibold mb-2">Instructions</h3>

            <p className="whitespace-pre-line">
              {recipeDetail.instructions}
            </p>

            <button
              onClick={() => setShowRecipe(false)}
              className="mt-6 bg-emerald-500 px-6 py-2 rounded-lg"
            >
              Close
            </button>

          </div>

        </div>

      )}

    </div>

  )

}

export default NutritionPlans
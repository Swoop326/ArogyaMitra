import React, { useState } from "react"
import { motion } from "framer-motion"
import { useMutation } from "@tanstack/react-query"
import { toast } from "react-hot-toast"
import { useNavigate } from "react-router-dom"

import Navbar from "../../components/layout/Navbar"
import BackgroundImage from "../../components/layout/BackgroundImage"
import api from "../../services/api"

const HealthAssessment: React.FC = () => {

  const navigate = useNavigate()

  const [formData, setFormData] = useState<any>({
    age: "",
    gender: "",
    height: "",
    weight: "",
    fitness_level: "beginner",
    fitness_goal: ""
  })

  const [answers, setAnswers] = useState<any>({})

  const handleChange = (key: string, value: any) => {

    setFormData((prev: any) => ({
      ...prev,
      [key]: value
    }))

  }

  const handleAnswerChange = (key: string, value: string) => {

    setAnswers((prev: any) => ({
      ...prev,
      [key]: value
    }))

  }

  /* -------------------------
     SUBMIT API
  --------------------------*/

  const submitAssessmentMutation = useMutation({

    mutationFn: async (assessmentData: any) => {

      const res = await api.post(
        "/api/health/assessment",
        assessmentData
      )

      return res.data

    },

    onSuccess: () => {

      toast.success("✅ Health assessment submitted")

      navigate("/dashboard")

    },

    onError: () => {

      toast.error("❌ Failed to submit assessment")

    }

  })

  /* -------------------------
     HANDLE SUBMIT
  --------------------------*/

  const handleSubmit = () => {

    if (
      !formData.age ||
      !formData.gender ||
      !formData.height ||
      !formData.weight ||
      !formData.fitness_goal
    ) {

      toast.error("Please fill all required fields")

      return
    }

    const payload = {

      age: Number(formData.age),
      gender: formData.gender,
      height: Number(formData.height),
      weight: Number(formData.weight),

      fitness_level: formData.fitness_level,
      fitness_goal: formData.fitness_goal,

      medical_history: [
        answers.h1,
        answers.h2,
        answers.h3
      ].filter(Boolean),

      injuries: [
        answers.i1,
        answers.i2,
        answers.i3
      ].filter(Boolean),

      allergies: [
        answers.a1,
        answers.a2
      ].filter(Boolean),

      medications: [
        answers.m1,
        answers.m2
      ].filter(Boolean)

    }

    submitAssessmentMutation.mutate(payload)

  }

  return (

    <div className="min-h-screen bg-slate-900 text-white">

      <BackgroundImage />
      <Navbar />

      <div className="max-w-[900px] mx-auto py-12 px-8">

        <h1 className="text-4xl font-bold mb-10 bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent">
          Health Assessment
        </h1>

        <div className="space-y-6">

          {/* BASIC DETAILS */}

          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">

            <h2 className="text-xl font-semibold mb-4">
              Basic Information
            </h2>

            <input
              type="number"
              placeholder="Age"
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              value={formData.age}
              onChange={(e) => handleChange("age", e.target.value)}
            />

            <select
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              value={formData.gender}
              onChange={(e) => handleChange("gender", e.target.value)}
            >

              <option value="">Select Gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>

            </select>

            <input
              type="number"
              placeholder="Height (cm)"
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              value={formData.height}
              onChange={(e) => handleChange("height", e.target.value)}
            />

            <input
              type="number"
              placeholder="Weight (kg)"
              className="w-full p-3 bg-slate-700 rounded-lg"
              value={formData.weight}
              onChange={(e) => handleChange("weight", e.target.value)}
            />

          </div>

          {/* MEDICAL HISTORY */}

          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">

            <h2 className="text-xl font-semibold mb-4">
              Medical History
            </h2>

            <input
              placeholder="Heart conditions"
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              onChange={(e) => handleAnswerChange("h1", e.target.value)}
            />

            <input
              placeholder="Diabetes"
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              onChange={(e) => handleAnswerChange("h2", e.target.value)}
            />

            <input
              placeholder="Blood pressure"
              className="w-full p-3 bg-slate-700 rounded-lg"
              onChange={(e) => handleAnswerChange("h3", e.target.value)}
            />

          </div>

          {/* INJURIES */}

          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">

            <h2 className="text-xl font-semibold mb-4">
              Past Injuries
            </h2>

            <input
              placeholder="Knee injury"
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              onChange={(e) => handleAnswerChange("i1", e.target.value)}
            />

            <input
              placeholder="Back pain"
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              onChange={(e) => handleAnswerChange("i2", e.target.value)}
            />

            <input
              placeholder="Other injuries"
              className="w-full p-3 bg-slate-700 rounded-lg"
              onChange={(e) => handleAnswerChange("i3", e.target.value)}
            />

          </div>

          {/* ALLERGIES */}

          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">

            <h2 className="text-xl font-semibold mb-4">
              Allergies
            </h2>

            <input
              placeholder="Food allergies"
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              onChange={(e) => handleAnswerChange("a1", e.target.value)}
            />

            <input
              placeholder="Medication allergies"
              className="w-full p-3 bg-slate-700 rounded-lg"
              onChange={(e) => handleAnswerChange("a2", e.target.value)}
            />

          </div>

          {/* MEDICATIONS */}

          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">

            <h2 className="text-xl font-semibold mb-4">
              Medications
            </h2>

            <input
              placeholder="Current medication"
              className="w-full p-3 bg-slate-700 rounded-lg mb-3"
              onChange={(e) => handleAnswerChange("m1", e.target.value)}
            />

            <input
              placeholder="Supplements"
              className="w-full p-3 bg-slate-700 rounded-lg"
              onChange={(e) => handleAnswerChange("m2", e.target.value)}
            />

          </div>

          {/* FITNESS GOAL */}

          <div className="bg-slate-800 p-6 rounded-xl border border-slate-700">

            <h2 className="text-xl font-semibold mb-4">
              Fitness Goal
            </h2>

            <select
              className="w-full p-3 bg-slate-700 rounded-lg"
              value={formData.fitness_goal}
              onChange={(e) => handleChange("fitness_goal", e.target.value)}
            >

              <option value="">Select Goal</option>
              <option value="weight_loss">Weight Loss</option>
              <option value="muscle_gain">Muscle Gain</option>
              <option value="general_fitness">General Fitness</option>
              <option value="endurance">Endurance</option>

            </select>

          </div>

          {/* SUBMIT */}

          <motion.button
            whileHover={{ scale: 1.05 }}
            className="w-full mt-6 bg-emerald-500 py-4 rounded-xl font-semibold text-lg hover:bg-emerald-600"
            onClick={handleSubmit}
          >
            Submit Health Assessment
          </motion.button>

        </div>

      </div>

    </div>

  )

}

export default HealthAssessment
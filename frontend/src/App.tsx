import { Routes, Route, Navigate } from "react-router-dom";

import Dashboard from "./pages/dashboard/Dashboard";
import WorkoutPlans from "./pages/workouts/WorkoutPlans";
import WorkoutDay from "./pages/workouts/WorkoutDay";   // ⭐ ADD THIS
import ExercisePlayer from "./pages/workouts/ExercisePlayer";

import NutritionPlans from "./pages/nutrition/NutritionPlans";
import HealthAssessment from "./pages/assessment/HealthAssessment";
import ProgressTracking from "./pages/progress/ProgressTracking";

import ArogyaCoach from "./components/ArogyaCoach/ArogyaCoach";
import ProtectedRoute from "./components/auth/ProtectedRoute";

import Login from "./pages/auth/Login";
import Register from "./pages/auth/Register";

function App() {

  return (

    <div className="min-h-screen bg-gray-50">

      <Routes>

        {/* Default route */}
        <Route path="/" element={<Navigate to="/login" />} />

        {/* Public Routes */}

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/health-assessment" element={<HealthAssessment />} />

        {/* Protected Routes */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        {/* Workout Plan Generator */}

        <Route
          path="/workouts"
          element={
            <ProtectedRoute>
              <WorkoutPlans />
            </ProtectedRoute>
          }
        />

        {/* ⭐ Workout Day Exercise List */}

        <Route
          path="/workouts/:day"
          element={
            <ProtectedRoute>
              <WorkoutDay />
            </ProtectedRoute>
          }
        />

        {/* ⭐ Exercise Player */}

        <Route
          path="/exercise/:day/:exerciseIndex"
          element={
            <ProtectedRoute>
              <ExercisePlayer />
            </ProtectedRoute>
          }
        />

        {/* Nutrition */}

        <Route
          path="/nutrition"
          element={
            <ProtectedRoute>
              <NutritionPlans />
            </ProtectedRoute>
          }
        />

        {/* Health Assessment */}

        <Route
          path="/assessment"
          element={
            <ProtectedRoute>
              <HealthAssessment />
            </ProtectedRoute>
          }
        />

        {/* Progress */}

        <Route
          path="/progress"
          element={
            <ProtectedRoute>
              <ProgressTracking />
            </ProtectedRoute>
          }
        />

      </Routes>

      {/* Floating AI assistant */}
      <ArogyaCoach />

    </div>

  );

}

export default App;
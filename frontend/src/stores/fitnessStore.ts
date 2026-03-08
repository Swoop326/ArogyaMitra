import { create } from "zustand";

interface FitnessState {
  calories: number;
  streak: number;
  steps: number;
  activeMinutes: number;
  charityImpact: number;

  updateCalories: (value: number) => void;
  updateSteps: (value: number) => void;
}

export const useFitnessStore = create<FitnessState>((set) => ({
  calories: 0,
  streak: 0,
  steps: 0,
  activeMinutes: 0,
  charityImpact: 0,

  updateCalories: (value) =>
    set(() => ({
      calories: value,
    })),

  updateSteps: (value) =>
    set(() => ({
      steps: value,
    })),
}));
import { motion } from "framer-motion";

interface ProgressRingProps {
  progress: number;
  label: string;
  color: string;
}

function ProgressRing({ progress, label, color }: ProgressRingProps) {
  const radius = 45;
  const circumference = 2 * Math.PI * radius;

  const offset = circumference - (progress / 100) * circumference;

  return (
    <div className="flex flex-col items-center">

      <svg width="120" height="120">

        {/* Background circle */}
        <circle
          cx="60"
          cy="60"
          r={radius}
          stroke="#334155"
          strokeWidth="10"
          fill="transparent"
        />

        {/* Animated progress */}
        <motion.circle
          cx="60"
          cy="60"
          r={radius}
          stroke={color}
          strokeWidth="10"
          fill="transparent"
          strokeDasharray={circumference}
          strokeDashoffset={circumference}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1 }}
          strokeLinecap="round"
        />

        {/* Percentage text */}
        <text
          x="50%"
          y="50%"
          textAnchor="middle"
          dy=".3em"
          className="fill-white text-lg font-semibold"
        >
          {progress}%
        </text>

      </svg>

      <p className="text-gray-400 text-sm mt-2">{label}</p>

    </div>
  );
}

export default ProgressRing;
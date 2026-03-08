import { motion } from "framer-motion";

interface StatCardProps {
  title: string;
  value: string;
  subtitle?: string;
}

function StatCard({ title, value, subtitle }: StatCardProps) {
  return (
    <motion.div
      whileHover={{ scale: 1.05 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-slate-800 border border-slate-700 rounded-xl p-6 shadow-md"
    >
      <p className="text-gray-400 text-sm">{title}</p>

      <h2 className="text-3xl font-bold text-white mt-2">
        {value}
      </h2>

      {subtitle && (
        <p className="text-emerald-400 text-sm mt-1">
          {subtitle}
        </p>
      )}
    </motion.div>
  );
}

export default StatCard;
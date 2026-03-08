import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  Tooltip
} from "recharts"

interface WeeklyActivityItem {
  day: string
  value: number
}

function WeeklyActivity({ data }: { data: WeeklyActivityItem[] }) {

  return (

    <ResponsiveContainer width="100%" height={300}>

      <BarChart data={data}>

        <XAxis dataKey="day" />

        <Tooltip />

        <Bar
          dataKey="value"
          fill="#10b981"
          radius={[6,6,0,0]}
        />

      </BarChart>

    </ResponsiveContainer>

  )

}

export default WeeklyActivity
import { MessageCircle } from "lucide-react"

interface Props {
  onClick: () => void
}

const ArogyaCoachButton: React.FC<Props> = ({ onClick }) => {

  return (

    <button
      onClick={onClick}
      className="fixed bottom-6 right-6 bg-emerald-500 p-4 rounded-full shadow-lg hover:bg-emerald-600 z-50"
    >
      <MessageCircle className="text-white" size={24} />
    </button>

  )

}

export default ArogyaCoachButton
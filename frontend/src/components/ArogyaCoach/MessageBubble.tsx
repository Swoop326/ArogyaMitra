import React from "react"

interface Props {
  type: "user" | "aromi"
  content: string
}

const MessageBubble: React.FC<Props> = ({ type, content }) => {

  return (

    <div className={`flex ${type === "user" ? "justify-end" : "justify-start"} mb-3`}>

      <div
        className={`max-w-[75%] px-4 py-2 rounded-xl text-sm ${
          type === "user"
            ? "bg-emerald-500 text-white"
            : "bg-slate-700 text-gray-200"
        }`}
      >
        {content}
      </div>

    </div>

  )

}

export default MessageBubble
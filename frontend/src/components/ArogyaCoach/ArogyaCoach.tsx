import React, { useState, useRef, useEffect } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Send, X } from "lucide-react"

import MessageBubble from "./MessageBubble"
import ArogyaCoachButton from "./ArogyaCoachButton"
import { chatApi } from "../../services/api"

interface Message {
  id: string
  type: "user" | "aromi"
  content: string
}

const ArogyaCoach: React.FC = () => {

  const [isOpen, setIsOpen] = useState(false)

  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      type: "aromi",
      content:
        "🙏 Namaste! I'm AROMI, your personal AI health coach. Ask me about workouts, nutrition, or motivation!"
    }
  ])

  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {

    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setLoading(true)

    try {

      const res = await chatApi(userMessage.content)

      const aiMessage: Message = {
        id: Date.now().toString(),
        type: "aromi",
        content: res.reply || "Sorry, I couldn't respond."
      }

      setMessages((prev) => [...prev, aiMessage])

    } catch {

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now().toString(),
          type: "aromi",
          content: "⚠️ AI service unavailable"
        }
      ])

    }

    setLoading(false)

  }

  return (

    <>
      {!isOpen && <ArogyaCoachButton onClick={() => setIsOpen(true)} />}

      <AnimatePresence>

        {isOpen && (

          <motion.div
            initial={{ opacity: 0, y: 100 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 100 }}
            className="fixed bottom-6 right-6 w-[420px] h-[620px] bg-slate-900 border border-slate-700 rounded-2xl shadow-2xl flex flex-col z-50"
          >

            <div className="flex justify-between items-center p-4 border-b border-slate-700">

              <h2 className="text-emerald-400 font-semibold">
                AROMI AI Coach
              </h2>

              <button onClick={() => setIsOpen(false)}>
                <X size={18} />
              </button>

            </div>

            <div className="flex-1 overflow-y-auto p-5 space-y-2">

              {messages.map((msg) => (
                <MessageBubble
                  key={msg.id}
                  type={msg.type}
                  content={msg.content}
                />
              ))}

              {loading && (
                <p className="text-gray-400 text-sm">
                  AROMI is thinking...
                </p>
              )}

              <div ref={messagesEndRef} />

            </div>

            <div className="flex p-4 border-t border-slate-700 gap-2">

              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask AROMI..."
                className="flex-1 bg-slate-800 px-3 py-2 rounded-lg text-sm outline-none"
              />

              <button
                onClick={sendMessage}
                className="ml-2 bg-emerald-500 p-2 rounded-lg"
              >
                <Send size={18} />
              </button>

            </div>

          </motion.div>

        )}

      </AnimatePresence>
    </>
  )

}

export default ArogyaCoach
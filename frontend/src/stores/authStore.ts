import { create } from "zustand"
import { persist } from "zustand/middleware"
import { authApi } from "../services/api"

interface User {
  id?: number
  username?: string
  email: string
  full_name?: string
  role?: "user" | "admin"
}

interface AuthState {

  user: User | null
  token: string | null
  loading: boolean

  login: (email: string, password: string) => Promise<void>
  logout: () => void

}

export const useAuthStore = create<AuthState>()(

  persist(

    (set) => ({

      user: null,
      token: null,
      loading: false,

      login: async (email, password) => {

        set({ loading: true })

        try {

          const res = await authApi.login(email, password)

          const token = res.data.access_token || res.data.token
          const user = res.data.user || { email }

          // save token for axios interceptor
          localStorage.setItem("token", token)

          set({
            user,
            token,
            loading: false
          })

        } catch (error) {

          set({ loading: false })
          throw error

        }

      },

      logout: () => {

        localStorage.removeItem("token")

        set({
          user: null,
          token: null
        })

      }

    }),

    {
      name: "arogya-auth",

      // persist only what we need
      partialize: (state) => ({
        user: state.user,
        token: state.token
      })
    }

  )

)
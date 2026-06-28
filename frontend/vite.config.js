import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/movies/': 'http://127.0.0.1:8000',
      '/recommend/': 'http://127.0.0.1:8000',
    },
  },
})

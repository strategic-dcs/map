import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/',
  plugins: [react()],
  server: {
    watch: {
      usePolling: true,
    },
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000/",
        rewrite: (path) => path.replace(/^\/api/, ''),
      }
    },
    host: true,
    port: 3000,
  }
})

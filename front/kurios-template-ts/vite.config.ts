import tailwindcss from "@tailwindcss/vite";
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/schools': 'http://localhost:8000',
      '/teachers': 'http://localhost:8000',
      '/visits': 'http://localhost:8000',
    },
  },
})

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  build: {
    lib: {
      entry: 'src/widget.jsx',
      name: 'ChatbotWidget',
      fileName: () => 'widget.js',
      formats: ['iife'], // Needed for <script> tag usage
    },
    rollupOptions: {
      // Keep React bundled for standalone use
      external: [], // do NOT externalize
    },
  },
  define: {
    'process.env.NODE_ENV': JSON.stringify('production'),
    'process.env': {}, // prevent process.env from breaking the build
  },
});

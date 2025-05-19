import react from '@vitejs/plugin-react';
import { dirname, resolve } from 'path';
import { fileURLToPath } from 'url';
import { defineConfig } from 'vite';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default defineConfig({
    plugins: [react()],
    resolve: {
        alias: {
            '@': resolve(__dirname, './src'),
        },
    },
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:8001',
                changeOrigin: true,
                rewrite: path => path.replace(/^\/api/, ''),
            },
            // @todo need to test this with the custom node
            '/canvas-custom-node': {
                target: 'http://localhost:3001',
                changeOrigin: true,
                rewrite: path => path.replace(/^\/canvas-custom-node/, ''),
            },
        },
    },
    optimizeDeps: {
        include: ['@xyflow/react'],
    },
});

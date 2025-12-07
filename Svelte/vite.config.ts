import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		proxy: {
			// Proxy API calls to the FastAPI backend to keep same-origin
			'/api': {
				target: 'http://127.0.0.1:8000',
				changeOrigin: true,
				secure: false,
				rewrite: (path) => path
			}
		}
	}
});

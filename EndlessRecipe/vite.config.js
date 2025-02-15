import scss from 'rollup-plugin-scss';
import autoprefixer from 'autoprefixer';
import { defineConfig } from 'vite';

const basePath = './';

export default defineConfig({
    publicDir: 'wwwroot/dist',
    build: {
        minify: false,
        rollupOptions: {
            input: `/styles/scss/main.scss`,
            output: {
                dir: `wwwroot/dist`,
                entryFileNames: 'css/style.css',
            },
        },
    },
    plugins: [
        scss({
            fileName: 'css/style.css',
            sourceMap: true,
            outputStyle: 'compressed',
            watch: `${basePath}styles/scss`,
            postcss: {
                plugins: [
                    autoprefixer(),
                ],
            },
        }),
    ],
});
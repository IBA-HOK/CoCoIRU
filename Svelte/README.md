# sv

Everything you need to build a Svelte project, powered by [`sv`](https://github.com/sveltejs/cli).

## Creating a project

If you're seeing this, you've probably already done this step. Congrats!

```sh
# create a new project in the current directory
npx sv create

# create a new project in my-app
npx sv create my-app
```

## Developing

Once you've created a project and installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```sh
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

### Login sample route

- Access `http://localhost:5173/login` (default dev port) to open the new login form.
- Set `VITE_API_BASE` in `.env` to point at your FastAPI host (defaults to `http://localhost:8000`).
- The form submits `username` and `password` to `${VITE_API_BASE}/api/v1/token` using the OAuth2 password flow format and shows the returned token.

## Building

To create a production version of your app:

```sh
npm run build
```

You can preview the production build with `npm run preview`.

> To deploy your app, you may need to install an [adapter](https://svelte.dev/docs/kit/adapters) for your target environment.

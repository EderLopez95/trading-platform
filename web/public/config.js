// Runtime configuration. This file is served statically and can be replaced
// at container start (see docker-entrypoint.d/40-app-config.sh) so the same
// build can target different environments without recompiling.
// The values below are the dev/local defaults used by `npm run dev`.
window.__APP_CONFIG__ = {
  API_URL: "http://localhost:8080",
};

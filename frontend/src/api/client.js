const BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api').replace(/\/$/, '');
const TOKEN_KEY = 'placeprep-token';

let unauthorizedHandler = null;

export class ApiError extends Error {
  constructor(status, message, code = 'error', fields = null) {
    super(message);
    this.status = status;
    this.code = code;
    this.fields = fields;
  }
}

function readToken() {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch {
    return null;
  }
}

let token = readToken();

export function getToken() {
  return token;
}

export function setToken(value) {
  token = value || null;
  try {
    if (token) localStorage.setItem(TOKEN_KEY, token);
    else localStorage.removeItem(TOKEN_KEY);
  } catch {
    // Storage can be unavailable (private mode); the session then lasts until reload.
  }
}

/** Called when the server rejects the stored token, so the app can log out. */
export function onUnauthorized(handler) {
  unauthorizedHandler = handler;
}

export async function request(path, { method = 'GET', body, auth = true, signal } = {}) {
  const headers = { Accept: 'application/json' };
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (auth && token) headers.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal,
    });
  } catch (err) {
    if (err.name === 'AbortError') throw err;
    throw new ApiError(
      0,
      `Can't reach the PlacePrep server at ${BASE_URL}. It may be starting up (try again in a minute), or blocked by CORS settings.`,
      'network',
    );
  }

  const data = await response.json().catch(() => null);
  if (!response.ok) {
    const info = data?.error || {};
    if (response.status === 401 && auth && token && unauthorizedHandler) unauthorizedHandler(info.code);
    throw new ApiError(response.status, info.message || `Request failed (${response.status}).`, info.code, info.fields || null);
  }
  return data;
}

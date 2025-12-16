import { writable, derived } from 'svelte/store';

function readSession() {
  try {
    return sessionStorage.getItem('selectedCommunityId');
  } catch (e) {
    return null;
  }
}

const communityId = writable<string | null>(typeof window !== 'undefined' ? readSession() : null);

communityId.subscribe((val) => {
  try {
    if (val === null || val === undefined) sessionStorage.removeItem('selectedCommunityId');
    else sessionStorage.setItem('selectedCommunityId', val);
  } catch (e) {}
});

const isLoggedIn = derived(communityId, ($id) => !!$id);

function login(id: string) {
  communityId.set(id);
}

function logout() {
  communityId.set(null);
}

// Gov auth
const govLoggedIn = writable<boolean>(false);
const govUser = writable<any>(null);

function govLogin(user: any) {
  govLoggedIn.set(true);
  govUser.set(user);
}

function govLogout() {
  govLoggedIn.set(false);
  govUser.set(null);
}

export { communityId, isLoggedIn, login, logout, govLoggedIn, govUser, govLogin, govLogout };

// -----------------------------
// Token helpers (development fallback)
// -----------------------------
export const authToken = writable<string | null>(typeof window !== 'undefined' ? (localStorage.getItem('access_token')) : null);

export function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('access_token');
}

export function setToken(token: string) {
  if (typeof window === 'undefined') return;
  localStorage.setItem('access_token', token);
  authToken.set(token);
}

export function clearToken() {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
  authToken.set(null);
}

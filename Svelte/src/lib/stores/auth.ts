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

export { communityId, isLoggedIn, login, logout };

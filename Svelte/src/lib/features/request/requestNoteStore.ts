// src/lib/features/request/requestNoteStore.ts
import { writable } from 'svelte/store';

export const requestNote = writable<string>('');

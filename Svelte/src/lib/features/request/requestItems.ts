// src/lib/features/request/requestItems.ts

import { writable } from 'svelte/store';

export type RequestItem = {
  id: number;      // ★ 必ず存在する
  text: string;
  value: number;
};

const initialRequestItems: RequestItem[] = [
  { id: 1, text: '食料', value: 0 },
  { id: 2, text: '毛布', value: 0 },
  { id: 3, text: '乳児用粉・液体ミルク', value: 0 },
  { id: 4, text: '乳児・小児用おむつ', value: 0 },
  { id: 5, text: '生理用品', value: 0 },
  { id: 6, text: 'トイレットペーパー', value: 0 },
  { id: 7, text: '簡易・携帯トイレ', value: 0 },
  { id: 8, text: '大人用おむつ', value: 0 }
];

export const requestItems = writable(initialRequestItems);

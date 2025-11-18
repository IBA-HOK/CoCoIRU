// 申請物資リスト
import { writable } from 'svelte/store';

const initialRequestItems = [
  { text: '食料', value: 0 },
  { text: '毛布', value: 0 },
  { text: '乳児用粉・液体ミルク', value: 0 },
  { text: '乳児・小児用おむつ', value: 0 },
  { text: '生理用品', value: 0 },
  { text: 'トイレットペーパー', value: 0 },
  { text: '簡易・携帯トイレ', value: 0 },
  { text: '大人用おむつ', value: 0 }
];

export const requestItems = writable(initialRequestItems);
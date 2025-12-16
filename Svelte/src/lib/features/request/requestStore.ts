import { writable } from 'svelte/store';

export type MockRequest = {
  id: number;
  items: string[];      // 仮：品目名だけ
  note: string;         // 特記事項
  status: 'pending' | 'approved' | 'rejected';
};

export const mockRequests = writable<MockRequest[]>([
  {
    id: 1,
    items: ['粉ミルク', '毛布'],
    note: '乳児が多いため早めにお願いします',
    status: 'pending'
  },
  {
    id: 2,
    items: ['簡易ベッド'],
    note: '高齢者対応',
    status: 'pending'
  }
]);

// src/lib/features/request/requestItems.ts

import { writable } from 'svelte/store';

export type RequestItem = {
  id: number;      // ★ 必ず存在する
  text: string;
  value: number;
  unit?: string;
};

// 初期は空で、APIから動的に読み込む
export const requestItems = writable<RequestItem[]>([]);

async function loadRequestItems() {
  try {
    const res = await fetch('/api/v1/public/items');
    if (!res.ok) throw new Error(`Failed to fetch request items: ${res.status}`);
    const items = await res.json();
    const mapped: RequestItem[] = items.map((it: any) => ({
      id: it.items_id,
      text: it.item_name ?? '',
      value: 0,
      unit: it.unit ?? ''
    }));
    requestItems.set(mapped);
  } catch (err) {
    console.error('requestItems: failed to load items', err);
  }
}

// モジュールロード時に一度読み込む
loadRequestItems();

// src/routes/+page.ts
import type { PageLoadEvent } from './$types'; 

// APIが返すコミュニティの型 (gnss.py に合わせる)
interface Community {
  community_id: number;
  member_id?: number | null;
  name?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  member_count?: number | null;
  created_at?: string | null;
}

// FastAPIバックエンドのURL (仮にlocalhost:8000とします)
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const load = async ({ fetch }: PageLoadEvent) => {
  // 1. 検索パラメータ (例として固定値を使用)
  const params = {
    latitude: 35.681,  // 中心の緯度
    longitude: 139.767, // 中心の経度
    range: 10.0         // 検索範囲 (km)
  };

  try {
    // 2. FastAPIの /gnss/nearby エンドポイントを叩く
    const res = await fetch(
      `${API_BASE_URL}/gnss/nearby?latitude=${params.latitude}&longitude=${params.longitude}&range=${params.range}`
    );

    if (!res.ok) {
      throw new Error(`API error: ${res.status}`);
    }
    const communities: Community[] = await res.json();
    return {
      communities: communities,
      mapCenter: [params.longitude, params.latitude] as [number, number]
    };

  } catch (error) {
    console.error('Failed to fetch nearby communities:', error);
    return {
      communities: [],
      mapCenter: [139.767, 35.681] as [number, number]
    };
  }
};
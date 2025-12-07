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

// FastAPIバックエンドのURL — 開発では Vite の proxy (/api) を使うため相対パスにする
const API_BASE_URL = '/api/v1';

export const load = async (event: PageLoadEvent) => {
  const e: any = event;
  const fetch = e.fetch as typeof globalThis.fetch;
  const cookies = e.cookies as any;
  // 1. 検索パラメータ (例として固定値を使用)
  const params = {
    latitude: 35.681,  // 中心の緯度
    longitude: 139.767, // 中心の経度
    range: 10.0         // 検索範囲 (km)
  };

  try {
    // 2. FastAPIの /gnss/nearby エンドポイントを叩く
    const url = `${API_BASE_URL}/gnss/nearby?latitude=${params.latitude}&longitude=${params.longitude}&range=${params.range}`;

    // SvelteKitのloadはサーバーとクライアント両方で走る可能性があるため
    // - サーバーサイドではクライアントから受け取ったCookieを明示的に転送する必要がある
    // - クライアントサイドではブラウザにCookieを送らせるために`credentials: 'include'`を使う
    const fetchOptions: RequestInit = {};
    // `request` はサーバー側のロードから利用できるヘッダ情報（存在しない場合もある）

    if (typeof window === 'undefined') {
      // SSR: SvelteKit の cookies API から access_token を取得して転送
      const accessToken = cookies.get('access_token');
      if (accessToken) fetchOptions.headers = { cookie: `access_token=${accessToken}` };
    } else {
      // クライアント: ブラウザに Cookie を送らせる
      fetchOptions.credentials = 'include';
    }

    const res = await fetch(url, fetchOptions);

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
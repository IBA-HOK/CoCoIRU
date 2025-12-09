// src/routes/+page.ts
import type { PageServerLoad } from './$types'; 

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

export const load: PageServerLoad = async ({ fetch, cookies, url }) => {
  const latParam = url.searchParams.get('latitude');
  const lngParam = url.searchParams.get('longitude');
  const rangeParam = url.searchParams.get('range');
  // 1. 検索パラメータ (例として固定値を使用)
  const params = {
    latitude: latParam ? parseFloat(latParam) : 35.681, 
    longitude: lngParam ? parseFloat(lngParam) : 139.767,
    range: rangeParam ? parseFloat(rangeParam) : 10.0
  };

  try {
    // 2. FastAPIの /gnss/nearby エンドポイントを叩く
    const url = `${API_BASE_URL}/gnss/nearby?latitude=${params.latitude}&longitude=${params.longitude}&range=${params.range}`;

    // SvelteKitのloadはサーバーとクライアント両方で走る可能性があるため
    // - サーバーサイドではクライアントから受け取ったCookieを明示的に転送する必要がある
    // - クライアントサイドではブラウザにCookieを送らせるために`credentials: 'include'`を使う
    const fetchOptions: RequestInit = {};
    // `request` はサーバー側のロードから利用できるヘッダ情報（存在しない場合もある）

    const accessToken = cookies.get('access_token');
    
    if (accessToken) {
      fetchOptions.headers = { cookie: `access_token=${accessToken}` };
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
      mapCenter: [params.longitude, params.latitude] as [number, number]
    };
  }
};
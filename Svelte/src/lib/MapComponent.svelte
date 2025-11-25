<script lang="ts">
  import { onMount, onDestroy, createEventDispatcher } from 'svelte';
  import maplibregl from 'maplibre-gl';
  import 'maplibre-gl/dist/maplibre-gl.css';
  const dispatch = createEventDispatcher();

  // マーカー情報の型定義
  interface MarkerInfo {
    lat: number;
    lng: number;
    caption: string;
    detail?: any; // 詳細データ用 何を入れるかはまだ決めていない
  }

  export let markers: MarkerInfo[] = [];
  export let initialCenter: [number, number] = [136.884, 35.170];
  export let initialZoom: number = 10;
  export let radiusKm: number = 5;
  export let isSelectionMode = false; // 範囲指定モードかどうか

  let mapContainer: HTMLDivElement;
  let map: maplibregl.Map;
  let isDragging = false;
  let dragStartCoords: maplibregl.LngLat | null = null;
  let hoverPopup: maplibregl.Popup | null = null;// 現在のカーソル位置のポップアップ（ホバー用）

  // --- ヘルパー関数: 中心と半径(km)から円のポリゴン座標を生成 ---
  function createGeoJSONCircle(center: [number, number], radiusInkm: number, points: number = 64) {
    const coords = {
      latitude: center[1],
      longitude: center[0]
    };
    const km = radiusInkm;
    const ret = [];
    const distanceX = km / (111.32 * Math.cos((coords.latitude * Math.PI) / 180));
    const distanceY = km / 110.574;

    let theta, x, y;
    for (let i = 0; i < points; i++) {
      theta = (i / points) * (2 * Math.PI);
      x = distanceX * Math.cos(theta);
      y = distanceY * Math.sin(theta);
      ret.push([coords.longitude + x, coords.latitude + y]);
    }
    ret.push(ret[0]); // 多角形を閉じる
    return ret;
  }

  // --- ヘルパー関数: 地図上の円を更新する関数 ---
  function updateCircle(center: [number, number], radius: number) {
    const source = map.getSource('search-radius-source') as maplibregl.GeoJSONSource;
    if (source) {
      source.setData({
        type: 'FeatureCollection',
        features: [{
          type: 'Feature',
          geometry: {
            type: 'Polygon',
            coordinates: [createGeoJSONCircle(center, radius)]
          },
          properties: {}
        }]
      });
    }
  }

  // --- 範囲指定モードの監視 ---
  $: if (map) {
    if (isSelectionMode) {
      map.dragPan.disable(); // 地図の移動を禁止
      map.getCanvas().style.cursor = 'crosshair'; // カーソルを十字に
    } else {
      map.dragPan.enable(); // 地図の移動を許可
      map.getCanvas().style.cursor = '';
    }
  }

  // --- 半径や中心の監視 ---
  $: if (map && !isDragging) {
     // ドラッグ中でなければ、Propsの変更を地図に反映
     updateCircle(initialCenter, radiusKm);
  }

  onMount(() => {
    map = new maplibregl.Map({
      container: mapContainer,
      style: {
        version: 8,
        sources: {
          'osm-tiles': {
            type: 'raster',
            tiles: ['https://a.tile.openstreetmap.org/{z}/{x}/{y}.png'],
            tileSize: 256,
            attribution: '&copy; OpenStreetMap contributors'
          }
        },
        layers: [{
          id: 'osm-layer',
          type: 'raster',
          source: 'osm-tiles',
          minzoom: 0,
          maxzoom: 19
        }]
      },
      center: initialCenter,
      zoom: initialZoom
    });

    map.on('load', () => {
      // ソース追加
      map.addSource('search-radius-source', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] } // 初期は空
      });

      // 円のレイヤー追加
      map.addLayer({
        id: 'search-radius-layer',
        type: 'fill',
        source: 'search-radius-source',
        paint: {
          'fill-color': '#ff5252', // 赤系に変更
          'fill-opacity': 0.2
        }
      });
      map.addLayer({
        id: 'search-radius-outline',
        type: 'line',
        source: 'search-radius-source',
        paint: {
          'line-color': '#ff5252',
          'line-width': 2,
          'line-dasharray': [2, 2]
        }
      });
      
      // 円の外枠線 (オプション)
      map.addLayer({
        id: 'search-radius-outline',
        type: 'line',
        source: 'search-radius-source',
        layout: {},
        paint: {
          'line-color': '#007cbf',
          'line-width': 2
        }
      });
      // 初期描画
      updateCircle(initialCenter, radiusKm);
      // --- マーカー配置 ---
      renderMarkers();
    });


    // D&Dで半径を選択
    map.on('mousedown', (e) => {
      if (!isSelectionMode) return;
      isDragging = true;
      dragStartCoords = e.lngLat;
      
      // 中心点を更新 (Propsを更新するために親へ通知)
      dispatch('centerChange', [dragStartCoords.lng, dragStartCoords.lat]);
    });

    map.on('mousemove', (e) => {
      if (!isSelectionMode || !isDragging || !dragStartCoords) return;

      const currentCoords = e.lngLat;
      // 距離計算 (メートル → キロメートル)
      const distKm = dragStartCoords.distanceTo(currentCoords) / 1000;
      
      // 円をリアルタイム更新
      updateCircle([dragStartCoords.lng, dragStartCoords.lat], distKm);
      
      // 親コンポーネントへ「今の半径」を伝える（表示用）
      dispatch('radiusChangePreview', distKm);
    });

    map.on('mouseup', (e) => {
      if (!isSelectionMode || !isDragging || !dragStartCoords) return;
      
      const currentCoords = e.lngLat;
      const distKm = dragStartCoords.distanceTo(currentCoords) / 1000;
      
      isDragging = false;
      dragStartCoords = null;

      // 最終的な半径を親へ通知
      dispatch('radiusChange', distKm);
      
      // モードを終了するかはUX次第ですが、今回は連続操作できるように維持します
      // isSelectionMode = false; 
    });
  });
  // マーカーを再描画する関数
  function renderMarkers() {
    // 既存マーカーの削除ロジックを入れるのが理想ですが、今回は簡易的に追加のみ
    markers.forEach((markerInfo) => {
      // マーカー要素を作成
      const el = document.createElement('div');
      el.className = 'custom-marker';
      el.style.backgroundImage = 'url(https://maplibre.org/maplibre-gl-js/docs/assets/osgeo-logo.png)'; // 仮アイコン
      el.style.width = '30px';
      el.style.height = '30px';
      el.style.backgroundSize = 'cover';
      el.style.cursor = 'pointer';

      // --- イベント: マウスオーバーで概要 (Popup) ---
      el.addEventListener('mouseenter', () => {
        if (!map) return;
        hoverPopup = new maplibregl.Popup({
            closeButton: false,
            closeOnClick: false,
            offset: 15
        })
        .setLngLat([markerInfo.lng, markerInfo.lat])
        .setHTML(`<div style="font-weight:bold;">${markerInfo.caption}</div>`)
        .addTo(map);
      });

      el.addEventListener('mouseleave', () => {
        if (hoverPopup) {
            hoverPopup.remove();
            hoverPopup = null;
        }
      });

      // --- イベント: クリックで詳細モーダル ---
      el.addEventListener('click', () => {
        // 親へ通知
        dispatch('markerClick', markerInfo);
      });

      // マーカー追加 (デフォルトのピンを使う場合)
      new maplibregl.Marker() // el を渡せばカスタムアイコンになります
        .setLngLat([markerInfo.lng, markerInfo.lat])
        // .setPopup... // クリック時のPopupは無効化してModalにするためセットしない
        .addTo(map);
    });
  }

  onDestroy(() => {
    if (map) map.remove();
  });
</script>

<div class="map-wrap">
  <div class="map" bind:this={mapContainer}></div>
  
  {#if isSelectionMode}
    <div class="mode-indicator">
      中心をクリックし、ドラッグして範囲を決めてください
    </div>
  {/if}
</div>

<style>
  .map-wrap {
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 500px;
  }
  
  .map {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 100%;
    height: 100%;
  }

  .mode-indicator {
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    background: rgba(255, 82, 82, 0.9);
    color: white;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: bold;
    pointer-events: none;
    z-index: 10;
  }
</style>
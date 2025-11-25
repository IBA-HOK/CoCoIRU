<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import maplibregl from 'maplibre-gl';
  import 'maplibre-gl/dist/maplibre-gl.css';

  // マーカー情報の型定義
  interface MarkerInfo {
    lat: number;
    lng: number;
    caption: string;
  }

  export let markers: MarkerInfo[] = [];
  export let initialCenter: [number, number] = [136.884, 35.170];
  export let initialZoom: number = 10;
  export let radiuskm: number;

  let mapContainer: HTMLDivElement;
  let map: maplibregl.Map;

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

  onMount(() => {
    map = new maplibregl.Map({
      container: mapContainer,
      style: {
        version: 8,
        sources: {
          'osm-tiles': {
            type: 'raster',
            tiles: [
              'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
              'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
              'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png'
            ],
            tileSize: 256,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          }
        },
        layers: [
          {
            id: 'osm-layer',
            type: 'raster',
            source: 'osm-tiles',
            minzoom: 0,
            maxzoom: 19
          }
        ]
      },
      center: initialCenter,
      zoom: initialZoom
    });

    map.on('load', () => {
      // 範囲円 (Circle) の描画
      map.addSource('search-radius-source', {
        type: 'geojson',
        data: {
          type: 'FeatureCollection',
          features: [{
            type: 'Feature',
            geometry: {
              type: 'Polygon',
              coordinates: [createGeoJSONCircle(initialCenter, radiuskm)]
            },
            properties: {}
          }]
        }
      });

      // レイヤーを追加 (半透明の青い円)
      map.addLayer({
        id: 'search-radius-layer',
        type: 'fill',
        source: 'search-radius-source',
        layout: {},
        paint: {
          'fill-color': '#007cbf', // 円の色
          'fill-opacity': 0.3      // 透明度 (0.0 ~ 1.0)
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

      markers.forEach((markerInfo) => {
        // maplibregl.Popup として使う
        const popup = new maplibregl.Popup({ offset: 25 })
          .setText(markerInfo.caption);

        // maplibregl.Marker として使う
        new maplibregl.Marker()
          .setLngLat([markerInfo.lng, markerInfo.lat])
          .setPopup(popup)
          .addTo(map);
      });
    });
  });

  onDestroy(() => {
    if (map) map.remove();
  });
</script>

<div class="map-wrap">
  <div class="map" bind:this={mapContainer}></div>
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
</style>
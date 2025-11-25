<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  
  // 【修正ポイント1】中括弧 {} をやめて、デフォルトインポートにします
  // エラー原因: import { Map, Marker, Popup } from 'maplibre-gl'; 
  import maplibregl from 'maplibre-gl';
  
  import 'maplibre-gl/dist/maplibre-gl.css';

  // マーカー情報の型定義
  interface MarkerInfo {
    lat: number;
    lng: number;
    caption: string;
  }

  export let markers: MarkerInfo[] = [];
  export let initialCenter: [number, number] = [139.767, 35.681];
  export let initialZoom: number = 10;

  let mapContainer: HTMLDivElement;
  // 型定義も maplibregl.Map を参照するように変更
  let map: maplibregl.Map;

  onMount(() => {
    // 【修正ポイント2】 maplibregl.Map として使います
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
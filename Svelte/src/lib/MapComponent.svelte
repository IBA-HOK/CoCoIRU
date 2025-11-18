<script lang="ts">
  import { MapLibre, Marker, Popup } from 'svelte-maplibre-gl';
  import type { LngLatLike, StyleSpecification } from 'maplibre-gl';
  import 'maplibre-gl/dist/maplibre-gl.css';

  // マーカーの型定義 (TypeScriptエラー防止のため)
  interface MarkerInfo {
    lat: number;
    lng: number;
    caption: string;
  }

  /**
   * マーカー情報の配列
   */
  export let markers: MarkerInfo[] = [];

  /** 地図の初期中心座標 (緯度経度) [lng, lat] */
  export let initialCenter: [number, number] = [139.767, 35.681];// 名駅

  /** 地図の初期ズームレベル */
  export let initialZoom: number = 10;

  const mapStyle: StyleSpecification = {
    version: 8,
    sources: {
      'osm-tiles': {
        type: 'raster',
        tiles: [
          // OSMのタイルサーバーURL
          'https://a.tile.openstreetmap.org/{z}/{x}/{y}.png',
          'https://b.tile.openstreetmap.org/{z}/{x}/{y}.png',
          'https://c.tile.openstreetmap.org/{z}/{x}/{y}.png'
        ],
        tileSize: 256,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }
    },
    layers: [
      {
        id: 'osm-layer', 
        type: 'raster',
        source: 'osm-tiles'
      }
    ]
  };
</script>

<div class="map-container">
  <MapLibre
    style={mapStyle}
    center={initialCenter}
    zoom={initialZoom}
  >

    {#each markers as marker (marker.caption)}
      
      <Marker lnglat={[marker.lng, marker.lat]}>
        
        <Popup>
          <div>
            <p>{marker.caption}</p>
          </div>
        </Popup>

      </Marker> [cite: 7]
    {/each}

  </MapLibre>
</div>

<style>
  /* スタイルも変更ありません */
  .map-container {
    width: 100%;
    height: 500px;
  }
  :global(.maplibregl-popup-content) {
    padding: 10px;
  }
  :global(.maplibregl-popup-content p) {
    margin: 0;
  }
</style>
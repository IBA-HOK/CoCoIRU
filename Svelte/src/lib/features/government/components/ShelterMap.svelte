<script lang="ts">
  import MapComponent from '$lib/MapComponent.svelte';

  // 親から受け取るデータ
  export let markers: any[] = [];
  export let mapCenter: [number, number];
  export let searchRadiusKm: number;
  export let isSelectionMode: boolean = false;

  // イベントディスパッチャー
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  // イベントハンドラ（親にそのまま転送する）
  function handleMarkerClick(e: CustomEvent) { dispatch('markerClick', e.detail); }
  function handleRadiusPreview(e: CustomEvent) { dispatch('radiusChangePreview', e.detail); }
  function handleRadiusChange(e: CustomEvent) { dispatch('radiusChange', e.detail); }
  function handleCenterChange(e: CustomEvent) { dispatch('centerChange', e.detail); }

  $: console.debug('[ShelterMap] markers length', markers?.length);
</script>

<div class="map-wrapper">
  <MapComponent 
    {markers}
    center={mapCenter}
    initialZoom={11}
    radiusKm={searchRadiusKm}
    bind:isSelectionMode={isSelectionMode}
    on:markerClick={handleMarkerClick}
    on:radiusChangePreview={handleRadiusPreview}
    on:radiusChange={handleRadiusChange}
    on:centerChange={handleCenterChange}
  />
</div>

<style>
  .map-wrapper {
    flex: 1;
    border: 1px solid var(--outline);
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
</style>
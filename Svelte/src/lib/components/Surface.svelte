<script lang="ts">
  export { className as class };
  
  /**
	 * @component Surface
	 * @description
	 * 背景の上にのせる一つ目のカードコンポーネント。
	 */

  let className = '';
</script>

<div class="surface {className}">
  <slot />
</div>

<style>
  .surface {
    height: 100%;
    background-color: var(--card);
    border-radius: 16px;
    margin: 20px;
    padding: 24px;
    box-shadow: 
      0 2px 4px color-mix(in srgb, var(--shadow), transparent 90%), 
      0 0 1px color-mix(in srgb, var(--shadow), transparent 85%);
    border: 1px solid var(--outline-sub);
    box-sizing: border-box;
  }
</style>
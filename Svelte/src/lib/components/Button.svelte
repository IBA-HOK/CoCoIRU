<script lang="ts">
  export let text = 'ボタンテキスト';
</script>

<button on:click>
  {text}
</button>

<style>
  button {
    flex: 1;
    width: 100%;
    padding: 20px;
    text-decoration: none;
    border: none;
    border-radius: 8px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 6px color-mix(in srgb, var(--md-sys-color-shadow), transparent 85%);
    text-align: center;
    font-weight: bold;
    font-size: 1.5rem;
    cursor: pointer;
    background-color: var(--primary);
    color: var(--on-primary);
    font-family: inherit;
  }

  button:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 15px color-mix(in srgb, var(--md-sys-color-shadow), transparent 80%);
    background-color: color-mix(in srgb, var(--primary), black 10%);
  }

  button:active {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px color-mix(in srgb, var(--md-sys-color-shadow), transparent 85%);
  }
</style>
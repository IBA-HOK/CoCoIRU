<script lang="ts">
  export let text = 'ボタンテキスト';
</script>

<button on:click>
  {text}
</button>

<style>
  button {
        flex: 1;
        padding: 20px;
        text-decoration: none; /* リンクの下線を消す */
        color: inherit; /* 文字の色を親要素から継承する */
        border: 1px solid #ddd;
        border-radius: 8px;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 要素の下に影を付ける */
        text-align: center;
  }
  button:hover {
            transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
        background-color: #e8f5e9;
  }
</style>
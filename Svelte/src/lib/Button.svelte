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
      text-decoration: none; 
      border: 1px solid #ddd;
      border-radius: 8px;
      transition: all 0.2s ease;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      text-align: center;
      font-weight: bold; 
      font-size: 1.5rem;
      background-color: #ffffff;
      color: #00796b;       
  }

  button:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 15px rgba(0, 0, 0, 0.15);
      background-color: #e8f5e9;
  }
</style>
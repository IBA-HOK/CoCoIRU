<script lang="ts">
  export let value: string = '';
</script>

<div class="note-input-container">
  <label for="note-textarea" class="label">特記事項</label>
  <div class="input-wrapper">
    <textarea
      id="note-textarea"
      bind:value
      placeholder="ご要望があればご記入ください"
      rows="3"
    ></textarea>
  </div>
</div>

<style>
  .note-input-container {
    width: 100%;
  }

  .label {
    display: block;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 8px;
    color: #666;
  }

  textarea {
    width: 100%;
    box-sizing: border-box;
    font-size: 0.95rem;
    padding: 10px;
    border-radius: 8px;
    
    background-color: #f7f7f7; 
    border: 1px solid #e0e0e0;
    
    resize: none;
    transition: all 0.2s ease;
    outline: none;
    font-family: inherit;
    color: #333;
  }

  textarea:focus {
    background-color: #fff;
    border-color: #4CAF50;
    box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.1);
  }

  textarea::placeholder {
    color: #bbb;
  }
</style>
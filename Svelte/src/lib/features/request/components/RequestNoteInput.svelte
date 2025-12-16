<script lang="ts">
	//export let value: string = '';
	import { requestNote } from '$lib/features/request/requestNoteStore';
</script>

<div class="note-input-container">
	<label for="note-textarea" class="label">特記事項</label>
	<div class="input-wrapper">
		<textarea 
			id="note-textarea" 
			bind:value={$requestNote}   
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
		color: var(--text);
	}

	textarea {
		width: 100%;
		box-sizing: border-box;
		font-size: 0.95rem;
		padding: 10px;
		border-radius: 8px;

		background-color: var(--bg);
		border: 1px solid var(--outline);

		resize: none;
		
		outline: none;
		font-family: inherit;
		color: var(--text);
	}

	textarea:focus,
	textarea:focus-visible {
		border-width: 2px; 
  		background-color: var(--bg);
  		box-shadow: none;
  		outline: none;
	}


	textarea::placeholder {
		color: var(--text-sub);
		opacity: 0.7;
	}
</style>

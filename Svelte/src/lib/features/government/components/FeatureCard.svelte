<script lang="ts">
	/**
	 * @component FatureCard
	 * @description
	 * 行政画面トップのカードコンポーネント
	 */

	export let href = '';
	export let titleText = '';
	export let descriptionText = '';
	export let linkText = '';
	export let iconSrc = '';
	export let iconAlt = 'カードアイコン';
</script>

<a {href} class="feature-card">
    <div class="card-header">
        {#if iconSrc}
            <img src={iconSrc} alt={iconAlt} class="card-icon" />
        {/if}
        <h2>{titleText}</h2>
    </div>
    <p>{descriptionText}</p>
    <div class="link-label">{linkText}</div>
</a>

<style>
	.feature-card {
        display: block;
        padding: 25px;
        border-radius: 8px;
        box-shadow: 0 4px 12px color-mix(in srgb, var(--shadow), transparent 90%);
        text-decoration: none;
        transition:
            transform 0.2s,
            box-shadow 0.2s;
        background-color: var(--card);
        border-top: 5px solid var(--primary);
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 18px color-mix(in srgb, var(--shadow), transparent 85%);
    }
	.card-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .card-icon {
        width: 2em;
        height: 2em;
        flex-shrink: 0;
    }
	.feature-card h2 {
		color: var(--primary);
		margin: 0;
		font-size: 1.5em;
	}
	.feature-card p {
		color: var(--text);
		line-height: 1.6;
		margin-top: 15px;
	}
	.link-label {
		margin-top: 15px;
		color: var(--accent);
		font-weight: bold;
	}
</style>

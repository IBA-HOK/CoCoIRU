<script lang="ts">
  const currentYear = new Date().getFullYear();
</script>

<footer class="simple-footer">
    <a href="/" class="logo-link">
      <img src="/src/lib/assets/CoCoIRU_logo.png" alt="CoCoIRU" class="footer-logo" />
    </a>

</footer>

<style>
  .simple-footer {
    padding: 30px 20px;
    margin-top: auto;
    display: flex;
    justify-content: center;
    align-items: center;
		background-color: var(--bg);
  }

  /* ロゴのリンク */
  .logo-link {
    display: block;
    transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    text-decoration: none;
    line-height: 0;
  }
  
  .footer-logo {
    height: 40px;
    width: auto;
    transition: filter 0.3s;
  }
</style>
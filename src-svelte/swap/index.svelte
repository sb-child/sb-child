<script lang="ts">
  import metaStyle from "../meta.module.css";
  let count = $state(0);
</script>

<div class={metaStyle.container}>
  <button onclick={() => count++}>
    Clicks: {count}
  </button>
</div>

<style>
</style>

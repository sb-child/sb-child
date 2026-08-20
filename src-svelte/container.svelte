<script lang="ts">
  import { compContainerClass } from "./meta";
  let { children } = $props();
</script>

<div class={compContainerClass}>
  <div>
    {@render children()}
  </div>
</div>

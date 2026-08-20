<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card/index.js";
  import { compContainerClass } from "../meta";
  let count = $state(0);
</script>

<div class={compContainerClass}>
  <Card.Root>
    <Button onclick={() => count++} variant="outline">
      Click1111s: {count}
    </Button>
  </Card.Root>
</div>

<style>
</style>

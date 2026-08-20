<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import * as Card from "$lib/components/ui/card/index.js";
  import * as Item from "$lib/components/ui/item";
  import Container from "../container.svelte";
  import { compContainerClass } from "../meta";
  let count = $state(0);
</script>

<!-- {@render Container(<div></div>)} -->

<Container>
  <Button onclick={() => count++} variant="outline">
    Click1111s: {count}
  </Button>
  <Item.Root variant="outline" size="sm">
    <Item.Content>
      <Item.Title>Your profile has been verified.</Item.Title>
    </Item.Content>
  </Item.Root>
  <Card.Root>
    <Button onclick={() => count++} variant="outline">
      Click1111s: {count}
    </Button>
  </Card.Root>
</Container>

<style>
</style>

<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { onMount } from "svelte";
  import * as Card from "$lib/components/ui/card/index.js";
  import * as Item from "$lib/components/ui/item";
  import Container from "../container.svelte";
  import { global_width } from "../globalWidthListener.svelte";
  import { containerWidth } from "../meta";
  const bp = containerWidth * 0.7;
  const displayMode = global_width((w) => (w < bp ? "single" : "split"));
</script>

<div use:displayMode.attach>
  <Container>
    {#if displayMode.current === "split"}
      <div class="flex gap-4">
        <div
          class="flex-1 rounded-lg bg-blue-500 p-10 text-center text-xl font-bold text-white shadow-md"
        >
          Container A
        </div>
        <div
          class="flex-1 rounded-lg bg-emerald-500 p-10 text-center text-xl font-bold text-white shadow-md"
        >
          Container B
        </div>
      </div>
    {:else}
      <div class="w-full">
        <div
          class="rounded-lg bg-amber-500 p-10 text-center text-xl font-bold text-white shadow-md"
        >
          Container C
        </div>
      </div>
    {/if}
  </Container>
</div>

<style>
</style>

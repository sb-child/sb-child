<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { onMount } from "svelte";
  import * as Card from "$lib/components/ui/card/index.js";
  import * as Item from "$lib/components/ui/item";
  import Container from "../container.svelte";
  import { global_width } from "../globalWidthListener.svelte";
  import {
    containerWidth,
    OnlineStatus,
    type ContainerHeaderOptions,
  } from "../meta";
  import {
    Check as CheckIcon,
    SatelliteDish as SatelliteDishIcon,
    Heart as HeartIcon,
    DatabaseSearch as DatabaseSearchIcon,
    Ellipsis as EllipsisIcon,
  } from "@lucide/svelte";
  const bp = containerWidth * 0.7;
  const displayMode = global_width((w) => (w < bp ? "single" : "split"));
  let headerOpt: ContainerHeaderOptions = $state({
    name: "sbchild Swap",
    onlineLog: (brief: boolean) => {
      return "";
    },
    onlineStatus: OnlineStatus.Online,
    buttons: [
      {
        onClick: () => {},
        title: "Order Status",
        icon: DatabaseSearchIcon,
      },
      {
        onClick: () => {
          setTimeout(() => {
            headerOpt.name = "test";
            headerOpt.onlineStatus = OnlineStatus.Offline;
            headerOpt.buttons[0].title = "aaa";
            console.log(headerOpt);
          }, 1000);
        },
        title: "Donate me",
        icon: HeartIcon,
      },
    ],
  });
</script>

<div use:displayMode.attach>
  <Container headerOptions={headerOpt}>
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

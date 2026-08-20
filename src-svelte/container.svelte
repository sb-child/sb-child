<script lang="ts">
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
  import { Separator } from "$lib/components/ui/separator";
  import Spinner from "$lib/components/ui/spinner/spinner.svelte";
  import {
    compContainerClass,
    containerHeaderButtonOverrideClass,
    containerHeaderColorClass,
    type ContainerHeaderOptions,
    containerHeaderSizeClass,
    OnlineStatus,
  } from "./meta";
  import {
    Check as CheckIcon,
    SatelliteDish as SatelliteDishIcon,
    Heart as HeartIcon,
    DatabaseSearch as DatabaseSearchIcon,
  } from "@lucide/svelte";
  let { children } = $props();

  let containerOptions: ContainerHeaderOptions = $state({
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
            containerOptions.name = "test";
            containerOptions.onlineStatus = OnlineStatus.Offline;
            containerOptions.buttons[0].title = "aaa";
            console.log(containerOptions);
          }, 1000);
        },
        title: "Donate me",
        icon: HeartIcon,
      },
    ],
  });
</script>

{#snippet HeaderWide(opt: ContainerHeaderOptions)}
  <div class="flex">
    <div
      class={containerHeaderColorClass +
        containerHeaderSizeClass +
        " rounded-tl-lg rounded-br-lg"}
    >
      <span class="font-bold tracking-tight pl-1 pr-1 [align-self:end]"
        >{opt.name}</span
      >
      {#if [OnlineStatus.Connecting, OnlineStatus.WaitRetry].includes(opt.onlineStatus)}
        <Spinner />
      {/if}
      {#if opt.onlineStatus == OnlineStatus.Connecting}
        <Badge variant="outline"><SatelliteDishIcon />Connecting...</Badge>
      {:else if opt.onlineStatus == OnlineStatus.Offline}
        <Badge variant="destructive"><SatelliteDishIcon />Offline</Badge>
      {:else if opt.onlineStatus == OnlineStatus.WaitRetry}
        <Badge variant="secondary"><SatelliteDishIcon />Retry in 5s...</Badge>
      {:else}
        <Badge variant="default"><CheckIcon />Online</Badge>
      {/if}
    </div>
    <div class="flex-1"></div>
    <div
      class={containerHeaderColorClass +
        containerHeaderSizeClass +
        " rounded-tr-lg rounded-bl-lg"}
    >
      {#each opt.buttons as butt}
        <Button
          class={containerHeaderButtonOverrideClass}
          variant="outline"
          size="xs"
          onclick={butt.onClick}
        >
          {#if butt.icon}
            <butt.icon />
          {/if}
          {butt.title}
        </Button>
      {/each}
    </div>
  </div>
{/snippet}

<div class={compContainerClass}>
  {@render HeaderWide(containerOptions)}
  <div class="pt-4 pl-4 pr-4">
    {@render children()}
  </div>
</div>

<script lang="ts">
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
  import { Separator } from "$lib/components/ui/separator";
  import Spinner from "$lib/components/ui/spinner/spinner.svelte";
  import {
    compContainerClass,
    containerHeaderButtonOverrideClass,
    containerHeaderColorClass,
    containerHeaderCornerColorClass,
    type ContainerHeaderOptions,
    containerHeaderSizeClass,
    OnlineStatus,
  } from "./meta";
  import {
    Check as CheckIcon,
    SatelliteDish as SatelliteDishIcon,
    Heart as HeartIcon,
    DatabaseSearch as DatabaseSearchIcon,
    Ellipsis as EllipsisIcon,
  } from "@lucide/svelte";
  let { children } = $props();
  import { global_width } from "./globalWidthListener.svelte";
  import { get_root } from "./root.svelte";
  import { containerWidth } from "./meta";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import Cc from "./concaveCorner.svelte";
  import { cn } from "$lib/utils";
  const headerMode = global_width((w) =>
    w < containerWidth * 0.6 ? "merged" : "wide",
  );
  const rootNode = get_root();

  let headerMergedContainerWidth = $state(0);
  let headerMergedLeftWidth = $state(0);
  let headerMergedButtonsIntrinsicWidth = $state(0);
  let headerMergedMoreWidth = $state(0);
  const headerMergedModeGapMin = 24;
  let headerMergedShowInlineButtons = $derived(
    headerMergedContainerWidth > 0 &&
      headerMergedContainerWidth >=
        headerMergedLeftWidth +
          headerMergedButtonsIntrinsicWidth +
          headerMergedMoreWidth +
          headerMergedModeGapMin,
  );
  // $effect(() => {
  //   console.log("resize", {
  //     container: headerMergedContainerWidth,
  //     left: headerMergedLeftWidth,
  //     buttonsIntrinsic: headerMergedButtonsIntrinsicWidth,
  //     more: headerMergedMoreWidth,
  //     showInline: headerMergedShowInlineButtons,
  //   });
  // });

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
  <div class="flex [anchor-name:--HeaderWideLeft]">
    <Cc
      class={cn(
        containerHeaderCornerColorClass,
        "w-4 h-4 [position-anchor:--HeaderWideLeft] absolute top-[anchor(bottom)]",
      )}
      corner="top-right"
    ></Cc>
    <div
      class={containerHeaderColorClass +
        containerHeaderSizeClass +
        " rounded-tl-lg rounded-br-lg"}
    >
      <span class="font-bold tracking-tight px-1">
        {opt.name}
      </span>
      {#if [OnlineStatus.Connecting, OnlineStatus.WaitRetry].includes(opt.onlineStatus)}
        <Spinner />
      {/if}
      {#if opt.onlineStatus == OnlineStatus.Connecting}
        <Badge variant="outline"><SatelliteDishIcon />Connecting...</Badge>
      {:else if opt.onlineStatus == OnlineStatus.Offline}
        <Badge variant="destructive"><SatelliteDishIcon />Server Offline</Badge>
      {:else if opt.onlineStatus == OnlineStatus.WaitRetry}
        <Badge variant="secondary"><SatelliteDishIcon />
          {}
          Retry in 5s...</Badge>
      {:else}
        <Badge variant="default"><CheckIcon />Server Online</Badge>
      {/if}
    </div>
    <Cc
      class={cn(containerHeaderCornerColorClass, "w-4 h-4")}
      corner="top-right"
    ></Cc>
    <div class="flex-1"></div>
    <Cc class={cn(containerHeaderCornerColorClass, "w-4 h-4")} corner="top-left"
    ></Cc>
    <div
      class={containerHeaderColorClass +
        containerHeaderSizeClass +
        " rounded-tr-lg rounded-bl-lg [anchor-name:--HeaderWideRight]"}
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
      <Cc
        class={cn(
          containerHeaderCornerColorClass,
          "w-4 h-4 [position-anchor:--HeaderWideRight] absolute top-[anchor(bottom)] right-[anchor(right)]",
        )}
        corner="top-left"
      ></Cc>
    </div>
  </div>
{/snippet}

{#snippet HeaderMerged(opt: ContainerHeaderOptions)}
  <div
    bind:clientWidth={headerMergedContainerWidth}
    class={containerHeaderColorClass +
      containerHeaderSizeClass +
      " rounded-t-lg [anchor-name:--HeaderMerged]"}
  >
    <Cc
      class={cn(
        containerHeaderCornerColorClass,
        "w-4 h-4 [position-anchor:--HeaderMerged] absolute top-[anchor(bottom)] left-[anchor(left)] mr-0",
      )}
      corner="top-right"
    ></Cc>
    <div
      bind:clientWidth={headerMergedLeftWidth}
      class="flex flex-none items-center space-x-1 overflow-x-clip"
    >
      <span class="font-bold tracking-tight px-1">
        {opt.name}
      </span>
      {#if [OnlineStatus.Connecting, OnlineStatus.WaitRetry].includes(opt.onlineStatus)}
        <Spinner />
      {/if}
      {#if opt.onlineStatus == OnlineStatus.Connecting}
        <Badge variant="outline"><SatelliteDishIcon />Connecting...</Badge>
      {:else if opt.onlineStatus == OnlineStatus.Offline}
        <Badge variant="destructive"><SatelliteDishIcon />Server Offline</Badge>
      {:else if opt.onlineStatus == OnlineStatus.WaitRetry}
        <Badge variant="secondary"><SatelliteDishIcon />Retry in 5s...</Badge>
      {:else}
        <Badge variant="default"><CheckIcon />Server Online</Badge>
      {/if}
    </div>
    <div class="flex-auto"></div>
    {#if headerMergedShowInlineButtons}
      <div class="flex gap-1 overflow-x-clip flex-none mr-0">
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
    {:else}
      <div bind:clientWidth={headerMergedMoreWidth} class="flex-none mr-0">
        <DropdownMenu.Root>
          <DropdownMenu.Trigger>
            {#snippet child({ props })}
              <Button
                {...props}
                size="xs"
                variant="outline"
                class={containerHeaderButtonOverrideClass}
              >
                <EllipsisIcon />More
              </Button>
            {/snippet}
          </DropdownMenu.Trigger>
          <DropdownMenu.Content
            class="w-auto"
            align="end"
            portalProps={{ to: rootNode?.current }}
          >
            <DropdownMenu.Group>
              {#each opt.buttons as butt}
                <DropdownMenu.Item onclick={butt.onClick}>
                  {#if butt.icon}
                    <butt.icon />
                  {/if}
                  <div class="transform-[translateY(0.15rem)]">{butt.title}</div>
                </DropdownMenu.Item>
              {/each}
            </DropdownMenu.Group>
          </DropdownMenu.Content>
        </DropdownMenu.Root>
      </div>
    {/if}
    <Cc
      class={cn(
        containerHeaderCornerColorClass,
        "w-4 h-4 [position-anchor:--HeaderMerged] absolute top-[anchor(bottom)] right-[anchor(right)] mr-0",
      )}
      corner="top-left"
    ></Cc>
    <div
      bind:clientWidth={headerMergedButtonsIntrinsicWidth}
      aria-hidden="true"
      class="absolute left-0 top-0 pointer-events-none opacity-0 flex gap-1 whitespace-nowrap -z-50"
      style="visibility: hidden;"
    >
      {#each opt.buttons as butt}
        <Button
          class={containerHeaderButtonOverrideClass}
          variant="outline"
          size="xs"
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
  <div use:headerMode.attach use:rootNode.attach>
    {#if headerMode.current == "wide"}
      {@render HeaderWide(containerOptions)}
    {:else}
      {@render HeaderMerged(containerOptions)}
    {/if}
  </div>
  <div class="pt-4 pl-4 pr-4">
    {@render children()}
  </div>
</div>

<script lang="ts">
  import { Badge } from "$lib/components/ui/badge";
  import { Button } from "$lib/components/ui/button";
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
    Ellipsis as EllipsisIcon,
    FileScan as FileScanIcon,
  } from "@lucide/svelte";
  import { global_width } from "./globalWidthListener.svelte";
  import { get_root } from "./root.svelte";
  import { containerWidth } from "./meta";
  import * as DropdownMenu from "$lib/components/ui/dropdown-menu";
  import * as Empty from "$lib/components/ui/empty";
  import Cc from "./concaveCorner.svelte";
  import { cn } from "$lib/utils";
  import type { Snippet } from "svelte";

  interface Props {
    children?: Snippet;
    headerOptions: ContainerHeaderOptions;
  }
  let { children, headerOptions }: Props = $props();

  function hardReload() {
    window.location.reload();
  }

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
</script>

{#snippet HeaderServerStatus(opt: ContainerHeaderOptions)}
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
    <Badge variant="secondary"
      ><SatelliteDishIcon />
      {#if opt.RetrySeconds != undefined}
        {`Retry in ${opt.RetrySeconds.toFixed(2)}s...`}
      {:else}
        Retry soon...
      {/if}
    </Badge>
  {:else}
    <Badge variant="default"><CheckIcon />Server Online</Badge>
  {/if}
  {#if opt.onForceReconnect != undefined && [OnlineStatus.WaitRetry, OnlineStatus.Offline].includes(opt.onlineStatus)}
    <Button
      class={containerHeaderButtonOverrideClass}
      variant="outline"
      onclick={opt.onForceReconnect}
      size="xs">Retry Now</Button
    >
  {/if}
{/snippet}

{#snippet HeaderWide(opt: ContainerHeaderOptions)}
  <div class="flex [anchor-name:--HeaderWideLeft]">
    <Cc
      class={cn(
        containerHeaderCornerColorClass,
        "w-4 h-4 [position-anchor:--HeaderWideLeft] absolute top-[calc(anchor(bottom)-0.1px)]",
      )}
      corner="top-right"
    ></Cc>
    <div
      class={containerHeaderColorClass +
        containerHeaderSizeClass +
        " rounded-tl-lg rounded-br-lg"}
    >
      {@render HeaderServerStatus(opt)}
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
          "w-4 h-4 [position-anchor:--HeaderWideRight] absolute top-[calc(anchor(bottom)-0.1px)] right-[anchor(right)]",
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
        "w-4 h-4 [position-anchor:--HeaderMerged] absolute top-[calc(anchor(bottom)-0.1px)] left-[anchor(left)] mr-0",
      )}
      corner="top-right"
    ></Cc>
    <div
      bind:clientWidth={headerMergedLeftWidth}
      class="flex flex-none items-center space-x-1 overflow-x-clip"
    >
      {@render HeaderServerStatus(opt)}
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
                  <div>
                    {butt.title}
                  </div>
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
        "w-4 h-4 [position-anchor:--HeaderMerged] absolute top-[calc(anchor(bottom)-0.1px)] right-[anchor(right)] mr-0",
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

{#snippet emptyContainer()}
  <Empty.Root>
    <Empty.Header>
      <Empty.Media variant="icon">
        <FileScanIcon />
      </Empty.Media>
      <Empty.Title>Container is empty</Empty.Title>
      <Empty.Description>
        This situation typically occurs when there is an error in the code or
        when there is actually no content inside the
        <code
          class="relative rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm font-semibold"
          >{"<Container></Container>"}</code
        >.
      </Empty.Description>
    </Empty.Header>
    <Empty.Content>
      <div class="flex gap-2">
        <Button onclick={hardReload}>Reload Page</Button>
        <!-- <Button variant="outline">Go Back</Button> -->
      </div>
    </Empty.Content>
  </Empty.Root>
{/snippet}

<div class={compContainerClass}>
  <div use:headerMode.attach use:rootNode.attach>
    {#if headerMode.current == "wide"}
      {@render HeaderWide(headerOptions)}
    {:else}
      {@render HeaderMerged(headerOptions)}
    {/if}
  </div>
  <div class="pt-4 pl-4 pr-4">
    {#if children}
      {@render children()}
    {:else}
      {@render emptyContainer()}
    {/if}
  </div>
</div>

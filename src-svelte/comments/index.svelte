<script lang="ts">
  import { Button } from "$lib/components/ui/button";
  import { onMount } from "svelte";
  import * as Card from "$lib/components/ui/card/index.js";
  import * as Item from "$lib/components/ui/item";
  import * as Select from "$lib/components/ui/select/index.js";
  import * as Resizable from "$lib/components/ui/resizable/index.js";
  import { Textarea } from "$lib/components/ui/textarea/index.js";
  import Container from "../container.svelte";
  import { global_width } from "../globalWidthListener.svelte";
  import { getPlaceholder } from "./placeholders";
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
    Upload as UploadIcon,
    ScanSearch as ScanSearchIcon,
  } from "@lucide/svelte";

  interface Props {
    articleId?: string;
  }

  let { articleId }: Props = $props();
  let placeholderText = getPlaceholder(() => articleId ?? "");

  const commentFormats = [
    { value: "markdown", label: "Markdown" },
    { value: "plaintext", label: "纯文本" },
  ];

  let commentFormat = $state("markdown");

  const bp = containerWidth * 0.7;
  const writeAreaMinWidth = 350;
  const displayMode = global_width((w) => (w < bp ? "single" : "split"));
  const writeAreaPercent = global_width((w) => (writeAreaMinWidth / w) * 100);
  let headerOpt: ContainerHeaderOptions = $state({
    name: "评论区",
    onlineLog: (brief: boolean) => {
      return articleId ?? "-";
    },
    onlineStatus: OnlineStatus.Online,
    buttons: [
      {
        onClick: () => {},
        title: "登录",
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
        title: "Support me",
        icon: HeartIcon,
      },
    ],
  });
</script>

{#snippet WriteComment(articleId: string)}
  {#await placeholderText}
    <p>Loading...</p>
  {:then placeholderValue}
    <!-- 注意 overflow hidden 会把 textarea 的 foucs ring 截断 -->
    <Textarea name="comment-editor" placeholder={placeholderValue}></Textarea>
  {:catch error}
    <p>Error: {error.message}</p>
  {/await}
  <div class="flex gap-2 pt-2">
    <Select.Root
      type="single"
      name="选择格式"
      items={commentFormats}
      bind:value={commentFormat}
    >
      <Select.Trigger class="w-full max-w-32">
        <Select.Value placeholder="选择格式" />
      </Select.Trigger>
      <Select.Content>
        <Select.Group>
          <Select.Label>文档格式</Select.Label>
          {#each commentFormats as i (i.value)}
            <Select.Item value={i.value} label={i.label}>
              {i.label}
            </Select.Item>
          {/each}
        </Select.Group>
      </Select.Content>
    </Select.Root>
    <!-- <p class="text-sm text-muted-foreground">字数 0/8192</p> -->
    <div class="flex-1"></div>
    <Button variant="default"><UploadIcon />发布</Button>
    <Button variant="outline"><ScanSearchIcon />预览</Button>
  </div>
{/snippet}

{#snippet CommentsBody(
  articleId: string,
  headerOptions: ContainerHeaderOptions,
  displayMode: "single" | "split",
  writeAreaPercent: number,
)}
  {#if displayMode === "split"}
    <Resizable.PaneGroup direction="horizontal" class="overflow-visible!">
      <Resizable.Pane defaultSize={60}>
        <div
          class="rounded-lg bg-blue-500 p-10 text-center text-xl font-bold text-white mr-1"
        >
          id: {articleId}
        </div>
      </Resizable.Pane>
      <Resizable.Handle withHandle />
      <Resizable.Pane
        defaultSize={40}
        minSize={writeAreaPercent}
        class="overflow-visible!"
      >
        <div class="ml-1">
          {@render WriteComment(articleId)}
        </div>
      </Resizable.Pane>
    </Resizable.PaneGroup>
  {:else}
    <div class="w-full">
      <div
        class="rounded-lg bg-amber-500 p-10 text-center text-xl font-bold text-white"
      >
        id: {articleId}
      </div>
    </div>
  {/if}
{/snippet}

{#if articleId}
  <div use:displayMode.attach use:writeAreaPercent.attach>
    <Container headerOptions={headerOpt}>
      {@render CommentsBody(
        articleId,
        headerOpt,
        displayMode.current,
        writeAreaPercent.current,
      )}
    </Container>
  </div>
{/if}

<style>
</style>

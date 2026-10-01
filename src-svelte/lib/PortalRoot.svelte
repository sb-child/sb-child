<script lang="ts">
  import { BitsConfig } from "bits-ui";
  import type { Component } from "svelte";

  let {
    app: App,
    appProps = {},
    portalTarget,
  }: {
    app: Component<any>;
    appProps?: Record<string, any>;
    portalTarget: Element;
  } = $props();
</script>

<BitsConfig defaultPortalTo={portalTarget}>
  <App {...appProps} />
</BitsConfig>

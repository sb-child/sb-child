<script lang="ts">
  type Corner = "bottom-right" | "bottom-left" | "top-right" | "top-left";

  let {
    corner = "bottom-right",
    class: className = "w-3 h-3",
  }: { corner?: Corner; class?: string } = $props();

  const paths: Record<Corner, string> = {
    "bottom-right": "M 0 0 A 12 12 0 0 0 12 12 L 0 12 Z",
    "bottom-left": "M 12 0 A 12 12 0 0 1 0 12 L 12 12 Z",
    "top-right": "M 0 12 A 12 12 0 0 1 12 0 L 0 0 Z",
    "top-left": "M 12 12 A 12 12 0 0 0 0 0 L 12 0 Z",
  };
</script>

<svg
  class="flex-none pointer-events-none {className}"
  viewBox="0 0 12 12"
  fill="currentColor"
  aria-hidden="true"
>
  <path d={paths[corner]} />
</svg>

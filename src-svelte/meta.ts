import { cn } from "$lib/utils";

export function toContainerId(name: string): string {
  return `${name}-svelte-container`;
}

export const compContainerClass = cn(
  "bg-background text-foreground p-4 rounded-lg shadow-md",
  "border border-purple-400 [border-style:dashed] transition-all",
  "w-full max-w-[1100px] duration-300",
);

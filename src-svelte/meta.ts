import { cn } from "$lib/utils";
import { type Component } from "svelte";

export function toContainerId(name: string): string {
  return `${name}-svelte-container`;
}

export const containerWidthClass = cn("w-full max-w-275");
export const containerWidth = 1100;

export const compContainerClass = cn(
  "bg-background text-foreground pb-4 pt-0 pl-0 pr-0 rounded-lg shadow-md",
  "border border-purple-400 border-dashed transition-all",
  "duration-300",
  containerWidthClass,
);

export const containerHeaderColorClass = cn(
  "dark:bg-purple-400/15 bg-purple-200 dark:text-purple-300 text-purple-600",
);

export const containerHeaderSizeClass = cn(
  "h-8 p-2 space-x-1 text-sm items-center flex",
);

export const containerHeaderButtonOverrideClass = cn(
  "bg-purple-300 hover:bg-purple-500/40 border-purple-400",
);

export enum OnlineStatus {
  Offline,
  WaitRetry,
  Connecting,
  Online,
}

export type ContainerHeaderOptions = {
  name: string;
  onlineStatus: OnlineStatus;
  onlineLog: (brief: boolean) => string;
  RetrySeconds?: number;
  onForceReconnect?: () => void;
  buttons: ContainerHeaderButton[];
};

export type ContainerHeaderButton = {
  icon?: Component;
  title: string;
  onClick: () => void;
};

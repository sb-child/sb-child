import { cn } from "$lib/utils";
import { containerWidthClass } from "./meta";

export function global_width<T>(predicate: (w: number) => T) {
  let currentWidth = $state(0);
  function attach(node: HTMLElement) {
    const root = node.getRootNode();
    const targetParent = root instanceof ShadowRoot ? root : document.body;
    const measureDiv = document.createElement("div");
    measureDiv.className = cn(
      "mx-auto pointer-events-none h-0 opacity-0",
      containerWidthClass,
    );
    targetParent.appendChild(measureDiv);
    const observer = new ResizeObserver((entries) => {
      for (const entry of entries) {
        currentWidth = entry.contentRect.width;
      }
    });
    observer.observe(measureDiv);
    return {
      destroy() {
        observer.disconnect();
        measureDiv.remove();
      },
    };
  }
  return {
    get current() {
      return predicate(currentWidth);
    },
    attach,
  };
}

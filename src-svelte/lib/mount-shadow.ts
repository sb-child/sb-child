import { mount, unmount, type Component } from "svelte";
import PortalRoot from "./PortalRoot.svelte";
import globalCss from "../global.css?inline";

const cssToApply = globalCss;
const sheet = new CSSStyleSheet();
sheet.replaceSync(cssToApply);

if (typeof document !== "undefined") {
  const propertySheet = new CSSStyleSheet();
  const propertyRules = Array.from(sheet.cssRules)
    .filter((rule) => rule.cssText.startsWith("@property"))
    .map((rule) => rule.cssText)
    .join("\n");
  if (propertyRules) {
    propertySheet.replaceSync(propertyRules);
    if (!document.adoptedStyleSheets.includes(propertySheet)) {
      document.adoptedStyleSheets = [
        ...document.adoptedStyleSheets,
        propertySheet,
      ];
    }
  }
}

export function mountShadowApp(App: Component, comp: HTMLElement, props: any) {
  const target = comp;
  const shadow = target.shadowRoot ?? target.attachShadow({ mode: "open" });
  shadow.innerHTML = "";
  if (shadow.adoptedStyleSheets) {
    shadow.adoptedStyleSheets = [sheet];
  } else {
    const style = document.createElement("style");
    style.textContent = cssToApply;
    shadow.appendChild(style);
  }
  const container = document.createElement("div");
  container.className = "svelte-root";
  syncTheme(target, container);
  shadow.appendChild(container);
  const observer = new MutationObserver(() => syncTheme(target, container));
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme", "class"],
  });
  observer.observe(document.body, {
    attributes: true,
    attributeFilter: ["data-theme", "class"],
  });
  const appInstance = mount(PortalRoot, {
    target: container,
    props: { app: App, appProps: props, portalTarget: container },
  });
  return () => {
    observer.disconnect();
    unmount(appInstance);
  };
}

function syncTheme(target: HTMLElement, container: HTMLElement) {
  const html = document.documentElement;
  const body = document.body;
  const isDark =
    html.classList.contains("dark") || body.classList.contains("dark");
  const theme =
    html.getAttribute("data-theme") ||
    body.getAttribute("data-theme") ||
    (isDark ? "dark" : "light");
  if (isDark) {
    target.classList.add("dark");
    container.classList.add("dark");
  } else {
    target.classList.remove("dark");
    container.classList.remove("dark");
  }
  if (theme) {
    target.setAttribute("data-theme", theme);
    container.setAttribute("data-theme", theme);
  }
}

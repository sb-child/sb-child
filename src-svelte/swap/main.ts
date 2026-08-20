import { mount } from "svelte";
import App from "./index.svelte";
import { toContainerId } from "../meta";

const targetId = toContainerId("swap");
const target = document.getElementById(targetId);

if (target) {
  mount(App, { target });
} else {
  console.error(`[Svelte Mount Error]: Element #${targetId} not found.`);
}

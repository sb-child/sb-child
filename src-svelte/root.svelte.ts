export function get_root() {
  let target: Element | HTMLElement | null = $state(null);
  function attach(node: HTMLElement) {
    const root = node.getRootNode();
    const targetParent =
      root instanceof ShadowRoot ? root.firstElementChild : document.body;
    target = targetParent ? targetParent : null;
    console.log("get_root(): target is", target);
    return {
      destroy() {},
    };
  }
  return {
    get current() {
      if (target) {
        return target;
      }
      return undefined;
    },
    attach,
  };
}

export const PLACEHOLDER_TEXTS = [
  "按下红色回车键，微博，发布！",
  "读完你的文章，我有以下三点建议：...",
  "在评论区留下你的看法。",
  "想说点什么呢？",
  "我做梦给你写了个评论。",
  "没有人能翻到这个网页，我不是人。",
  "听君一席话，如听一席话。",
  "我同意我的发言会被爬取整理成训练语料！",
];

export async function getPlaceholder(input: () => string): Promise<string> {
  if (!PLACEHOLDER_TEXTS || PLACEHOLDER_TEXTS.length === 0) {
    throw new Error("PLACEHOLDER_TEXTS is empty");
  }
  const encoder = new TextEncoder();
  const data = encoder.encode(input());
  const hashBuffer = await crypto.subtle.digest("SHA-256", data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
  const bigIntValue = BigInt(`0x${hashHex}`);
  const index = Number(bigIntValue % BigInt(PLACEHOLDER_TEXTS.length));
  return PLACEHOLDER_TEXTS[index];
}

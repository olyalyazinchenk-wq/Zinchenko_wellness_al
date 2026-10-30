import assert from "node:assert/strict";
import test from "node:test";

async function render() {
  const workerUrl = new URL("../dist/server/index.js", import.meta.url);
  workerUrl.searchParams.set("test", String(Date.now()));
  const { default: worker } = await import(workerUrl.href);
  return worker.fetch(
    new Request("https://nutriok.example/", { headers: { accept: "text/html" } }),
    { ASSETS: { fetch: async () => new Response("Not found", { status: 404 }) } },
    { waitUntil() {}, passThroughOnException() {} },
  );
}

test("renders the NutriOK sales page with safe claims and Telegram conversion", async () => {
  const response = await render();
  assert.equal(response.status, 200);
  assert.match(response.headers.get("content-type") ?? "", /^text\/html\b/i);

  const html = await response.text();
  assert.match(html, /<title>НутриОК/);
  assert.match(html, /Разбор, после которого/);
  assert.match(html, /ХМС по Осипову/);
  assert.match(html, /не заменяет клиническую диагностику/i);
  assert.match(html, /zinchenko_wellness_ai_1_bot/);
  assert.match(html, /application\/ld\+json/);
  assert.match(html, /name="robots" content="noindex, nofollow"/);
  assert.doesNotMatch(html, /Your site is taking shape|Starter Project|codex-preview/);
});
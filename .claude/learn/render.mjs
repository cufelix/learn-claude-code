#!/usr/bin/env node
// Render a Mermaid (.mmd) or SVG (.svg) source to PNG.
//   node .claude/learn/render.mjs <source>              -> preview PNG (not published)
//   node .claude/learn/render.mjs <source> --save <slug> -> publishes viz/viz-<slug>-<ts>.png
// Prints the PNG path. The caller must Read the PNG and LOOK at it.
import { execFileSync } from "node:child_process"
import { copyFileSync, existsSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from "node:fs"
import { dirname, extname, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const HERE = dirname(fileURLToPath(import.meta.url))
const PROJECT = resolve(HERE, "..", "..")
const STATE = join(HERE, "state")
const CHROME = ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"].find(existsSync)

const [arg, flag, slug] = process.argv.slice(2)
// Auto-allowed in settings.json, so only render sources from viz/src/ — never arbitrary files.
const src = arg && resolve(arg)
if (!src || !existsSync(src) || !src.startsWith(join(PROJECT, "viz", "src") + "/") || realpathSync(src) !== src
    || ![".mmd", ".svg"].includes(extname(src)) || (flag && (flag !== "--save" || !slug))) {
  console.error("usage: render.mjs viz/src/<file.mmd|file.svg> [--save <slug>]")
  process.exit(2)
}
mkdirSync(STATE, { recursive: true })
const out = join(STATE, `preview-${Date.now()}.png`)
const launch = { ...(CHROME && { executablePath: CHROME }) }

try {
  if (extname(src) === ".svg") await renderSvg(src, out)
  else renderMermaid(src, out)
} catch (e) {
  console.error(`RENDER FAILED — fix the source and re-render.\n${(e.stderr?.toString() || e.message).slice(0, 1500)}`)
  process.exit(1)
}

if (flag === "--save") {
  const clean = slug.toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/^-+|-+$/g, "") || "viz"
  const filename = `viz-${clean}-${Date.now()}.png`
  mkdirSync(join(PROJECT, "viz"), { recursive: true })
  copyFileSync(out, join(PROJECT, "viz", filename))
  console.log(`filename: ${filename}\npath: ${join(PROJECT, "viz", filename)}`)
} else {
  console.log(`preview: ${out}`)
}

function renderMermaid(file, png) {
  const cfg = join(STATE, "puppeteer.json")
  writeFileSync(cfg, JSON.stringify(launch))
  execFileSync(join(HERE, "node_modules", ".bin", "mmdc"),
    ["-i", file, "-o", png, "-s", "2", "-b", "white", "-p", cfg], { stdio: "pipe", timeout: 90_000 })
}

async function renderSvg(file, png) {
  const { default: puppeteer } = await import("puppeteer")
  const browser = await puppeteer.launch({ ...launch, headless: true })
  try {
    const page = await browser.newPage()
    // The SVG is model-written: no scripts, no network — it only needs to be painted.
    await page.setJavaScriptEnabled(false)
    await page.setRequestInterception(true)
    page.on("request", (r) => (r.url().startsWith("data:") ? r.continue() : r.abort()))
    await page.setViewport({ width: 1600, height: 1200, deviceScaleFactor: 2 })
    await page.setContent(`<body style="margin:0;background:#fff">${readFileSync(file, "utf8")}</body>`)
    const el = await page.$("svg")
    if (!el) throw new Error("no <svg> element found in source")
    await el.screenshot({ path: png, omitBackground: false })
  } finally {
    await browser.close()
  }
}

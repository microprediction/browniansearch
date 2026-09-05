// exp2k: headless server exposing a humpday JS demo's objective(u).
//
// The docs/applications demos carry the FULL-fidelity physics (Matter.js
// multi-body simulation) while several Python ports are reduced-order
// stand-ins. This runs the real thing: load the demo HTML, evaluate its
// inline scripts in a vm sandbox with a black-hole DOM (rendering and UI
// wiring are absorbed; the physics path is DOM-free), then serve
// objective(u) over stdin/stdout as JSON lines.
//
// Usage: node js_objective_server.js <demo.html>
//   stdin:  one JSON array per line, e.g. [0.4,0.6,0.5]
//   stdout: one JSON number per line (the objective value)
//   "EXIT" terminates.

const fs = require("fs");
const vm = require("vm");
const readline = require("readline");

const Matter = require("/Users/petercotton/github/humpday/node_modules/matter-js");

const htmlPath = process.argv[2];
const html = fs.readFileSync(htmlPath, "utf8");

// ---- black-hole proxy: absorbs any get/set/call/construct ------------
function blackhole() {
  const f = function () {};
  const p = new Proxy(f, {
    get: (t, prop) => {
      if (prop === Symbol.toPrimitive) return () => 0;
      if (prop === "length") return 0;
      return p;
    },
    set: () => true,
    apply: () => p,
    construct: () => p,
  });
  return p;
}
const HOLE = blackhole();

// ---- minimal DOM ------------------------------------------------------
const elements = new Map();
function element(id) {
  if (!elements.has(id)) {
    elements.set(id, {
      id,
      textContent: "",
      value: "",
      checked: false,
      width: 800,
      height: 600,
      style: {},
      disabled: false,
      addEventListener: () => {},
      removeEventListener: () => {},
      getContext: () => HOLE,
      getBoundingClientRect: () => ({ left: 0, top: 0, width: 800, height: 600 }),
      appendChild: () => {},
      classList: { add: () => {}, remove: () => {}, toggle: () => {} },
    });
  }
  return elements.get(id);
}
const document = {
  getElementById: (id) => element(id),
  querySelector: (s) => element(s),
  querySelectorAll: () => [],
  createElement: (t) => element("created-" + t + "-" + elements.size),
  addEventListener: () => {},
  body: element("body"),
  documentElement: element("html"),
};

const sandbox = {
  Matter,
  document,
  console: { log: () => {}, warn: () => {}, error: () => {} },
  Math,
  JSON,
  performance: { now: () => Date.now() },
  requestAnimationFrame: () => 0,
  cancelAnimationFrame: () => {},
  setTimeout: () => 0,
  clearTimeout: () => {},
  setInterval: () => 0,
  clearInterval: () => {},
  navigator: { userAgent: "node" },
  location: { search: "", href: "" },
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  alert: () => {},
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
sandbox.window.addEventListener = () => {};
sandbox.window.innerWidth = 1200;
sandbox.window.innerHeight = 800;
vm.createContext(sandbox);

// ---- evaluate inline scripts, tolerating UI-block failures ------------
const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
let m;
let blocks = 0;
let failures = 0;
while ((m = re.exec(html)) !== null) {
  blocks += 1;
  try {
    vm.runInContext(m[1], sandbox, { filename: `${htmlPath}#script${blocks}` });
  } catch (e) {
    failures += 1;
    process.stderr.write(`script block ${blocks} failed: ${String(e).slice(0, 120)}\n`);
  }
}
if (typeof sandbox.objective !== "function") {
  process.stderr.write(`no objective() after ${blocks} blocks (${failures} failed)\n`);
  process.exit(2);
}
process.stderr.write(`ready: ${blocks} blocks, ${failures} tolerated failures\n`);

// ---- serve ------------------------------------------------------------
const rl = readline.createInterface({ input: process.stdin, terminal: false });
rl.on("line", (line) => {
  const s = line.trim();
  if (s === "EXIT") process.exit(0);
  if (!s) return;
  try {
    const u = JSON.parse(s);
    const v = sandbox.objective(u);
    process.stdout.write(JSON.stringify(Number(v)) + "\n");
  } catch (e) {
    process.stdout.write(JSON.stringify({ error: String(e).slice(0, 200) }) + "\n");
  }
});

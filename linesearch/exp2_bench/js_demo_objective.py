"""Python bridge to the full-fidelity JS demo objectives (exp2k).

Wraps js_objective_server.js: one persistent node process per demo,
JSON lines over pipes. The JS pages carry the real Matter.js physics
where several Python ports are reduced-order stand-ins.
"""

import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
APPS = "/Users/petercotton/github/humpday/docs/applications"

# demo -> (html file, n_dim of the page's decode(u))
JS_DEMOS = {
    "pool_js": ("pool.html", 3),
    "trebuchet_js": ("trebuchet.html", 4),
    "mini_golf_js": ("mini-golf.html", 3),
    "curling_js": ("curling.html", 4),
    "slingshot_js": ("slingshot.html", 3),
}


class JsObjective:
    def __init__(self, demo):
        html, self.n_dim = JS_DEMOS[demo]
        self.proc = subprocess.Popen(
            [
                "node",
                os.path.join(HERE, "js_objective_server.js"),
                os.path.join(APPS, html),
            ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        # wait for the ready line (or an early failure)
        line = self.proc.stderr.readline()
        if "ready" not in line:
            rest = self.proc.stderr.read()
            raise RuntimeError(f"{demo} server failed: {line}{rest}")

    def __call__(self, u):
        self.proc.stdin.write(json.dumps([float(x) for x in u]) + "\n")
        self.proc.stdin.flush()
        out = json.loads(self.proc.stdout.readline())
        if isinstance(out, dict):
            raise RuntimeError(f"js objective error: {out['error']}")
        return float(out)

    def close(self):
        try:
            self.proc.stdin.write("EXIT\n")
            self.proc.stdin.flush()
        except Exception:
            pass
        self.proc.terminate()


if __name__ == "__main__":
    import time

    import numpy as np

    for demo in JS_DEMOS:
        try:
            obj = JsObjective(demo)
            rng = np.random.default_rng(0)
            u = list(rng.uniform(0.2, 0.8, obj.n_dim))
            v1, v2 = obj(u), obj(u)
            t0 = time.time()
            n = 20
            for i in range(n):
                obj(list(np.random.default_rng(i).uniform(0.1, 0.9, obj.n_dim)))
            dt = (time.time() - t0) / n * 1000
            det = "deterministic" if v1 == v2 else f"NONDET ({v1} vs {v2})"
            print(f"{demo:14s} d={obj.n_dim} v={v1:10.4f} {det}  {dt:6.1f} ms/eval")
            obj.close()
        except Exception as e:
            print(f"{demo:14s} FAILED: {str(e)[:140]}")

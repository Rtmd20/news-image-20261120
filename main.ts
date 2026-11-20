// News-image entry (Node 22, standard library only).
//
// The front page itself is entry.png, drawn beside this file by draw.py
// (Python + Pillow, every letter rendered as text). This program does one
// thing: it places an exact copy of that image where the grader expects it.
// A plain copy is byte-for-byte deterministic, so two runs always agree.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));

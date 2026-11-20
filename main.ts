// news-image-20261119 entry (Node 22, standard library only).
// The program writes the image beside this file to the output directory
// make.fun grades: /output, or MAKEFUN_OUTPUT_DIR when run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// The image is entry.png, drawn by draw-image.py in this repository from
// six verified stories of Thursday 19 November 2026.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = new URL("./entry.png", import.meta.url);
copyFileSync(src, join(outDir, "entry.png"));

// news-image-20261118 — one-day world-news image entry.
//
// The entry itself is a pre-rendered PNG that sits next to this file
// (entry.png: the 18 November 2026 world-news summary, 1024x1024).
// This program only hands that file to the grader: it copies it to
// <output>/entry.png. Inside the grader the output directory is
// /output; anywhere else, point MAKEFUN_OUTPUT_DIR at a directory:
//
//   MAKEFUN_OUTPUT_DIR=./out node main.ts

import { copyFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ENTRY_NAME = 'entry.png';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

const source = join(dirname(fileURLToPath(import.meta.url)), ENTRY_NAME);
const destination = join(OUTPUT_DIR, ENTRY_NAME);

copyFileSync(source, destination);

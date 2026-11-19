import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const sourcePath = join(botDir, "POST.json");

const raw = readFileSync(sourcePath, "utf8");
const parsed = JSON.parse(raw) as unknown;
if (
  typeof parsed !== "object" ||
  parsed === null ||
  typeof (parsed as { url?: unknown }).url !== "string" ||
  ((parsed as { url: string }).url.length === 0)
) {
  throw new Error("POST.json must be a JSON object with a non-empty url field");
}

const targetPath = join(outDir, "POST.json");
mkdirSync(outDir, { recursive: true });
writeFileSync(targetPath, raw);
console.log(
  `Copied POST.json to ${targetPath} for ${(parsed as { url: string }).url}`,
);

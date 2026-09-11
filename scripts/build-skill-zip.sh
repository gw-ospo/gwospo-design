#!/bin/sh
# Rebuild gw-design-review.zip — the upload-ready package for claude.ai and any other
# client that installs skills from a ZIP.
#
# The archive must contain the skill folder at its root:
#
#     gw-design-review/SKILL.md
#     gw-design-review/references/...
#     gw-design-review/scripts/...
#
# SKILL.md any deeper than that is rejected with "the MD file must be in the top-level
# folder". That is why we do NOT ship the repository's own Download-ZIP for this purpose:
# GitHub wraps everything in gwospo-design-main/, putting SKILL.md four levels down.
#
# Run from the repository root:   sh scripts/build-skill-zip.sh

set -eu

SKILL_DIR=".claude/skills/gw-design-review"
OUT="gw-design-review.zip"

cd "$(dirname "$0")/.."

[ -f "$SKILL_DIR/SKILL.md" ] || { echo "error: $SKILL_DIR/SKILL.md not found" >&2; exit 1; }

rm -f "$OUT"

# Stage a clean copy so the archive root is the skill folder itself.
STAGE=$(mktemp -d)
trap 'rm -rf "$STAGE"' EXIT
cp -R "$SKILL_DIR" "$STAGE/gw-design-review"
find "$STAGE" -name '.DS_Store' -delete
find "$STAGE" -name '__MACOSX' -type d -exec rm -rf {} + 2>/dev/null || true

( cd "$STAGE" && zip -q -r -X "$OUT" gw-design-review )
mv "$STAGE/$OUT" "$OUT"

echo "Built $OUT"
unzip -l "$OUT"

# Fail loudly if the structure is ever wrong.
unzip -l "$OUT" | grep -q ' gw-design-review/SKILL.md$' || {
    echo "error: SKILL.md is not at gw-design-review/SKILL.md in the archive" >&2
    exit 1
}
echo "OK: SKILL.md is at the required depth."

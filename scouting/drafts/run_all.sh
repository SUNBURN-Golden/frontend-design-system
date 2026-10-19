#!/usr/bin/env bash
# 사이트 레포를 건드리지 않는 검증 묶음 (의존성은 이 레포의 tools 폴더/임시 폴더에만).
# 사용: ./run_all.sh NAME DIST_DIR [CSS_FILE]
# 환경: PY=playwright가 있는 파이썬(기본 python3), AXE=axe.min.js 경로, CHROME=시스템 크롬
set -u
NAME=${1:?name}; DIST=${2:?dist}; CSS=${3:-}
HERE=$(cd "$(dirname "$0")" && pwd)
PY=${PY:-python3}; AXE=${AXE:-/tmp/axe/node_modules/axe-core/axe.min.js}; CHROME=${CHROME:-/usr/bin/google-chrome}
OUT=${OUT:-/tmp/uxcheck/$NAME}; mkdir -p "$OUT"; FAIL=0
echo "== 1/4 static (stdlib) =="; python3 "$HERE/static_check.py" "$DIST" > "$OUT/static.json"; python3 - "$OUT/static.json" <<'PYEOF' || FAIL=1
import json,sys
d=json.load(open(sys.argv[1])); bad={k:v for k,v in d['html'].items() if not k.startswith('external-resource:') or True}
print('html findings:',bad or 'none'); sys.exit(1 if bad else 0)
PYEOF
echo "== 2/4 axe (light/dark x 390/1440) =="; $PY "$HERE/axe_audit.py" "$DIST" --axe "$AXE" --chrome "$CHROME" --port 0 > "$OUT/axe.txt" 2>&1 || FAIL=1; tail -3 "$OUT/axe.txt"
echo "== 3/4 first screen (5-second test, semi-auto) =="; $PY "$HERE/first_screen_audit.py" "$OUT/first-screen" "$NAME=$DIST" --chrome "$CHROME" > "$OUT/first_screen.txt" 2>&1 || FAIL=1; cut -c1-220 "$OUT/first_screen.txt"
if [ -n "$CSS" ] && [ -x "${STYLELINT:-}" ]; then echo "== 4/4 stylelint =="; "$STYLELINT" --config "$HERE/stylelint.config.mjs" --config-basedir "$(cd "$(dirname "$STYLELINT")/../.." && pwd)" "$CSS" || FAIL=1; else echo "== 4/4 stylelint skipped (set STYLELINT=path and pass CSS) =="; fi
echo "RESULT: $([ $FAIL = 0 ] && echo PASS || echo 'FAIL (see '$OUT')')"; exit $FAIL

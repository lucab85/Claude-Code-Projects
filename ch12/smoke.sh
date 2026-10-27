#!/usr/bin/env bash
# Smoke-test the Bookmarks API. Usage: ./smoke.sh [port]
BASE="http://localhost:${1:-8000}"
CT='content-type: application/json'
fail=0

check() {  # check LABEL EXPECTED_STATUS CURL_ARGS...
  local label=$1 want=$2; shift 2
  local got
  got=$(curl -s -o /dev/null -w '%{http_code}' "$@")
  if [ "$got" = "$want" ]; then echo "PASS  $label ($got)"
  else echo "FAIL  $label (expected $want, got $got)"; fail=1; fi
}

check "create"         201 -X POST "$BASE/bookmarks" -H "$CT" \
  -d '{"url":"https://example.com","title":"ex","tag":"misc"}'
check "bad url"        422 -X POST "$BASE/bookmarks" -H "$CT" \
  -d '{"url":"ftp://x","title":"ex","tag":"misc"}'
check "list"           200 "$BASE/bookmarks"
check "filter by tag"  200 "$BASE/bookmarks?tag=misc"
check "get 1"          200 "$BASE/bookmarks/1"
check "delete 1"       204 -X DELETE "$BASE/bookmarks/1"
check "missing"        404 "$BASE/bookmarks/1"
[ "$fail" = 0 ] && echo "RESULT: PASS" || { echo "RESULT: FAIL"; exit 1; }

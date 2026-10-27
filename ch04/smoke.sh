#!/usr/bin/env bash
# Smoke-test the Notes API. Usage: ./smoke.sh [port]
BASE="http://localhost:${1:-8000}"
CT='content-type: application/json'

check() {  # check LABEL EXPECTED_STATUS CURL_ARGS...
  local label=$1 want=$2; shift 2
  local got
  got=$(curl -s -o /dev/null -w '%{http_code}' "$@")
  if [ "$got" = "$want" ]; then echo "PASS  $label ($got)"
  else echo "FAIL  $label (expected $want, got $got)"; fi
}

check "create note"   201 -X POST "$BASE/notes" -H "$CT" \
  -d '{"title":"hi","body":"there"}'
check "blank title"   422 -X POST "$BASE/notes" -H "$CT" \
  -d '{"title":"   ","body":"x"}'
check "list notes"    200 "$BASE/notes"
check "search notes"  200 "$BASE/notes?q=hi"
check "get note 1"    200 "$BASE/notes/1"
check "update note 1" 200 -X PATCH "$BASE/notes/1" -H "$CT" \
  -d '{"body":"world"}'
check "delete note 1" 204 -X DELETE "$BASE/notes/1"
check "missing note"  404 "$BASE/notes/999"
echo "404 body: $(curl -s "$BASE/notes/999")"

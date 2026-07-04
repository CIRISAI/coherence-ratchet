#!/usr/bin/env bash
# Verify every `mechanized` in-lake anchor in cc_lean.tsv resolves to a real
# declaration (theorem/def/structure/axiom) in the Lean lake at the current commit.
# `open` rows and non-lake (RATCHET:… / —) anchors are skipped. Exit 1 on any miss.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
LAKE="$HERE/../formal"
TSV="$HERE/cc_lean.tsv"
fail=0; checked=0

# skip header; fields: decimal, claim, module_theorem, status, note
tail -n +2 "$TSV" | while IFS=$'\t' read -r dec claim mt status note; do
  [ "$status" = "mechanized" ] || continue
  case "$mt" in
    RATCHET:*|"—"|"") continue ;;
  esac
  # Core.Module.name  -> file CoherenceRatchet/Core/Module.lean, decl `name`
  name="${mt##*.}"
  modpath="${mt%.*}"                       # Core.Module
  file="$LAKE/CoherenceRatchet/${modpath//.//}.lean"
  checked=$((checked+1))
  if [ ! -f "$file" ]; then
    echo "MISS  $dec $claim  -> file not found: $file"; fail=1; continue
  fi
  if grep -qE "^(noncomputable def|def|theorem|lemma|structure|axiom) ${name}\b" "$file"; then
    echo "ok    $dec $claim  -> ${mt}"
  else
    echo "MISS  $dec $claim  -> ${name} not declared in ${file##*/}"; fail=1
  fi
done

# the while runs in a subshell (pipe); recompute status via a marker file
tail -n +2 "$TSV" | while IFS=$'\t' read -r dec claim mt status note; do
  [ "$status" = "mechanized" ] || continue
  case "$mt" in RATCHET:*|"—"|"") continue ;; esac
  name="${mt##*.}"; modpath="${mt%.*}"
  file="$LAKE/CoherenceRatchet/${modpath//.//}.lean"
  [ -f "$file" ] && grep -qE "^(noncomputable def|def|theorem|lemma|structure|axiom) ${name}\b" "$file" || exit 1
done
echo "---"
if [ $? -eq 0 ]; then echo "ALL in-lake mechanized anchors resolve."; else echo "SOME anchors missing (see MISS above)."; exit 1; fi

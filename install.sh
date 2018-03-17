#!/bin/bash -eu
SCRIPT_HOME="$(dirname "$0")"
cd "$SCRIPT_HOME"
KARABINER_ASSETS_DIR="$HOME/.config/karabiner/assets"
TEMP_DIR="$(mktemp -d)"
trap "rm -rf '$TEMP_DIR'" EXIT

CSON2JSON="$SCRIPT_HOME/node_modules/.bin/cson2json"
[[ -e "$CSON2JSON" ]] || npm install --save cson

cp -pr ./complex_modifications "$TEMP_DIR/complex_modifications"

for cson_file in "$TEMP_DIR"/complex_modifications/*.cson;do
  json_file="${cson_file%%.cson}.json"
  echo "convert $(basename $cson_file) -> $(basename $json_file)"
  $CSON2JSON $cson_file > $json_file
  rm $cson_file
done

rsync -auvr --delete "$TEMP_DIR/complex_modifications/" "$KARABINER_ASSETS_DIR/complex_modifications/"

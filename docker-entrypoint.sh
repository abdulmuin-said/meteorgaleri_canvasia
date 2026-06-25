#!/bin/sh
set -eu

APP_ROOT="/app"
PERSISTENT_ROOT="${PERSISTENT_ROOT:-/app/storage}"
APP_PORT="${PORT:-8080}"

mkdir -p \
  "$PERSISTENT_ROOT/uploads" \
  "$PERSISTENT_ROOT/img/products" \
  "$PERSISTENT_ROOT/media/products" \
  "$PERSISTENT_ROOT/App_Data" \
  "$PERSISTENT_ROOT/logs"

seed_directory() {
  source_dir="$1"
  target_dir="$2"

  if [ -d "$source_dir" ] && [ -z "$(ls -A "$target_dir" 2>/dev/null || true)" ]; then
    cp -a "$source_dir/." "$target_dir/"
  fi
}

link_directory() {
  link_path="$1"
  target_dir="$2"

  mkdir -p "$(dirname "$link_path")" "$target_dir"
  rm -rf "$link_path"
  ln -s "$target_dir" "$link_path"
}

# Railway volumes are mounted at runtime. Seed bundled files only when the
# persistent target is empty, then point mutable app folders at the volume.
seed_directory "$APP_ROOT/wwwroot/uploads" "$PERSISTENT_ROOT/uploads"
seed_directory "$APP_ROOT/wwwroot/img/products" "$PERSISTENT_ROOT/img/products"
seed_directory "$APP_ROOT/wwwroot/media/products" "$PERSISTENT_ROOT/media/products"
seed_directory "$APP_ROOT/App_Data" "$PERSISTENT_ROOT/App_Data"
seed_directory "$APP_ROOT/logs" "$PERSISTENT_ROOT/logs"

link_directory "$APP_ROOT/wwwroot/uploads" "$PERSISTENT_ROOT/uploads"
link_directory "$APP_ROOT/wwwroot/img/products" "$PERSISTENT_ROOT/img/products"
link_directory "$APP_ROOT/wwwroot/media/products" "$PERSISTENT_ROOT/media/products"
link_directory "$APP_ROOT/App_Data" "$PERSISTENT_ROOT/App_Data"
link_directory "$APP_ROOT/logs" "$PERSISTENT_ROOT/logs"

exec dotnet KanvasProje.Web.dll --urls "http://0.0.0.0:$APP_PORT"

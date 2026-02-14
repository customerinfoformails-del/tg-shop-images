#!/usr/bin/env zsh

ROOT="/Users/roma/Desktop/github_2/tg-shop-images/public/images"

cd "$ROOT" || exit 1

# Нормализация имени: пробелы -> -, _ -> -, lowercase
function normalize_name() {
  local name="$1"
  # пробелы и _ в -
  name="${name// /-}"
  name="${name//_/-}"
  # в lowercase
  name="${name:l}"
  echo "$name"
}

# 1. Файлы
find . -type f -print0 | while IFS= read -r -d '' f; do
  dir="${f:h}"
  base="${f:t}"
  new_base="$(normalize_name "$base")"

  if [[ "$base" != "$new_base" ]]; then
    tmp="$dir/.tmp_$$_$new_base"
    mv "$f" "$tmp"
    mv "$tmp" "$dir/$new_base"
    echo "file: $f -> $dir/$new_base"
  fi
done

# 2. Директории (сначала глубина!)
find . -depth -type d -print0 | while IFS= read -r -d '' d; do
  dir_parent="${d:h}"
  base="${d:t}"
  new_base="$(normalize_name "$base")"

  if [[ "$base" != "$new_base" ]]; then
    tmp="$dir_parent/.tmp_$$_$new_base"
    mv "$d" "$tmp"
    mv "$tmp" "$dir_parent/$new_base"
    echo "dir:  $d -> $dir_parent/$new_base"
  fi
done

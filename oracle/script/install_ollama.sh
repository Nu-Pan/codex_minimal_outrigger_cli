#!/bin/bash
set -euo pipefail

# ollama を `<repo-root>/.cmoc` ツリー内にインストールするスクリプト
# cmoc 開発者だけが実行するスクリプトであり、cmoc インターフェースではないため、oracle file 扱いとした。

# `<repo-root>` を解決
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"

# 定数
archive_path="/tmp/ollama-linux-amd64.tar.zst"
install_dir="$repo_root/.cmoc/local/ollama"

# 前提パッケージをインストール
sudo apt update
sudo apt install -y curl zstd ca-certificates

# ollama パッケージをダウンロード
curl -fsSL https://ollama.com/download/ollama-linux-amd64.tar.zst \
  -o "$archive_path"

# ollama パッケージを解凍
mkdir -p "$install_dir"
tar --zstd -xf "$archive_path" -C "$install_dir"

cat <<EOF
ollama を $install_dir にインストールしました。

実行ファイル:
  $install_dir/bin/ollama

現在の shell で使う場合:
  export PATH="$install_dir/bin:\$PATH"

確認:
  $install_dir/bin/ollama --version
EOF

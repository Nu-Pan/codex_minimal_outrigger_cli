# Ollama SLM Server

## 概要

- cmoc は ollama をローカル実行し、そこで SLM をサーブする
- cmoc はバックエンドモデルとして、このローカル SLM を選択出来る

## ollama のインストール方法

- 手順
    1. `<repo-root>/.cmoc/local/ollama/bin/ollama --version` が通るなら、インストールを中断（正常系）
    2. ollama archive を `https://ollama.com/download/ollama-linux-amd64.tar.zst` から取得し `/tmp/ollama-linux-amd64.tar.zst` に保存
    3. archive を `<repo-root>/.cmoc/local/ollama` へ展開
- 仕様
    - インストール処理は冪等性を持つこと
    - 各手順が要求する結果が既に存在する場合は、その手順をスキップする

## ollama の起動方法

- `<port>` は安全なポート番号の範囲内から乱数で決める
    - TODO もうちょっとマシな定義にする
- サーブするモデルの名前は `CmocConfigCodex.model[ModelClass.LOCAL_SLM]` から取得する
- TODO 起動のやりかたを書く (デーモンではない)

## ollama の使用方法

- cmoc から ollama へは `127.0.0.1:<port>` でアクセスする
- モデル名が未定義の状態で SLM バックエンドでの Codex CLI 実行を要求された場合はエラー終了

## ollama のインスタンス寿命管理

- ollama のインストール・起動は doctor preprocess で実行される (`<cmoc-root>/oracle/doc/app_spec/doctor_preprocess.md`)
- cmoc のプロセス終了時に ollama インスタンスも終了する
- `<repo-root>` 内で存在して良い ollama インスタンスは最大で 1 つだけ
- 並列実行時は 1 の ollama を複数の cmoc で共用する
- ollama の寿命管理
    - ollama が立ち上がっていない場合、最初に必要とした cmoc が ollama を立ち上げる
    - ollama を使用する cmoc が居なくなったら ollama をシャットダウンする
- TODO 冗長なのでスッキリさせる

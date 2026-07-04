# Ollama SLM Server

## 概要

- cmoc は ollama をローカル実行し、そこで SLM をサーブする
- cmoc はバックエンドモデルとして、このローカル SLM を選択出来る

## 設定のロード

- サーブするモデルの名前 `<slm-name>` は `CmocConfigCodex.model[ModelClass.LOCAL_SLM]` からロードする

## ollama のインストール方法

- 手順
    1. `<repo-root>/.cmoc/local/ollama/bin/ollama --version` が通るなら、インストールを中断（正常系）
    2. ollama archive を `https://ollama.com/download/ollama-linux-amd64.tar.zst` から取得し `/tmp/ollama-linux-amd64.tar.zst` に保存
    3. archive を `<repo-root>/.cmoc/local/ollama` へ展開
- 仕様
    - インストール処理は冪等性を持つこと
    - 各手順が要求する結果が既に存在する場合は、その手順をスキップする

## ollama の起動方法

- `<port>` の選び方
    - 49152 以上 65535 以下から選ぶ
    - 使用中の port は選ばない
    - 乱数で選択
- ollama は `<repo-root>/.cmoc/local/ollama/bin/ollama serve` を、デーモン化しない子プロセスとして起動する
- ollama の listen 先は `127.0.0.1:<port>` に限定する

## ollama の使用方法

- cmoc から ollama へは `127.0.0.1:<port>` でアクセスする
- Codex CLI に ollama を使わせる場合、cmoc が生成する codex profile に以下を設定する
    ```yaml
    model: <slm-name>
    model_provider: cmoc_ollama
    model_providers:
    cmoc_ollama:
        name: cmoc ollama
        base_url: http://127.0.0.1:<port>/v1
        wire_api: responses
    ```
- cmoc は `codex exec` の argv に `--oss` や `--local-provider` を指定しない
- cmoc は Codex CLI の組み込み `ollama` provider ID に依存しない

## ollama のインスタンス寿命管理

- ollama のインストール・起動は doctor preprocess で実行される (`<cmoc-root>/oracle/doc/app_spec/doctor_preprocess.md`)
- `<repo-root>` 内で存在して良い ollama インスタンスは最大で 1 つだけ
- 並列実行時は同じ `<repo-root>` の cmoc 間で 1 つの ollama インスタンスを共用する
- ollama が立ち上がっていない場合、最初に必要とした cmoc が起動する
- 同じ `<repo-root>` で ollama を使用する cmoc が居なくなったら ollama を終了する

# Ollama SLM Server

## 概要

- 設定が有効化されている場合、cmoc は ollama をローカル実行し、そこで SLM をサーブする
- cmoc は Codex CLI の model provider として、cmoc managed ollama を選択出来る

## ollama を利用可能にする方法

- 関数 `ensure_cmoc_managed_ollama` を正本とする

## Codex CLI からの ollama の使用方法

- cmoc から ollama へは `127.0.0.1:11434` でアクセスする
- `<slm-name>` は `CodexModelSpec.model` から読み出すこととする
- 生成する codex profile に以下を設定する TODO model_provider, model_providers が居るけどこれなんで？
    ```yaml
    model: <slm-name>
    model_provider: cmoc_managed_ollama
    model_providers:
    cmoc_managed_ollama:
        name: cmoc managed ollama
        base_url: http://127.0.0.1:11434/v1
        wire_api: responses
    ```
- cmoc は `codex exec` の argv に `--oss` や `--local-provider` を指定しない
- cmoc は Codex CLI の組み込み `ollama` provider ID に依存しない

## ollama のインスタンス寿命管理

- doctor preprocess で `ensure_cmoc_managed_ollama` を呼び出す

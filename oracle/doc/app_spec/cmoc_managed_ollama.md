# cmoc managed ollama

## 概要

- 設定が有効化されている場合、cmoc は ollama をローカル実行し、そこで SLM をサーブする
- cmoc は Codex CLI の model provider として、cmoc managed ollama を選択出来る

## 用語定義

- `CodexModelSpec.model` を `<slm-name>` とする

## cmoc managed ollama の検証

- cmoc managed ollama へのリクエストが通ること
- cmoc managed ollama が提供するモデルが `CmocConfigCodex.model` の要求を満たすこと
- 127.0.0.1:11434 を listen しているのが cmoc managed ollama であること
- cmoc managed ollama のサービスが起動していること

## ollama のサービス起動

- ollama archive は `https://ollama.com/download/ollama-linux-amd64.tar.zst` から取得する
- ollama archive は ollama 実行ファイルが `~/.cmoc/ollama/bin/ollama` に配置されるように展開する
- ollama はサービスとして起動する
    - サービス設定ファイルは `~/.config/systemd/user/cmoc-ollama.service`
    - サービスはユーザー空間で起動する (e.g. `systemctl --user enable --now cmoc-ollama`)

## ollama のモデル pull

- `CodexModelSpec` 上、cmoc managed ollama を model provider としている (i.e. `CodexModelSpec.model_provider=="cmoc"`) モデルは cmoc managed ollama で pull しなければならない
- cmoc managed ollama が pull したモデルの配置先は `~/.cmoc/ollama/models` とする

## Codex CLI からの ollama の使用方法

- cmoc から ollama へは `127.0.0.1:11434` でアクセスする
- Codex CLI 呼び出しの argv で以下を指定する
    ```text
    --model <slm-name>
    --config 'model_provider="cmoc_managed_ollama"'
    --config 'model_providers.cmoc_managed_ollama.name="cmoc managed ollama"'
    --config 'model_providers.cmoc_managed_ollama.base_url="http://127.0.0.1:11434/v1"'
    --config 'model_providers.cmoc_managed_ollama.wire_api="responses"'
    ```
- `--profile` (`-p`) を使って cmoc managed ollama の設定を注入してはならない
- cmoc は `codex exec` の argv に `--oss` や `--local-provider` を指定しない
- cmoc は Codex CLI の組み込み `ollama` provider ID に依存しない

## ollama の起動タイミング・条件

- `CodexModelSpec.model_provider=="cmoc"` が指定されている場合、cmoc は doctor preprocess で cmoc managed ollama を起動し、適切なモデルをロードする必要がある

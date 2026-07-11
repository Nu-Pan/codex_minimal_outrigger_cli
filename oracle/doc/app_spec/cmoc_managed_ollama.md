# cmoc managed ollama

## 概要

- 設定が有効化されている場合、cmoc は ollama をローカル実行し、そこで SLM をサーブする
- cmoc は Codex CLI の model provider として、cmoc managed ollama を選択出来る

## 実行主体

- cmoc 自身が Codex CLI の agent call を開始する前に cmoc managed ollama を準備・起動し、そのサービスを agent sandbox の外側で実行・検証する
- Codex agent の責務は cmoc managed ollama を model provider として利用することに限り、ollama の取得・配置、サービス管理、モデル pull、ダウンロード資源の管理、および GPU 推論の検証を担わせてはならない

## 用語定義

- `CodexModelSpec.model` を `<slm-name>` とする
- GPU 推論とは、モデルの推論計算の一部以上を GPU へ offload して実行することを指す。GPU の検出だけでは GPU 推論とはみなさない

## cmoc managed ollama の検証

- cmoc managed ollama へのリクエストが通ること
- cmoc managed ollama が提供するモデルが `CmocConfigCodex.model` の要求を満たすこと
- 127.0.0.1:11434 を listen しているのが cmoc managed ollama であること
- cmoc managed ollama のサービスが起動していること
- 使用するモデルが GPU 推論を行っていることを、cmoc managed ollama の実行時情報から確認できること

## ollama のサービス起動

- ollama archive の取得が必要な場合は `https://ollama.com/download/ollama-linux-amd64.tar.zst` から取得する
- ollama archive は ollama 実行ファイルが `~/.cmoc/ollama/bin/ollama` に配置されるように展開する
- ollama はサービスとして起動する
    - サービス設定ファイルは `~/.config/systemd/user/cmoc-ollama.service`
    - サービスはユーザー空間で起動する (e.g. `systemctl --user enable --now cmoc-ollama`)

## ダウンロード資源の永続化

- ollama 実行ファイル、pull 済みモデル、および cmoc managed ollama の動作に必要なその他のダウンロード資源は `~/.cmoc/ollama` 配下に永続化する
- ダウンロード前に永続化済みの資源を検証し、要求を満たす場合は再利用する
- 資源のダウンロードは、要求を満たす資源が存在しない場合に限る。cmoc の実行間、テストケース間、および pytest の実行間で資源を再利用し、実行ごとにダウンロードしてはならない
- cmoc の run 終了処理およびテストの終了処理で、永続化したダウンロード資源を削除してはならない

## ollama のモデル pull

- `CodexModelSpec` 上、cmoc managed ollama を model provider としている (i.e. `CodexModelSpec.model_provider=="cmoc"`) モデルを新たに取得する場合は、cmoc managed ollama で pull しなければならない
- cmoc managed ollama が pull したモデルの配置先は `~/.cmoc/ollama/models` とする

## GPU 推論

- cmoc managed ollama は GPU 推論を行わなければならない
- GPU 推論ができない場合に CPU のみの推論へ切り替えてはならない
- 使用可能な GPU がない場合、使用するモデルの推論計算が GPU へ offload されない場合、または GPU 推論を確認できない場合は、Codex CLI からの推論リクエストを開始せずエラー終了する

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

# cmoc managed ollama

## 概要

- cmoc managed ollama は、cmoc がユーザー空間で管理し、ローカルで SLM をサーブする OS ユーザーごとに 1 つのサービスである
- 本番実行とテストは同じ cmoc managed ollama を共有する
- cmoc は Codex CLI の model provider として、cmoc managed ollama を選択出来る

## 用語定義

- `CodexModelSpec.model` を `{{slm-name}}` とする
- テスト用 SLM は `qwen3:4b-instruct-2507-q4_K_M` とする
- モデルをロードするとは、必要ならモデルを pull したうえで、そのモデルを使う推論リクエストを cmoc managed ollama に行い、実行時情報から GPU 推論を確認できる状態にすることを指す
- GPU 推論とは、モデルの推論計算の一部以上を GPU へ offload して実行することを指す。GPU の検出だけでは GPU 推論とはみなさない

## 管理主体・ライフサイクル

- cmoc 自身が cmoc managed ollama を準備・起動し、そのサービスを Codex agent sandbox の外側で実行・検証する
- Codex agent は cmoc managed ollama を model provider として利用するだけとし、ollama の取得・配置、サービス管理、モデル pull、ダウンロード資源の管理、および GPU 推論の検証を担わない
- cmoc managed ollama のライフサイクルは個々の cmoc run およびテストから独立させる
- cmoc run の終了処理およびテストの終了処理で、サービスを停止または disable したり、永続化したダウンロード資源を削除したりしてはならない
- サービスが異常終了した場合は user systemd が再起動する
- WSL または user systemd の停止に伴うサービス終了は許容し、次に必要となった時点で cmoc が再び利用可能性を保証する
- サービスを継続実行することは、使用後もモデルを GPU メモリに無期限でロードし続けることを意味しない

## サービスとダウンロード資源

- サービス設定ファイルは `~/.config/systemd/user/cmoc-ollama.service` とする
- サービスは user systemd で enable し、起動する (e.g. `systemctl --user enable --now cmoc-ollama`)
- ollama archive の取得が必要な場合は `https://ollama.com/download/ollama-linux-amd64.tar.zst` から取得する
- ollama 実行ファイルは `~/.cmoc/ollama/bin/ollama` に配置する
- ollama 実行ファイル、pull 済みモデル、および cmoc managed ollama の動作に必要なその他のダウンロード資源は `~/.cmoc/ollama` 配下に永続化する
- cmoc managed ollama が pull したモデルの配置先は `~/.cmoc/ollama/models` とする
- `CodexModelSpec.model_provider=="cmoc"` のモデルを新たに取得する場合は、cmoc managed ollama で pull する

## preflight のプロセス間排他

- cmoc managed ollama の preflight は、`~/.cmoc/ollama/lock` の排他的 lock により、同じ OS ユーザーの cmoc process 間で直列化する
- Codex agent sandbox 内から cmoc がこの lock file を操作する command を実行する場合は、最初の実行から sandbox 外実行の承認を得る

## 利用可能性の保証

- doctor preprocess の cmoc managed ollama service 起動保証処理は、`CmocConfig.cmoc_managed_ollama_service_launch_behavior` によって挙動を切り替える。各設定値の詳細は同メンバーのコメントを正本とする
- 起動保証処理を実行する場合は、本番実行とテストのどちらからでも繰り返し実行可能とし、以下を満たす状態へ必要な修復を行う
    - サービスが起動していること
    - 127.0.0.1:11434 を listen しているのが cmoc managed ollama であること
    - `CodexModelSpec.model_provider=="cmoc"` の使用対象モデルとテスト用 SLM がロードされていること
    - ロード対象モデルを使う cmoc managed ollama へのリクエストが通ること
    - ロード対象モデルが GPU 推論を行っていることを、cmoc managed ollama の実行時情報から確認できること
- テスト用 SLM は、`CmocConfigCodex.model` で指定されているかどうかに関わらず、起動保証処理で必ずロードする
- 要求を満たすサービスとダウンロード資源が既に存在する場合は、cmoc の実行間、テストケース間、および pytest の実行間で再利用し、実行ごとの再起動、再ダウンロード、または再度の pull をしてはならない
- サービスの新規構築・修復およびダウンロード資源の取得・修復は、既存のものが要求を満たさない場合に限る
- 使用可能な GPU がない場合、ロード対象モデルの推論計算が GPU へ offload されない場合、または GPU 推論を確認できない場合は、CPU のみの推論へ切り替えず、Codex CLI からの推論リクエストを開始する前にエラー終了する

## Codex CLI からの ollama の使用方法

- cmoc から ollama へは `127.0.0.1:11434` でアクセスする
- Codex CLI 呼び出しの argv で以下を指定する
    ```text
    --model {{slm-name}}
    --config 'model_provider="cmoc_managed_ollama"'
    --config 'model_providers.cmoc_managed_ollama.name="cmoc managed ollama"'
    --config 'model_providers.cmoc_managed_ollama.base_url="http://127.0.0.1:11434/v1"'
    --config 'model_providers.cmoc_managed_ollama.wire_api="responses"'
    ```
- `--profile` (`-p`) を使って cmoc managed ollama の設定を注入してはならない
- cmoc は `codex exec` の argv に `--oss` や `--local-provider` を指定しない
- cmoc は Codex CLI の組み込み `ollama` provider ID に依存しない
- Codex sandbox から `127.0.0.1:11434` へ接続するための argv は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` のネットワークアクセス仕様を正本とする

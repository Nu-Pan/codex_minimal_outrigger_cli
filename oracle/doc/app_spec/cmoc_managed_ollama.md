# cmoc managed ollama

## 概要

- cmoc managed ollama は、cmoc がユーザー空間で管理し、ローカルで SLM をサーブする OS ユーザーごとに 1 つのサービスである
- 本番実行とテストは同じ cmoc managed ollama を共有する
- cmoc は Codex CLI の model provider として、cmoc managed ollama を選択出来る

## 用語定義

- `CodexModelSpec.model` を `{{slm-name}}` とする
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

- `CodexModelSpec.model_provider=="cmoc"` のモデルを 1 つ以上使用する場合、cmoc は managed Ollama の状態確認・修復を始める前に、`~/.cmoc/ollama/lock` でプロセス間の排他的 advisory lock を取得する
- lock file は書き込み可能な状態で作成または open する必要がある。サービスとダウンロード資源が既に要求を満たしている場合も、lock の取得を省略してはならない
- 別の cmoc process が lock を保持している場合、後続 process は access failure とせず、先行する preflight が lock を解放するまで待機する
- lock は preflight の完了まで保持し、ollama の配置、サービス設定・起動・修復、待受と API の確認、およびモデルの pull・load・GPU 推論確認を、同じ OS ユーザーの cmoc process 間で直列化する
- lock の目的は、複数の cmoc process が同じサービスや永続資源を同時に変更したり、別 process による修復途中の状態を検証したりすることを防ぐことである。lock file の存在は、サービスの利用可能性や lock の取得状態を表すものではない
- lock は file descriptor の close または process の終了により解放される。通常の解放操作として lock file を削除してはならない
- この lock が直列化するのは、同じ lock を使用する cmoc の preflight に限る。preflight 完了後の推論 request や、cmoc を介さない直接のサービス操作は対象外とする
- Codex agent sandbox 内からこの lock を取得し得る cmoc command を起動する場合は、通常 sandbox 内での失敗を待たず、その command の最初の実行から sandbox 外実行の承認を得る。これは OS の root 権限を与えることではなく、cmoc の管理領域、user systemd、local service、および GPU を Codex agent sandbox の外側から利用させるための承認である
- テスト実行時の承認と結果報告の規則は `{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` を正本とする

## 利用可能性の保証

- `CodexModelSpec.model_provider=="cmoc"` の場合、cmoc は Codex CLI の agent call を開始する前に、doctor preprocess で cmoc managed ollama の利用可能性を保証する
- 利用可能性の保証は本番実行とテストのどちらからでも繰り返し実行可能とし、以下を満たす状態へ必要な修復を行う
    - サービスが起動していること
    - 127.0.0.1:11434 を listen しているのが cmoc managed ollama であること
    - 使用するモデルが `CmocConfigCodex.model` の要求を満たすこと
    - cmoc managed ollama へのリクエストが通ること
    - 使用するモデルが GPU 推論を行っていることを、cmoc managed ollama の実行時情報から確認できること
- 要求を満たすサービスとダウンロード資源が既に存在する場合は、cmoc の実行間、テストケース間、および pytest の実行間で再利用し、実行ごとの再起動、再ダウンロード、または再度の pull をしてはならない
- サービスの新規構築・修復およびダウンロード資源の取得・修復は、既存のものが要求を満たさない場合に限る
- 使用可能な GPU がない場合、使用するモデルの推論計算が GPU へ offload されない場合、または GPU 推論を確認できない場合は、CPU のみの推論へ切り替えず、Codex CLI からの推論リクエストを開始する前にエラー終了する

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

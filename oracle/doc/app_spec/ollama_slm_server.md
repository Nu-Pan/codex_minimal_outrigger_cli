# Ollama SLM Server

- SLM はローカル実行の ollama でサーブされる
- ollama と SLM は `cmoc doctor` でインストールされる
    - モデル名が未定義の場合は SLM をインストールせずに正常終了
- cmoc から ollama へは `127.0.0.1:<port>` でアクセスする
- `<port>` は安全なポート番号の範囲内から乱数で決める
- サーブするモデルの名前は `CmocConfigCodex.model[ModelClass.LOCAL_SLM]` から取得する
- モデル名が未定義の状態で SLM バックエンドでの Codex CLI 実行を要求された場合はエラー終了
- 並列実行時は 1 の ollama を複数の cmoc で共用する
- ollama の寿命管理
    - ollama が立ち上がっていない場合、最初に必要とした cmoc が ollama を立ち上げる
    - ollama を使用する cmoc が居なく鳴ったら ollama をシャットダウンする

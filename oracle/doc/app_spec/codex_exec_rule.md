# `codex exec` 呼び出し規約

## 基本

- cmoc からの Codex CLI 呼び出しは、原則として `codex exec` で行う
- 個別の `codex exec` 呼び出しの仕様は `<cmoc-root>/oracle/src/acp/builder` ツリー内の AgentCallParameter builder を正本とする

## プロンプトの渡し方

- run_codex_exec() は、プロンプト本文を argv に載せてはならない
- プロンプト本文は stdin 経由 (`codex exec -`) で渡す
- argv に載せてよいのは、フラグ、短い固定文字列、短いファイルパスのみとする

## codex profile

- cmoc は Codex CLI 呼び出し前に `<cmoc-root>/.codex/cmoc_<hash>.config.toml` を動的に生成する
- cmoc は `codex exec --profile "<cmoc-root>/.codex/cmoc_<hash>.config.toml"` の形式で、動的に生成した codex profile を指定する
- `<cmoc-root>/.codex/cmoc_<hash>.config.toml` の内容は cmoc 側の設定 (e.g. `AgentCallParameters`, `CmocConfig`, ...) から一意に決まる
- `<hash>` は `cmoc_<hash>.config.toml` 本文の SHA256 ハッシュとする

## ファイルアクセス制限

- Codex CLI に対するファイルアクセス制限の設定は codex profile 経由で行う
- 具体的な設定は AgentCallParameter builder を正本とする
- cmoc はファイルアクセス制限についての情報をプロンプトとして注入して Codex CLI に知らせる

## Model, Reasoning Effort

- Codex CLI に対する Model, Reasoning Effort の設定は codex profile 経由で行う
- 具体的な設定は AgentCallParameter builder を正本とする
- cmoc は Model, Reasoning Effort 設定についての情報を Codex CLI プロンプトに注入しない

## Codex CLI 呼び出し情報の保存

- Codex CLI 呼び出しに関する情報は `<repo-root>/.cmoc/log/codex/<time-stamp>_call.json` に保存すること
- `<time-stamp>_stdout.jsonl`, `<time-stamp>_stderr.log`, `<time-stamp>_output.json` に残らない情報だけを `<time-stamp>_call.json` に書くこと
- 同一の Codex CLI 呼び出しの間で `<time-stamp>` は一致しなければならない

## stdout, stderr の扱い

- `--json` を必ず指定すること
- stdout は `<repo-root>/.cmoc/log/codex/<time-stamp>_stdout.jsonl` に出力すること
- stderr は `<repo-root>/.cmoc/log/codex/<time-stamp>_stderr.log` に出力すること
- stdout, stderr をコンソールには流さないこと

## `--output-last-message`

- `--output-last-message <repo-root>/.cmoc/log/codex/<time-stamp>_output.json` を必ず指定すること
- cmoc が Codex CLI の作業結果を取り出す必要がある場合、`<time-stamp>_output.json` から読み出すこと

## Structured Output

- Codex CLI に Structued Output を要求する場合は、必ず `--output-schema` を使うこと
- `--output-schema` を使わずにプロンプト上だけで JSON 出力を要求するのは禁止
- スキーマは、一度 `<work-root>/.cmoc/state/scehma/<hash>.json` に保存して、これを Codex CLI に参照させること
- `<hash>` は schema 本文の SHA256 ハッシュとする
- Structued Output の結果は cmoc 側でも機械的検証を行うこと

## `codex exec` の並列呼び出し

- fork-join 的な並列化が可能な場合は `codex exec` を並列実行しても良い
- ただし、最大並列数は `CmocConfig.num_parallel` で制限すること

## `codex exec` が失敗した場合

### 基本的な考え方

- 異常な状態に基づいた無駄な作業によるトークンの浪費を避けたい
- quota 不足で停止した場合は quota が復活するまで待機・再開してほしい
- OpenAI サーバー側の一時的な問題であることが明白な既知のエラーなら、自動的にリトライしてほしい

### レスポンスの意味的な失敗

- Codex CLI のレスポンスが満たすべき要件を満たせていなかった場合
    - e.g. Structured Output のパース失敗
- 2 回までリトライする
- リトライの間隔を開ける必要は無い
- リトライが全て失敗したら、続行しようとせずに即時コマンド全体を失敗させる

### quota 枯渇・レートリミットで停止した場合

- quota が枯渇して Codex CLI の実行が停止した場合、再び実行可能な状態になるまで待機し、再開する
- quota が枯渇とは
    - e.g. 5h limit が枯渇して credits も無い
    - e.g. weekly limit が枯渇して credits も無い
- 再び実行可能な状態とは
    - e.g. 5h limit がリセットされて、元々 weekly limit も残っていたので、実行可能になった
    - e.g. 人間が credits を追加購入した
- 待機とは
    - 動作確認用のミニマルな Codex CLI 呼び出しを定期的に繰り返し実行する（ポーリング待機）
    - 動作確認の間隔は 30 分に１回とする
- 並列に呼び出した Codex CLI 呼び出しが同時に待機に突入した場合
    - 一番最初に待機に入ったスレッドだけが代表してポーリングを行う
    - 複数スレッドで並列にポーリングを行うのは禁止
- 再開とは
    - 停止した時のセッションを `codex exec ... resume ...` サブコマンドで復元したうえで、全く同じプロンプトで実行する
- quota 枯渇の判定方法
    - `codex exec --json` の stdout JSONL に、以下のいずれかが含まれている場合
        - `{"type":"error","message":"...Quota exceeded..."}`
        - `{"type":"turn.failed","error":{"message":"...Quota exceeded..."}}`
        - `{"type":"error","message":"...You've hit your usage limit..."}`
        - `{"type":"turn.failed","error":{"message":"...You've hit your usage limit..."}}`
        - `{"type":"error","message":"...out of credits.."}`
        - `{"type":"turn.failed","error":{"message":"...out of credits..."}}`
        - `{"type":"error","message":"...You hit your spend cap..."}`
        - `{"type":"turn.failed","error":{"message":"...You hit your spend cap..."}}`
- ユーザー向けメッセージについて
    - quota 枯渇による待機を行う場合、進捗をユーザーに表示すること
    - e.g. quota が枯渇して待機モードに入ったことを表示する
    - e.g. 動作確認のための Codex CLI 実行を行ったことと、その結果を表示する
    - e.g. quota が復活して処理を再開したことを表示する

### サーバーの一時的不調で失敗した場合

- `codex exec --json` の stdout JSONL に、以下のいずれかが含まれている場合
    - `{"type":"error", "message": "...Selected model is at capacity..."}`
    - `{"type":"turn.failed", "error":{"message": "...Selected model is at capacity..."}}`
- 8 回までリトライする
- リトライの間隔は 5 sec を初期値として、リトライ失敗 1 回毎に間隔を倍に増やす
- リトライが全て失敗したら、続行しようとせずに即時コマンド全体を失敗させる

### それ以外の想定外のエラー

- 続行しようとしない
- 即時コマンド全体を失敗させる

## `.agents` 配下を編集出来ない問題

- `.agents` ツリー内 Codex CLI で特別扱いされているため、人間が個別に approve しないと編集出来ない
- `codex exec` は個別の approve が出来ないので `<repo-root>/.agents` 配下は絶対に編集できない（やろうとしても失敗する）
- `.agents` ツリー内編集は cmoc としても禁止とする

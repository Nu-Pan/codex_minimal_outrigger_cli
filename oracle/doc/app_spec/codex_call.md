# Codex CLI 呼び出し規約

## 基本

- cmoc からの Codex CLI 呼び出しは、すべて `codex exec` で行う
- プロンプトの構築には `build_complete_prompt` を使用すること

## Codex CLI へのプロンプトの渡し方

- run_codex_exec() は、プロンプト本文を argv に載せてはならない
- プロンプト本文は stdin 経由 (`codex exec -`) で渡す
- argv に載せてよいのは、フラグ、短い固定文字列、短いファイルパスのみとする

## codex profile

- cmoc は Codex CLI 呼び出し前に `<cmoc-root>/.codex/cmoc_<uuid>.config.toml` を動的に生成する
- cmoc は `codex exec --profile "<cmoc-root>/.codex/cmoc_<uuid>.config.toml"` の形式で、動的に生成した codex profile を指定する
- `<cmoc-root>/.codex/cmoc_<uuid>.config.toml` の内容は `AgentCallParameters`, `CmocConfig` cmoc 側の設定から一意に決まる
- `<uuid>` は `cmoc_<uuid>.config.toml` 本文の sha256 ハッシュ値とする

## ファイルアクセス制限

- Codex CLI に対するサンドボックス的なファイルアクセス制限は codex profile 経由で行う
- 具体的なファイルアクセス制限設定は `FileAccessMode` から動的生成する
- それに加えて、 cmoc はファイルアクセス制限についての説明をプロンプトとして注入して Codex CLI に知らせる

## Model, Reasoning Effort

- Codex CLI に対する Model, Reasoning Effort 設定は codex profile 経由で行う
- 具体的なファイルアクセス制限設定は `CmocConfigCodex.model`, `CmocConfigCodex.reasoning_effort` から動的生成する
- cmoc はファイルアクセス制限についての説明を Codex CLI プロンプトに注入しない


## サンドボックスモード

- `<work-root>` への書き込みが不要であることが明確な場合
    - `codex` の引数からサンドボックスモードを読み取り専用に設定する
- それ以外の場合
    - `codex` の引数からサンドボックスモードをリポジトリ書き込み可に設定する

## Codex CLI の出力方法

- `--json` を必ず
- `--output-last-message` を必ず使うこと
    - 出力先として `<repo-root>/.cmoc/logs/codex_exec/output_last_message/<time-stamp>.json` を使用すること
- Codex CLI に Structued Output を要求する場合は、必ず `--output-schema` を使うこと
    - 「プロンプト上で JSON 出力を要求して、それをパースする」のは NG
    - Codex CLI に渡すスキーマを動的に生成する必要がある場合は、中間ファイルとして `<repo-root>/.cmoc/logs/codex_exec/output_schema/<schema-hash>.log` を使うこと
    - `<schema-hash>` とは、スキーマ本文から計算した SHA-256 ハッシュである
    - ハッシュの一致＝ファイル内容の一致とみなし、中間ファイルは可能な限り再利用すること（中間ファイルをキャッシュ的に用いること）
    - Structued Output の結果は cmoc 側でも機械的検証を行うこと

## `codex exec` 呼び出しログ

- `codex exec` の呼び出しと１：１で対応するフルログをファイルに出力すること
- ファイルの出力先は `<repo-root>/.cmoc/logs/codex_exec/call/<time-stamp>.md` とする
- フォーマットは markdown で、その呼び出し自体についての情報は YAML Front Matter に、入出力は本文に記録する
- このフルログファイルは事後調査用の証跡としての利用を想定する

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

## 言語

### 原則

- Codex CLI で取り扱う自然言語的な部分は、原則として日本語とする
- e.g.
    - 入力プロンプト
    - 作業レポート
    - レビューレポート
    - INDEX.md の Summary / Read this when / Do not read this when
    - エラーの説明・次に取るべきアクション
    - Codex CLI によるレビュー結果・調査結果の文章部分

### 例外

- 個別の仕様に言語指定がある場合はそちらに従う
- 個別の仕様として識別子が規定されている場合はそちらに従う
    - e.g. Structured Output の schema として定義されているキー名
- 元々が英語のワードは、英語のままで良い
    - e.g. コード識別子、ファイルパス、コマンドライン、JSON schema のキー、ログ原文、引用文、…
- LLM 内の思考言語 (e.g. reasoning 時の言語) のように、人間が直接読む想定ではない部分は自由にして良い

## `.agents` 配下を編集出来ない問題

- `.agents` 配下は Codex CLI で特別扱いされているため、人間が個別に approve しないと編集出来ない
- `codex exec` は個別の approve が出来ないので `<repo-root>/.agents` 配下は絶対に編集できない（やろうとしても失敗する）
- この問題については cmoc から `codex exec` に渡すプロンプトで工夫することで問題を緩和する（前述）

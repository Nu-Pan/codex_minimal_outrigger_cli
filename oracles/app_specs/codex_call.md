# Codex CLI 呼び出し規約

## 基本

- cmoc からの Codex CLI 呼び出しは、すべて `codex exec` で行う

## Codex CLI に渡すプロンプトの規約

### 構成

プロンプトは以下の構成に従うこと

1. エージェントのロール
    - e.g. あなたは `ProjectHoge` の開発チームの一員で、レビューを担当します。
2. かいつまんだ作業内容
    - e.g. git ブランチ `cmoc_2026-05-10_22-21-10` の変更内容をレビューしてください。
3. 作業完了条件
    - e.g. レビューの結果として、致命的な要修正項目の有無と、必要な修正内容を報告したら完了です。
4. 詳細な作業内容（自由記述・任意）
    - e.g. レビュー観点については `/path/to/review/instruction.md` を読んでください。...
    - e.g. 要修正項目のリストは Structured Output で返してください

## cmoc 知識注入の禁止

- `<cmoc-root>`, `<repo-root>` などの cmoc 仕様特有のワード・概念は使わないこと
    - ファイル・ディレクトリ・ブランチなどを指定する場合は、必ず具体的なパスをプロンプトに埋め込む
    - e.g.
        - NG: `<repo-root>` の実装を `<repo-root>/oracles` に追従させてください。
        - OK: `/path/to/repositry/root` の実装を `/path/to/repositry/root/oracles` に追従させてください
- 呼び出された AI エージェントが、プロンプトの情報だけから自走開始出来ること
    - e.g. AI エージェントが「自分は cmoc から呼び出されたエージェントであるというメタ認知」を持っていないと成立しないようなプロンプトは NG
- 特定のリポジトリに依存しない、汎用的な内容であること
    - e.g. cmoc の作業対象環境に特定のスキルが実装されていることを前提としたプロンプトは NG

## アクセス制限指示

ファイルシステムのアクセス制限指示を含める事

- 読み取り専用 (i.e. `--sandbox read-only`) で実行する場合
    - e.g. `<repo-root>/memo` などの読み書き禁止ルールを指示に含める
- 書き込み可能 (i.e. `--sandbox workspace-write`) で実行する場合
    - e.g. `<repo-root>/oracles` 編集禁止は必ず含める
    - e.g. `<repo-root>/.agents` 編集禁止は必ず含める

## Model, Reasoning Effort

- Code CLI 呼び出し時に Model, Reasoning Effort を必ず指定すること
    - Model: `--model <model>`
    - Reasoning Effort: `-c 'model_reasoning_effort="<reasoning-effort>"'`
- Model, Reasoning Effort の設定は、以下の原則に従って AI が裁量で決めて良い
    - Reasoning Effort = xhigh, high は使用禁止 
    - 特定の条件に当てはまらない場合はフロンティアモデル (e.g. GPT-5.5) の Reasoning Effort = medium を使う
    - 結果の品質がさほど重要ではなく繰り返し色が強い作業 (e.g. `INDEX.md` の内容生成) は、コストパフォーマンス重視モデル (e.g. GPT-5.4-mini) の Reasoning Effort = medium を使う
    - 疎通確認などの本当に全く結果の品質が重要ではない場合は、コストパフォーマンス重視モデル (e.g. GPT-5.4-mini) の Reasoning Effort = low を使う

## サンドボックスモード

- `<repo-root>` への書き込みが不要であることが明確な場合
    - `codex` の引数からサンドボックスモードを読み取り専用に設定する
- それ以外の場合
    - `codex` の引数からサンドボックスモードをリポジトリ書き込み可に設定する

## Codex CLI の出力方法

- `--json`, `--output-last-message <path>` を必ず使うこと
- Codex CLI に Structued Output を要求する場合は、必ず `--output-schema <schema.json>` を使うこと
    - 「プロンプトで JSON を要求してそれをパースする」のは NG
    - Structued Output の結果は cmoc 側でも機械的検証を行うこと

## `codex exec` 呼び出しフルログ

- `codex exec` 呼び出しのフルログは `<repo-root>/.cmoc/logs/codex_exec/<time-stamp>.log` に保存する

## `codex exec` が失敗した場合

### 基本的な考え方

- 異常な状態に基づいた無駄な作業によるトークンの浪費を避けたい
- quota 不足で停止した場合は quota が復活するまで待機・再開してほしい

### レスポンスの意味的な失敗

- Codex CLI のレスポンスが満たすべき要件を満たせていなかった場合
    - e.g. Structured Output のパース失敗
- 2 回までリトライする
- リトライが全て失敗したら、続行しようとせずに即時コマンド全体を失敗させる

### quota 不足で停止した場合

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
    - 停止した時のセッションを `--resume` で復元したうえで、全く同じプロンプトで実行する
- ユーザー向けメッセージについて
    - quota 枯渇による待機を行う場合、進捗をユーザーに表示すること
    - e.g. quota が枯渇して待機モードに入ったことを表示する
    - e.g. 動作確認のための Codex CLI 実行を行ったことと、その結果を表示する
    - e.g. quota が復活して処理を再開したことを表示する

### それ以外の想定外のエラー

- 続行しようとしない
- 即時コマンド全体を失敗させる

## 言語

### 原則

- Codex CLI で取り扱う自然言語的な部分は、原則として日本語とする
- e.g.
    - 入力プロンプト
    - 作業レポート
    - 評価レポート
    - INDEX.md の Summary / Read this when / Do not read this when
    - エラーの説明・次に取るべきアクション
    - Codex CLI によるレビュー結果・調査結果の文章部分

## 例外

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

# `acp`

## Summary
- cmoc が AI agent を呼び出すために渡すプロンプト本文、補助文脈、ファイルアクセス制約、モデル種別、reasoning effort、Structured Output 契約を定める正本仕様群への入口。
- 用途別の agent 呼び出しパラメータと、複数用途で共通注入されるプロンプト部品を扱い、レビュー、apply fork 後の確認・修正支援、INDEX.md エントリー生成、セッション合流時の conflict 解消、TUI 実行前のパラメータ選定へ分岐する。
- 実際の CLI 制御、git 操作、端末 UI、永続状態更新ではなく、それらの処理から呼ばれる AI agent に何を渡し、どの形式の応答を期待するかを確認するための階層。

## Read this when
- cmoc の機能が AI agent を呼び出す際の role、summary、goal、補助 prompt、ファイルアクセスモード、モデル種別、reasoning effort、出力 schema の正本値を確認したいとき。
- oracle review の所見列挙・擁護・反証・採否判定・マージ、apply fork の所見列挙・整理・対応・変更要約、INDEX.md エントリー生成、session join の conflict 解消、TUI 実行前のパラメータ選定について、呼び出し入力と応答契約を調べたいとき。
- agent に共通注入されるファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、oracle standard、realization standard、review standard、apply review standard、INDEX.md entry standard のプロンプト本文や注入条件を確認したいとき。
- 新しい AI agent 呼び出し仕様を追加する前に、既存の用途別パラメータ構築と共通プロンプト部品の責務分担、依存関係、Structured Output schema との接続を把握したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド全体の制御フロー、fork 作成、ブランチ操作、merge 実行、差分取得、端末 UI 描画、永続状態更新など、AI 呼び出しパラメータ以外の実処理を調べたいとき。
- 実装ファイルやテストにおける具体的な関数、状態ファイル形式、git command 実行手順、パッチ生成手順、UI 表示を探しているとき。
- 個別の oracle file 本文を読んで、具体的な仕様判断、レビュー所見、変更方針、conflict 解消内容、INDEX.md エントリー文面そのものを考えたいとき。
- path keyword、repo root、work root、StructDoc、AgentCallParameter など、プロンプト構築で参照される基礎データ構造やパス解決モデル自体の定義を確認したいとき。

## hash
- 3a0d8ab92a291f8e9f363aebc6d7847c9172446dab503dea89d717fc29556e3c

# `basic`

## Summary
- cmoc の oracle source のうち、複数領域から参照される基礎的な型・変換・文書生成 helper をまとめる領域。エージェント呼び出し条件の抽象モデル、ルートトークン付きパス表記と実パス解決、規範断片を表すモデル、構造化文書を Markdown へ描画する処理への入口になる。
- 個別機能の公開 CLI や実行フローではなく、他の oracle source が前提にする共通概念と小さな基盤実装を確認するための読む先である。

## Read this when
- cmoc 内部で使う基本概念や共通データ構造を確認してから、より具体的な oracle source を読む必要があるとき。
- エージェント呼び出し要求を、バックエンド固有値へ解決する前の論理パラメータとして扱う仕様断片を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` などのルートトークン表記、実パスとの相互変換、worktree root の検出規則に関わる作業をするとき。
- oracle standard などの規範を、背景・要求・判断例を持つ構造へ変換するための実装上のモデルを確認したいとき。
- 構造化された自然言語文書やコードブロックを、見出し階層付き Markdown として生成・整形する基礎処理を確認したいとき。

## Do not read this when
- 個別サブコマンドの CLI 引数、出力 schema、実行手順、プロセス制御、入出力処理を調べたいとき。
- バックエンドが実際に受理するモデル名、Reasoning effort、ファイルアクセス設定への変換や、エージェント起動処理そのものを確認したいとき。
- 特定の oracle doc、oracle test、realization file の内容や配置を確認したいだけで、基礎モデルや共通 helper の意味に触れないとき。
- 既存 Markdown の解析、INDEX.md の探索規則、またはリポジトリ全体のルーティング文書構成を把握したいとき。

## hash
- 271cccf9ccdb7b85a3d2eb5702cd6d9a3b23200af4fdfd9a15dd71ff90314919

# `config`

## Summary
- cmoc のリポジトリ単位の永続設定を定義する領域。人間が編集する設定 dataclass、Codex CLI に渡すモデル名・reasoning effort 名との対応、init で生成・同期される設定項目、apply fork と review oracle の各種ループ上限を確認する入口になる。

## Read this when
- リポジトリごとに永続化される cmoc 設定の構造、既定値、保存時の扱いを確認したいとき。
- Codex CLI 向けのモデル名や reasoning effort 名と、cmoc 内部の分類値との対応を確認・実装するとき。
- apply fork の apply ループ・所見改善ループ、または review oracle の所見列挙・マージ・検証ループの既定回数を確認・変更するとき。
- init が生成・同期する設定ファイルに含める項目や、人間が編集する設定面の範囲を確認するとき。

## Do not read this when
- パスキーワードや root 概念そのものの定義だけを確認したいとき。
- 設定の永続化先を超えて、実際のファイル読み書き処理、JSON 変換処理、init コマンドの制御フローを確認したいとき。
- apply fork や review oracle のループ内部で行われる具体的な処理内容や所見生成ロジックを調べたいとき。
- Codex CLI 呼び出し全体の実行手順、プロンプト、サブプロセス制御を調べたいとき。

## hash
- a370e0d0cb71ebbb02fef3bb47cd296df0aad0edb64dc9c4bc0638d60e3aeeed

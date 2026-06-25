# `acp`

## Summary
- AI エージェント呼び出しに関わる oracle src をまとめる階層。呼び出しパラメータ構築と、呼び出し時に組み込む標準プロンプト部品の正本仕様断片へ進む入口になる。
- サブコマンドや処理ごとに、どの補助文脈・role・goal・制約・モデル設定・reasoning effort・ファイルアクセス範囲・Structured Output 契約を AI に渡すか、またはそれらの前提となる標準文面を確認するための領域。
- CLI 制御フロー、git 操作、ファイル修正、TUI 描画、永続状態更新そのものではなく、それらの処理から呼び出される AI への入力境界と応答境界を読むための階層。

## Read this when
- cmoc の処理が AI エージェントを呼び出す場面で、prompt 構成、補助文脈、読み取り・編集権限、モデル種別、reasoning effort、Structured Output schema の対応を確認したいとき。
- AI に渡す標準プロンプト部品、ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、各種標準文書がどのように呼び出し prompt に組み込まれるかを確認したいとき。
- fork 適用後レビュー、INDEX.md エントリー生成、oracle review、セッション合流時の conflict 解消、TUI 実行パラメータ選定などで、AI 呼び出しへ渡す入力情報と期待する応答契約を調べたいとき。
- AI 呼び出しの実装やテストで、補助情報の組み込み条件、空配列や重複除外の境界、修正用と読み取り専用のアクセス条件を確認したいとき。

## Do not read this when
- CLI 引数解析、サブコマンド登録、branch 作成、merge 実行、git 操作、差分取得、patch 適用、永続状態更新、端末 UI 描画など、AI 呼び出しパラメータ以外の実行フロー本体を調べたいとき。
- 個別ファイルの patch 内容、merge conflict の具体的な統合判断、realization file の修正ロジック、oracle file 本文からの具体的な所見材料など、対象本文そのものを読んで判断する作業をしたいとき。
- StructDoc、AgentCallParameter、file access mode、path 語彙など、プロンプト部品や呼び出しパラメータを支える下位データ構造や共通型そのものを確認したいとき。
- INDEX.md 全体のルーティング方針、エントリー記述品質基準、生成結果の内容評価、または一般的なルーティング文書の書き方を確認したいとき。

## hash
- aa401737bc1147ec5bea7986acc266986eb158c60d5a46144fdab697546b0a28

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
- 開発対象リポジトリ単位で永続化される cmoc の設定仕様を扱う領域。全体設定、Codex CLI 向け設定、apply fork 向け設定、review oracle 向け設定の構造、既定値、JSON 保存時の Enum 値の扱いを確認する入口になる。

## Read this when
- リポジトリごとに保存される cmoc 設定の項目、入れ子構造、既定値を確認したいとき。
- 初期化処理が生成または同期する、人間編集対象の設定内容について正本仕様を確認したいとき。
- AI エージェント呼び出しの並列数、Codex CLI のモデルや reasoning effort、apply fork の処理上限、review oracle のループ回数上限に関わる仕様変更を扱うとき。

## Do not read this when
- 設定ファイルの実行時の読み書き、JSON 変換、CLI コマンド処理の実装だけを確認したいとき。
- パス語彙やルートディレクトリの定義を確認したいとき。
- apply fork や review oracle の処理アルゴリズム、所見生成、マージ、検証の詳細挙動を確認したいとき。

## hash
- a7101c642419b144683a448b15f7b8720bab8601f12897491ec4c7ae00454cd6

# `acp`

## Summary
- AI エージェント呼び出しに渡す前提・制約・入力・出力契約を定義する oracle src 領域。agent call parameter の用途別構築と、prompt に含める標準部品の組み立て方へ進む入口になる。
- 適用後レビュー支援、目次エントリー生成、oracle review、conflict 解消、TUI 実行前判定などで、role・summary・goal、補助文脈、モデル設定、reasoning、ファイルアクセス設定、Structured Output schema との接続を確認するための階層である。

## Read this when
- サブコマンドが AI エージェントを呼び出す際に、どの文脈・制約・モデル設定・出力契約で依頼するかを確認したいとき。
- 変更差分要約、レビュー所見列挙、所見修正依頼、目次エントリー生成、oracle file レビュー、merge conflict marker 解消、TUI 実行前判定に関する prompt 仕様を調べたいとき。
- agent に渡すファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、各種標準文書、完全な prompt への組み立て条件を確認したいとき。
- AI 呼び出しの応答を、判定結果、編集操作、要約、所見、実行パラメータ、空配列などとしてどの契約で扱うか確認したいとき。

## Do not read this when
- CLI 引数解析、ブランチ作成、fork 適用、merge 実行、conflict 検出、git diff 取得、レポート保存、永続状態更新、画面描画など、各サブコマンドの制御フロー本体を調べたいとき。
- oracle file と realization file の基本定義、path keyword、標準文書本文、Markdown 描画、AgentCallParameter や file access mode の共通部品そのものを確認したいとき。
- 個別の対象ファイル本文を読んで、具体的なレビュー所見、修正内容、conflict 解消判断、または目次エントリー内容を作りたいとき。
- AI Agent CLI/TUI プロセスの起動処理、端末 UI、エディタ入力、コメント除去、ログ、保存先など、エージェント呼び出しパラメータや prompt 部品以外の実装を探しているとき。

## hash
- 0a8c9d836b88a00c7369e0387d51d4c44fdba4e68367e3a62c1003aa20614048

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

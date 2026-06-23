# `acp`

## Summary
- ACP は agent call parameter 周辺の正本実装を束ねる領域で、用途別の prompt builder / Structured Output schema と、agent に渡す共通 prompt 断片を扱う。
- 下位には、各サブコマンド・工程ごとの role、goal、補助文脈、model 設定、file access 制約、応答 schema を組み立てる領域と、完全 prompt や標準文書断片を生成する領域がある。
- サブコマンド実行そのものではなく、AI agent 呼び出しに渡す入力契約と出力契約の正本断片へ進むための入口である。

## Read this when
- cmoc の各機能が AI agent をどの前提、制約、標準文書、model 設定、Structured Output schema で呼び出すかを調べたいとき。
- INDEX.md エントリー生成、apply fork の所見処理、review oracle の所見工程、session join の conflict marker 解消、TUI の resolve parameter など、用途別の agent call parameter を確認したいとき。
- agent call に共通して渡される file access rule、routing rule、oracle / realization の基本概念、各種 standard の prompt 断片を確認したいとき。
- AI 呼び出しの実装やテストで、prompt に含める文章と応答 JSON schema の意味的な対応先を切り分けたいとき。

## Do not read this when
- CLI 引数解析、サブコマンド制御フロー、git 操作、fork 作成、merge、差分取得、状態保存、画面表示など、AI 呼び出しパラメータ以外の処理を調べたいとき。
- oracle file、realization file、path keyword、StructDoc などの共通データモデルやユーティリティの基礎定義だけを確認したいとき。
- 個別の oracle file や realization file の本文を読んで、仕様問題、実装修正内容、conflict 解消判断、変更差分そのものを判断したいとき。
- Structured Output schema の項目定義だけ、または特定工程の prompt builder だけを確認したい場合で、該当する下位対象がすでに分かっているとき。

## hash
- 9ea11839b14018bacdc43933c7ce79028a305451e9d8ce24caafa06a938db283

# `basic`

## Summary
- cmoc の実装系正本仕様断片のうち、基礎的な型・文書生成・パス解決を扱う入口。AI コーディングエージェント呼び出しの論理パラメータ、root token と実パスの対応、規範モデル、構造化自然言語文書の Markdown 描画といった、複数領域から参照される低層概念をまとめている。
- バックエンド固有の実行オプションや個別サブコマンドの仕様ではなく、cmoc 内部で共有される抽象モデルや補助データ構造を確認するための階層。

## Read this when
- cmoc 内で共有される基本データ構造、列挙値、入力検証、または文書生成 helper の正本仕様断片を探すとき。
- AI コーディングエージェント呼び出しに渡す論理パラメータ、モデル選択、Reasoning effort、ファイルアクセスモード、Structured Output schema 指定の表現を確認したいとき。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` の意味、root token 付きパス表記と絶対パスの相互変換、git worktree に基づく root 解決を確認したいとき。
- 規範を背景・要求・判断例を持つ構造へ変換する処理、要求ラベル、または規範入力の検証条件を確認したいとき。
- 階層化された自然言語文書を Markdown として描画する処理、見出し深さ、コードブロック、三重引用文字列由来本文の正規化を確認したいとき。

## Do not read this when
- 個別 CLI サブコマンドの引数、出力形式、実行フロー、状態管理、ログ処理を確認したいだけのとき。
- AI コーディングエージェント呼び出し後の結果処理や、バックエンド固有のモデル名・実行時オプションへの具体的な変換規則を確認したいとき。
- ファイル内容の読み書き、永続状態、設定、サンドボックス実現方法などを調べたいだけで、root token や基本モデルの意味に触れないとき。
- 個別の規範本文そのもの、oracle file と realization file の概念定義、INDEX.md のルーティング方針を確認したいとき。
- Markdown 入力解析、既存 Markdown 文書の探索、またはリポジトリ全体の文書配置を把握したいとき。

## hash
- eef2ed94f0e439ff252202833e7f21f33076dd624dbfbd9f692925f564cc055d

# `config`

## Summary
- 開発対象リポジトリ単位で変わる cmoc の設定仕様を扱う oracle src 群への入口。
- 永続化される設定 JSON の構造、既定値、AI エージェント呼び出し・適用分岐・review oracle の上限値、Codex CLI 向けモデル名と reasoning effort 名の対応を確認するための領域。
- Enum 系の値を JSON 保存時に value 化する前提や、設定ファイルが初期化処理で生成・同期され人間編集される境界を把握するためのルーティング先。

## Read this when
- 開発対象リポジトリごとに保持される cmoc 設定の責務、永続化される内容、既定値を確認したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名が、cmoc 内部のモデル分類・推論努力度からどう対応づくかを確認したいとき。
- AI エージェント呼び出しの最大並列数、適用分岐や review oracle のループ上限など、設定由来の制御値を仕様根拠として確認したいとき。
- 設定 JSON へ保存する際に Enum 系インスタンスをどのような表現へ変換する前提かを確認したいとき。
- 設定ファイルが初期化処理で生成・同期され、人間が編集するものとして扱われる境界を確認したいとき。

## Do not read this when
- パスキーワードやルートディレクトリ概念の定義だけを確認したいとき。
- 設定ファイルを実際に読み書きする実装、JSON 変換処理、初期化サブコマンドの具体的な処理手順を探しているとき。
- 適用分岐や review oracle の具体的なアルゴリズム、所見形式、サブコマンド入出力仕様を確認したいとき。
- リポジトリに依存しない固定仕様、テスト方針、oracle file と realization file の一般的な関係を確認したいとき。

## hash
- e333b5511ee2e06b89ac77f9d8ea837a274f30698f6317c5dda1e45925b1239f

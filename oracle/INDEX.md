# `doc`

## Summary
- cmoc の正本仕様断片のうち、自然言語ドキュメントを集めた領域。アプリケーション挙動、branch/worktree モデル、開発ルール、不採用設計案など、実装前に読むべき人間意図への入口になる。
- 利用者向け仕様、実行基盤、開発時の横断ルール、過去に退けた設計判断を切り分け、どの正本仕様断片へ進むべきか判断するためのルーティング対象。

## Read this when
- cmoc の CLI 挙動、run 隔離、セッション状態、ログ、エラー処理、インデクシング、Codex CLI 呼び出しなど、アプリケーション全体の自然言語仕様を探すとき。
- session fork/join、run ごとの managed branch、linked worktree、repository default branch、session/run 系 branch の意味や命名規則を確認したいとき。
- Python 実装、CLI 責務配置、開発環境、realization test、Fake Codex CLI 利用など、開発時に守る横断ルールを確認したいとき。
- 採用済み仕様ではなく、apply orchestration、file access rule 違反処理、permission profile 変換、AI-generated memory や作業計画レビュー方式など、過去に不採用となった設計案の背景を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な定義、責務境界、編集権限、追跡対象判定、品質基準だけを確認したいとき。
- パスキーワードやルート種別の定義だけを確認したいとき。
- 実装内部の関数、クラス、テスト fixture、補助ファイル配置、Structured Output schema 構築ロジックなど、realization code の具体構造だけを調べたいとき。
- 採用済み仕様や設計判断ではなく、外部ツールや git ignore などの一般仕様だけを調べたいとき。

## hash
- f6db99a82e43238d8d8efff382b5ed6af8eadfd951d5857a2fa4c30662f18619

# `script`

## Summary
- cmoc 開発者向けの補助スクリプトを置く領域で、現時点では ollama の Linux amd64 アーカイブを取得し、リポジトリ内のローカル領域へ展開する開発環境準備手順を扱う。
- 利用者向け CLI 仕様やプロダクト挙動ではなく、開発者が手動で依存ツールを配置するための oracle file への入口として位置づけられる。

## Read this when
- cmoc 開発用に ollama をローカルインストールする手順や配置先を確認したいとき。
- ollama 実行ファイルの配置場所、必要な apt パッケージ、ダウンロード元、展開方法を確認したいとき。
- 開発者向けの手動セットアップ手順が、cmoc の利用者向け CLI 仕様ではないことを確認したいとき。

## Do not read this when
- cmoc の利用者向け CLI コマンド、引数、出力仕様を確認したいとき。
- ollama 以外の開発依存関係、または一般的な開発環境全体のセットアップを確認したいとき。
- 実装コードやテストコードから cmoc のプロダクト挙動を確認したいとき。

## hash
- d00105394382112a22c66f0512bafb345d086909235355381234ea8857dedb85

# `src`

## Summary
- AI エージェント呼び出しと共通プロンプト生成に関する正本実装断片への入口。呼び出しパラメータ、prompt、権限、モデル方針、preflight、Structured Output schema、共通規範プロンプトの構成を扱う。
- 設定、パス表記、規範文書モデル、構造化 Markdown レンダリングなど、複数領域から使われる正本実装断片も含む。
- レビュー、差分要約、所見対応、索引エントリー生成、競合解消、TUI 起動など、機能別の AI 呼び出し仕様と、それを支える共通部品へ進むためのまとまり。

## Read this when
- cmoc の機能が AI エージェントを呼び出す際の基本構造、個別機能ごとの呼び出し方針、出力契約を確認したいとき。
- agent call に渡す完全なプロンプトが、役割、概要、ゴール、補助プロンプト、ファイルアクセス制限、ルーティング規則、各種標準からどう構築されるかを確認・変更したいとき。
- oracle file、realization file、レビュー、INDEX.md エントリー、ファイル読み書きなど、AI に注入する共通規範プロンプトを確認・変更したいとき。
- cmoc の設定既定値、Codex CLI 向けモデル・推論設定、apply fork や review oracle のループ上限を確認したいとき。
- ルート概念、プレースホルダ付きパスと絶対パスの変換規則、相対パス禁止の扱いを確認したいとき。
- 規範文書を構造化して扱うモデルや、階層化された文章を Markdown としてレンダリングする helper の挙動を確認・変更したいとき。

## Do not read this when
- AI エージェント呼び出しではなく、CLI サブコマンドの実行制御、branch 操作、diff 取得、保存処理、表示整形、対象ファイル探索を調べたいとき。
- バックエンド固有のモデル名・reasoning effort 名への変換、プロセス起動、結果処理、エラー処理を確認したいとき。
- 特定の CLI サブコマンド、状態ファイル、利用者向け入出力形式など、個別プロダクト仕様だけを調べたいとき。
- 設定値の正本ではなく、設定ファイルを実際に読み書きする realization implementation だけを探しているとき。
- 個別の標準文書本文や品質基準そのものだけを確認したいとき。
- 実装ファイルやテストファイルの現在構造を把握して直接修正したいだけで、AI 呼び出し仕様、プロンプト生成、共通規範の注入に関係しないとき。

## hash
- 647329b550964cb9a2822e15cb2db729cbcc4df65b1a42f3be62e2abb55250c4

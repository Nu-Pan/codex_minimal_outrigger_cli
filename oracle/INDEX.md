# `doc`

## Summary
- cmoc の自然言語による正本仕様断片を集めた領域。アプリケーション全体の外部挙動、branch/worktree モデル、不採用設計案、開発規則など、実装・テストへ進む前に人間意図と判断境界を確認する入口になる。
- 個別ファイルは、利用者向け CLI 挙動や agent call 周辺の共通仕様、git branch と worktree による実行隔離、過去に退けた設計案、Python 実装・pytest・CLI 構成の開発ルールへ分かれている。

## Read this when
- cmoc の実装やテストを変更する前に、自然言語で書かれた正本仕様断片から根拠を探したいとき。
- CLI 挙動、サブコマンド、Codex CLI 呼び出し、ログ、エラー処理、セッション状態、run 隔離、索引生成など、アプリケーション横断の外部仕様を確認したいとき。
- session fork/join、apply/review、managed branch、linked worktree など、cmoc が git branch・commit・worktree をどう扱うかを確認したいとき。
- 現行設計の変更を検討する際に、過去に不採用となった代替案と不採用理由を確認したいとき。
- Python コーディング規則、CLI 構成、開発環境、pytest 方針など、realization code と realization test の書き方に関する開発規則を確認したいとき。

## Do not read this when
- oracle file と realization file の一般定義、品質基準、INDEX.md エントリー規則など、リポジトリ全体の仕様管理原則だけを確認したいとき。
- path keyword や root 種別そのものの定義だけを確認したいとき。
- 実装ファイルやテストファイルの具体的な関数、クラス、内部 helper、既存コード構造だけを調べたいとき。
- 採用済み仕様ではなく外部ツール自体の一般的な使い方だけを調べたいとき。
- 読むべき個別の正本仕様断片が既に分かっており、その本文へ直接進めるとき。

## hash
- 902786cddbf8c9884bed360caf27f20aa99b07ddcdfeb9985ca0fabb14f81c61

# `src`

## Summary
- cmoc の正本実装断片全体への入口。AI 呼び出し仕様、共通基礎モデル、プロンプト構築仕様など、実装として書かれた oracle の主要領域を切り分ける。
- agent call の入力方針、Structured Output schema、リポジトリ設定、パスモデル、規範文書モデル、共通規範を含むプロンプト生成について、どの下位領域へ進むべきか判断するための対象。

## Read this when
- cmoc の正本実装断片のうち、AI 呼び出し、プロンプト生成、共通モデルのどの領域へ進むべきかを切り分けたいとき。
- agent call に渡す role、prompt、権限、モデル方針、preflight 有無、Structured Output schema の正本値を探し始めるとき。
- リポジトリ別設定、ルートパスプレースホルダ、規範文書モデル、構造化 Markdown レンダリングなど、複数領域から参照される共通概念を確認したいとき。
- 完全プロンプトの組み立て順、標準文書や読み書き規則の注入、静的・動的プロンプトとプレースホルダ定義の配置を確認したいとき。

## Do not read this when
- CLI サブコマンドの実行制御、git 操作、状態ファイル、表示整形、対象ファイル探索など、プロダクト実行フローの実装を直接調べたいとき。
- oracle standard、realization standard、index entry standard などの標準本文そのものだけを確認したいとき。
- バックエンド固有のモデル名変換、プロセス起動、結果処理、エラー処理など、AI 呼び出し実行基盤の詳細を追いたいとき。
- 特定の下位領域を読むことがすでに決まっており、その領域の本文へ直接進めるとき。

## hash
- ec9b03d1c76fbd14b4ea1f57eb82a57439342f96962674091797a7a4d5d7d135

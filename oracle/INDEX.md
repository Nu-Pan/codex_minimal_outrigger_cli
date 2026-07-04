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
- プログラミング言語で書かれた正本仕様断片の下位領域を切り分ける入口。AI 呼び出し仕様、プロンプト構築、設定、パス、構造化文書、Markdown レンダリング helper などの正本定義へ進むための分岐点。
- agent call のパラメータ、Structured Output schema、共通プロンプト部品、リポジトリ設定、モデル・推論努力対応、並列数やリカバリ回数、パスプレースホルダ、規範文書モデルの正本値を確認する領域。
- CLI 実行制御や realization 側実装ではなく、AI に渡す情報、共通規範、設定・パス・文書構造の正本仕様断片を探すために読む。

## Read this when
- 実装形式の正本仕様断片から、どの下位領域を読むべきか切り分けたいとき。
- AI エージェント呼び出しの基本パラメータ、個別機能の prompt、応答 JSON、Structured Output schema の正本定義を探すとき。
- agent call 用プロンプトの構成順、共通規範の注入、ファイルアクセス制限、ルーティング規則、プレースホルダ定義の扱いを確認したいとき。
- リポジトリ別設定、モデル・推論努力対応、並列数やリカバリ回数、パスプレースホルダ、規範文書モデル、構造化 Markdown レンダリングの正本定義を探すとき。

## Do not read this when
- 自然言語で書かれた正本仕様断片や、テスト形式の正本仕様断片を確認したいとき。
- CLI サブコマンドの実行制御、branch 操作、diff 取得、保存処理、表示整形、対象ファイル探索など realization 側の実装詳細を調べたいとき。
- oracle standard、realization standard、apply review standard、index entry standard などの規範本文だけを確認したいとき。
- バックエンド固有のプロセス起動、モデル名変換、結果処理、エラー処理、生成済み設定ファイルの読み書きなど、具体的な実装経路を追いたいとき。

## hash
- 0287f55ed6bad97ca60371b5ae88f57384096c7c87257720b92b7b5f067bdb02

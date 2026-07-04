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
- cmoc の oracle src 群のうち、AI エージェント呼び出し仕様と横断的な基礎モデルを扱う領域への入口。agent call parameter、prompt、Structured Output schema、パス表記、設定、規範文書モデル、Markdown helper などの正本仕様断片を下位領域へ振り分ける。
- プロンプト構築や共通規範注入、サブコマンド向け agent 呼び出し契約、複数領域から参照される補助モデルのどれを確認すべきか判断するためのルーティング対象。

## Read this when
- cmoc の oracle src にある正本仕様断片のうち、AI エージェント呼び出し、prompt、Structured Output schema、またはそれらを支える横断モデルを探すとき。
- agent call 用の共通 parameter、機能別 builder、完全プロンプトの構築順序、共通規範プロンプト、ファイルアクセス制限やルーティング規則の注入位置を切り分けたいとき。
- cmoc の設定値、ルートパスプレースホルダ、パス解決、規範文書の構造化、仕様文生成用 Markdown helper など、複数領域から参照される基礎概念の oracle src を確認したいとき。

## Do not read this when
- CLI 実行制御、branch 操作、diff 取得、レポート保存、対象ファイル探索、表示整形など、AI エージェント呼び出し仕様や横断モデルではない実装を調べたいとき。
- 特定サブコマンドの利用者向け入出力、実行手順、状態ファイル仕様だけを確認したいとき。
- realization code 側の prompt builder 実装、外部コマンド起動、バックエンド固有モデル名への変換、またはテスト構成を確認したいとき。

## hash
- ff377c45bb81945513029eb17fc138911907e756d1fd4e961bc79a5ad24dcd20

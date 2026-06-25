# `builder`

## Summary
- AI エージェント呼び出し用のパラメータ構築を扱う領域。`apply`、`indexing`、`review`、`session`、`tui` などの各処理について、prompt、role、goal、補助文脈、ファイルアクセス条件、モデル設定、推論量、Structured Output schema の対応を定義する。
- cmoc の各サブコマンドや TUI 実行前処理で、AI に何を読ませ、何を出力させ、どの権限で作業させるかを確認する入口になる。

## Read this when
- AI エージェントへ渡す呼び出しパラメータの組み立てを、処理ごとに確認または変更したいとき。
- prompt に含める role、summary、goal、補助文脈、対象本文、標準指示、既知所見、差分などの渡し方を追いたいとき。
- Structured Output schema が、レビュー所見、理由、採否、差分要約、INDEX.md エントリー、TUI パラメータ判定などでどの責務を持つか確認したいとき。
- AI 呼び出しにおける model class、reasoning effort、file access mode、realization 書き込み可否、git 操作禁止条件などの組み合わせを調べたいとき。
- `cmoc apply fork`、`cmoc indexing`、`cmoc review oracle`、`cmoc session join`、TUI 実行前パラメータ解決のいずれかで、AI 呼び出し前の入力契約や出力契約を実装・テストしたいとき。

## Do not read this when
- 各サブコマンド全体の CLI 引数解析、実行順序、状態更新、git コマンド実行、保存処理など、AI 呼び出しパラメータ構築より外側の制御フローを調べたいとき。
- oracle file、realization file、review standard、apply review standard、INDEX.md 運用規則などの標準本文そのものを確認したいとき。
- Markdown レンダリング、構造化文書表現、パス解決、AgentCallParameter 型、モデル種別やファイルアクセスモードの共通定義など、呼び出し構築を支える共通基盤を調べたいとき。
- 個別の変更対象ファイル、実際の差分検出、分類アルゴリズム、conflict marker 検出、TUI 表示や入力取得など、AI に渡すパラメータ以外の具体処理を確認したいとき。

## hash
- d2a1ff13e7c9eb45eaef45de557128432770d36ed0e1a612ae6904d022892c93

# `prompt_parts`

## Summary
- AI agent に渡すプロンプトを構成する標準文書・規則文書の部品群を扱う実装ディレクトリ。ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念、各種標準、レビュー基準、INDEX.md エントリー品質基準などを構造化文書として生成する責務を持つ。
- 最終プロンプトを組み立てる処理と、個別の標準プロンプト本文を生成する処理の入口になっており、agent 呼び出し時にどの規範・制約・追加標準を含めるかを追うための起点となる。

## Read this when
- agent に渡す標準プロンプト群の構成、依存関係、追加条件、または Codex CLI 向けの用語・ルートトークン置換を確認・変更したいとき。
- ファイルアクセス規則、INDEX.md を使ったルーティング規則、oracle file と realization file の責務境界など、agent に提示される共通ルール文書の生成内容を確認・変更したいとき。
- oracle file、realization file、レビュー所見、INDEX.md エントリーに適用される標準・判断基準を、プロンプト部品としてどのように構築しているか確認したいとき。
- 新しい標準プロンプトを追加する、既存標準の文面を調整する、または最終プロンプトへの組み込み条件を変更するとき。

## Do not read this when
- 個別の CLI サブコマンド、path model、永続状態、出力 schema などのプロダクト仕様や実装詳細を探しているときは、それぞれの機能領域を直接読む。
- 構造化文書の型定義、レンダリング処理、Standard や Requirement の共通変換仕様そのものを確認したいときは、基盤となる構造化文書実装を直接読む。
- 実際のファイルアクセス制御やサンドボックス enforcement の実装を探しているときは、この対象ではなく実行制御側を読む。
- 特定の oracle file や realization file の内容そのものをレビュー・実装したいだけで、agent に渡す規範プロンプトの生成処理を確認する必要がないとき。

## hash
- 6a9266646719f0c0042086f544c503dccb4f86ba8a6fcfcfdfbb6766ff52e394

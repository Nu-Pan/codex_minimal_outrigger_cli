# `builder`

## Summary
- AI エージェント呼び出しに渡す AgentCallParameter と Structured Output schema を、用途別の builder 群として組み立てる領域。apply、indexing、review、session、tui などの上位処理から呼ばれ、role・summary・goal・補助プロンプト・モデル種別・reasoning effort・ファイルアクセス条件・schema 指定を用途ごとにまとめる入口になる。
- サブコマンド本体の実行制御ではなく、各処理が AI に何を依頼し、どの入力文脈と出力契約で呼び出すかを確認するための実装まとまり。

## Read this when
- apply 系処理、INDEX.md エントリー生成、oracle レビュー、session join の conflict marker 解消、TUI 実行パラメータ選定で、AI 呼び出しに渡すプロンプト内容や実行条件を確認・変更したいとき。
- 各用途の Structured Output schema が、どの意味情報・判定結果・レビュー所見・整理操作を出力契約として求めているかを確認したいとき。
- 対象ファイル、関連所見、git diff、review 結果、conflict 対象一覧、ユーザープロンプト、標準文書などの補助文脈が、AI 向け prompt にどう埋め込まれるかを追いたいとき。
- モデルクラス、reasoning effort、sandbox/approval、ファイルアクセスモード、構造化出力の指定など、複数の AI 呼び出し builder に共通する設定の使い分けを確認したいとき。

## Do not read this when
- 各サブコマンドの CLI 引数解析、サブコマンド登録、実行順序、結果保存、表示処理など、builder を呼び出す側の制御フローだけを調べたいとき。
- AI 呼び出し基盤そのもの、共通 prompt 部品、Markdown レンダリング、Structured Output 実行器、低レベルの path model や git command wrapper の詳細だけを確認したいとき。
- oracle file や realization file の正本仕様本文、レビュー基準本文、INDEX.md エントリーの個別文面そのものを読みたいとき。
- 実際のファイル編集、差分分類、merge conflict 解消、git merge、worktree 操作など、AI 呼び出し依頼後に行われる下位アルゴリズムや外部操作の詳細だけを調べたいとき。

## hash
- 528ab39c274e16d459a55423d705c3dd80e923a41770457cfad809bc34ea419f

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

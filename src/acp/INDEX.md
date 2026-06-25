# `builder`

## Summary
- AI エージェント呼び出し用のパラメータ構築実装と Structured Output schema を、機能領域ごとにまとめる入口。適用処理、目次エントリー生成、oracle file レビュー、session join の conflict 解消、TUI 実行前のパラメータ選定などで、role、goal、補助プロンプト、ファイルアクセス方針、モデル種別、reasoning effort、schema 参照をどう組み合わせるかを扱う。
- 各サブコマンドの本体制御ではなく、別の AI エージェントへ渡す依頼文と実行条件を組み立てる層を追うためのまとまり。下位要素は、レビュー所見列挙・採否・整理、実装修正依頼、差分要約、目次生成、権限選択、conflict marker 解消など、AI 呼び出しの目的別に分かれている。

## Read this when
- サブコマンド内で AI エージェントを呼び出す際の AgentCallParameter 構築箇所を探したいとき。
- AI に渡す role、summary、goal、補助文脈、対象パスや入力データの埋め込み方、読み取り専用または書き込み許可のファイルアクセス方針を確認または変更したいとき。
- AI 呼び出しごとのモデル種別、reasoning effort、Structured Output schema の対応関係を確認したいとき。
- 適用処理のレビュー所見列挙、所見対応作業、差分からの変更要約に使うプロンプトや出力契約の所在を選びたいとき。
- oracle file レビューで、新規所見、所見の肯定理由・反証理由、採否判定、所見リスト整理を行う各 AI 呼び出しの設定を追いたいとき。
- 目次エントリー生成や TUI 実行パラメータ選定など、標準文書やファイルアクセス規則を含めて AI に判断させる呼び出し仕様を確認したいとき。
- session join で検出された merge conflict marker の解消を別エージェントへ依頼するプロンプト条件を確認したいとき。

## Do not read this when
- サブコマンドの CLI 引数解析、実行順序、git 操作、ファイル走査、保存、表示、レポート生成など、AI 呼び出しを起動する側の制御フローを調べたいとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode などの共通データ構造や enum の定義そのものを確認したいとき。
- 共通プロンプトのレンダリング、構造化ドキュメント表現、パス解決、ファイルアクセス規則生成など、複数 builder から利用される基盤処理の詳細を調べたいとき。
- oracle file、realization file、review standard、apply review standard、INDEX.md エントリー標準など、AI 呼び出しに同梱される標準本文そのものを読みたいとき。
- 個別機能の実装挙動やテスト対象を調べたいだけで、AI に渡すプロンプトや Structured Output schema の契約を確認する必要がないとき。

## hash
- 167fe3cdad1b2b6f00fe1c9de975fc5bace8ef7d9365b74fb627146c4f0ed212

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

# `builder`

## Summary
- AI エージェント呼び出しに渡すパラメータ構築と Structured Output schema を、用途別にまとめる領域。レビュー、適用、目次生成、セッション競合解消、TUI の事前パラメータ判定などで、role、summary、goal、補助プロンプト、参照標準、ファイルアクセス権限、モデル設定、reasoning effort、出力契約を組み合わせる実装への入口になる。
- 各用途では、対象パス、対象本文、差分、所見、競合対象、元プロンプトなどの文脈を AI 呼び出し用プロンプトに埋め込み、呼び出し段階ごとに必要な schema と制約を選ぶ。実行フロー本体ではなく、AI に何をどう依頼し、どの構造で結果を受け取るかを追うためのまとまり。

## Read this when
- AI エージェントへ渡す AgentCallParameter、プロンプト断片、参照標準、ファイルアクセスモード、モデル種別、reasoning effort、Structured Output schema の対応関係を確認または変更したいとき。
- レビュー所見の列挙・整理・採否判断、適用時の修正依頼・変更要約、目次エントリー生成、merge conflict marker 解消、TUI の実行前パラメータ判定など、用途ごとの AI 呼び出し条件を比較して追いたいとき。
- 対象本文、git diff、所見リスト、個別所見、conflict 対象、元プロンプトなどの補助文脈が、各 AI 呼び出しのプロンプトへどう埋め込まれるか確認したいとき。
- AI 呼び出し結果として期待する構造化データの意味単位や、出力 schema が各処理段階の情報粒度をどう固定しているか確認したいとき。

## Do not read this when
- 各サブコマンドの CLI 引数解析、サブコマンド登録、実行制御、git 操作、ファイル走査、保存・集約・表示などの通常フロー本体を調べたいとき。
- 完全プロンプトの共通組み立て、Markdown レンダリング、AgentCallParameter や FileAccessMode、モデル種別、パスキーワードなどの共通型・共通ユーティリティを詳しく調べたいとき。
- oracle file、realization file、各種 standard の本文そのもの、または個別の実装対象ファイルやテスト本文を確認したいとき。
- TUI の画面表示やイベント処理、session join の merge 実行、apply fork の branch 作成や差分取得など、AI 呼び出し条件より外側の処理を調べたいとき。

## hash
- 1a2384b8e649d7c7668ccb5deb5a91caf75bdadaa9f87f60729caea6cc14cf01

# `prompt_parts`

## Summary
- AI agent に渡す標準プロンプト部品を構築する実装群をまとめた領域。ファイルアクセス規則、INDEX.md による読み進め方、oracle file と realization file の基本概念、oracle/realization の各種標準、レビュー所見の判断基準、INDEX.md エントリー品質基準を構造化文書として生成する入口になっている。
- 個別の規範本文を構築する部品と、それらを依存関係に従って完全な agent prompt へ組み立てる部品を扱うため、cmoc が AI に提示する作業前提・編集境界・レビュー基準・ルーティング基準を確認するための上位入口となる。

## Read this when
- agent call に含める標準プロンプト群の構成、追加条件、依存関係、組み立て順を確認したいとき。
- ファイル読み書き制約、INDEX.md の使い方、oracle file と realization file の責務境界を、AI 向けプロンプトとしてどう提示しているか確認・変更したいとき。
- oracle file、realization file、oracle review、apply review、INDEX.md エントリーに関する標準文書の生成内容や、どの規範文章がどの作業に対応するかを探したいとき。
- レビュー所見として扱うべき問題の境界、仕様断片の隙間の扱い、realization file 側の品質・肥大化抑制・テスト方針など、AI に与える共通判断基準の実装を追いたいとき。
- 新しい標準プロンプト部品を追加する、既存の標準文書を変更する、または完全な prompt への取り込み位置や有効化フラグを調整したいとき。

## Do not read this when
- 特定サブコマンドの CLI 挙動、入出力 schema、永続状態、path model など、個別機能の仕様や実装を直接調べたいとき。
- 生成されたプロンプトを使って agent call を実行する処理、外部プロセス起動、結果の保存や後続処理を確認したいとき。
- oracle file そのもののプロダクト仕様断片や、realization implementation/test の個別実装を確認したいとき。
- 構造化文書型、Standard/Requirement 変換、列挙値や型定義など、プロンプト本文ではなく共通データ構造や型だけを調べたいとき。
- INDEX.md エントリーの具体文面を作るために対象本文がすでに特定できているとき。この領域は標準規範や prompt parts の実装を読む入口であり、個別対象の本文の代替ではない。

## hash
- 8e2921652c743a7e7a6735aa65d028f64a9480635f986514a4f18ee8f05590c7

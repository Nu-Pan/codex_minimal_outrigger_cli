# `builder`

## Summary
- cmoc の各機能が AI エージェントへ作業を依頼する際の呼び出しパラメータを組み立てる領域。complete prompt に渡す role、summary、goal、補助入力、標準文書の参照指定、ファイルアクセス権限、モデル種別、推論量、必要に応じた Structured Output 契約を接続する。
- フォーク適用、目次情報生成、oracle review、session の conflict marker 解消、TUI の実行パラメータ解決など、機能別の builder 群への入口になる。実際の処理本体ではなく、下流エージェントに何をどの条件で依頼するかを定義する層である。

## Read this when
- AI エージェント呼び出しに渡すプロンプト本文、補助入力、標準文書の参照有無、ファイルアクセスモード、モデル・推論設定を機能別に確認または変更したいとき。
- フォーク適用の変更要約、ファイル起点の所見列挙、所見に基づく修正依頼のどの呼び出し設定を読むべきか判断したいとき。
- INDEX.md 用エントリー生成、oracle review の所見列挙・理由収集・採否判定・整理、session join の conflict marker 解消、TUI の実行パラメータ解決に関する AI 依頼条件を確認したいとき。
- 各 AI 呼び出しで、入力データがどの補助プロンプトとして埋め込まれ、どの Structured Output 契約または契約なしの実行に接続されるかを追いたいとき。

## Do not read this when
- 各サブコマンドの実行制御、状態管理、git 操作、ファイル走査、保存、merge 実行など、AI 呼び出し前後の処理本体を調べたいとき。
- complete prompt の共通構築規則、構造化 Markdown レンダリング、パス解決、AgentCallParameter や FileAccessMode などの基礎型そのものを調べたいとき。
- oracle review や apply review の所見を実際に評価・統合・適用する後段処理、または生成結果の表示・通知・永続化を探しているとき。
- 個別の Structured Output の項目構造だけを確認したい場合は、該当する下位の schema 定義へ直接進めばよい。

## hash
- 9375f9e81e1abc4d978554e7e00706f5680aa2ae006a684b6e020c8fa4b3806f

# `prompt_parts`

## Summary
- AI agent に渡す prompt part 群を構築する実装をまとめた領域。ファイルアクセス規則、ルーティング規則、oracle / realization の基本概念と品質規範、レビュー所見の判断基準、INDEX.md エントリー作成規範、agent call 用の完全 prompt 合成を扱う。
- 各 prompt part は構造化文書として標準文書や規則本文を返し、complete prompt 側では role、summary、goal、アクセス規則、ルーティング規則、追加 prompt、標準 prompt 間の依存関係、呼び出し先向けの内部呼称・root token 除去をまとめて扱う。
- cmoc のプロダクト挙動そのものではなく、AI に作業方針・レビュー基準・正本仕様と実装の責務境界を伝えるための prompt 文書生成箇所への入口になる。

## Read this when
- agent call に渡す prompt の構成順序、標準 prompt の依存関係、または各標準文書がどのように complete prompt に注入されるかを確認・変更したいとき。
- ファイルアクセス制限、INDEX.md によるルーティング、oracle file と realization file の基本定義、oracle / realization の品質規範を AI 向け prompt としてどう表現しているか調べたいとき。
- oracle file レビュー、oracle file を realization file に適用するレビュー、または INDEX.md エントリー作成で、どの基準を所見・規範・案内として扱うか確認したいとき。
- 標準 prompt part の本文、Standard 群の並び、構造化文書への変換呼び出し、または呼び出し先へ渡す前の root token や内部呼称の置換処理を変更したいとき。

## Do not read this when
- CLI コマンド、永続状態、外部プロセス実行、入出力 schema など、prompt 文書生成ではないプロダクト機能の実装詳細を調べたいとき。
- StructDoc、StructCodeBlock、Standard、Requirement などの構造化文書データ構造や変換基盤そのものを確認したいとき。
- path token、作業ルート、run root、各 root の定義や解決規則そのものを調べたいとき。
- 特定の oracle file、realization file、テスト、または実際の差分内容をレビューしたいだけで、AI に渡す標準 prompt の本文や判断基準を変更しないとき。

## hash
- ccba95c007c9a5146ae93517fe4e58e99db1ac3ec9b654caa88907d2f3beb6fa

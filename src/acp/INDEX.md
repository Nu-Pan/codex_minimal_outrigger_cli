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
- AI agent に渡す構造化プロンプト部品を構築する実装群。ファイルアクセス規則、INDEX.md によるルーティング規則、oracle file と realization file の基本説明、oracle/realization/index entry/review/apply review の各種標準文書を扱う。
- 個別の標準文書を StructDoc 化する部品と、それらを agent call 用の完全なプロンプトへ組み立てる処理を含む。標準部品間の依存関係に応じた自動注入や、プロンプト中の root token とツール固有用語の呼び出し先向け置換もこの領域で扱う。
- プロンプト本文として agent に何を指示するか、どの標準をどの条件で含めるか、標準文書の責務境界をどう保つかを確認するための入口になる。

## Read this when
- agent call に渡す最終プロンプトの構成順、含める標準部品、標準部品間の依存関係、または追加プロンプトとの結合方法を確認・変更したいとき。
- AI 向けに提示するファイル読み書き制限、INDEX.md の読み進め方、oracle file と realization file の基本概念を、プロンプト本文としてどう生成しているか確認したいとき。
- oracle file の記述規範、realization file の品質規範、INDEX.md エントリー作成規範、oracle file レビュー規範、oracle 内容を realization へ適用するレビュー規範の本文を確認・変更したいとき。
- 標準プロンプトを StructDoc として組み立てる責務境界や、長い標準文書を単一の prompt part として保持している理由を確認したいとき。
- プロンプト中の root token を実パスへ置換する処理や、呼び出し先に渡す文面からツール固有の呼称を作業対象向け表現へ置換する処理を追いたいとき。

## Do not read this when
- StructDoc、StructCodeBlock、Standard、Requirement など、構造化文書や標準項目そのもののデータ構造・レンダリング基盤を調べたいとき。
- root token の定義、作業ルートや実パスの解決規則そのもの、またはパスモデルの基本仕様を確認したいとき。
- agent call の実行、外部プロセス起動、CLI サブコマンドの制御フロー、永続状態、入出力 schema など、プロンプト部品生成以外の処理を調べたいとき。
- 特定の oracle file や realization file の本文内容、または実際の差分レビュー結果を確認したいだけで、レビュー基準や標準プロンプト本文を変更する必要がないとき。
- 実際のファイルアクセス制御を OS 権限、サンドボックス、実行環境で enforcement する仕組みを探しているとき。

## hash
- 94f20b380c1fa30ace1d0202ad855fb4456c93f9977a6544b50cd8752ffa1b57

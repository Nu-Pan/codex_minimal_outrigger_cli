# `apply`

## Summary
- `cmoc apply fork` に関する変更要約、ファイル単位レビュー・修正の AgentCallParameter と、それらに対応する正本スキーマを扱う。変更要約の出力契約、レビュー・修正用 prompt、モデル・アクセス設定を確認する入口。

## Read this when
- `cmoc apply fork` の変更要約処理を実装・検証するとき。
- ファイル単位レビュー・修正の prompt、出力スキーマ、AgentCall 設定を調査するとき。
- 変更要約やファイルレビュー・修正に対応する oracle src とスキーマの関係を確認するとき。

## Do not read this when
- 差分取得、fork の作成・適用など、要約・レビューの前後にある実行フローを調査するとき。
- レビュー対象ファイルの具体的な realization 実装やテストを確認するとき。
- 共通 prompt builder、パス解決、構造化文書処理の実装詳細だけを調査するとき。

## hash
- adc698de6dbcc5483d43c421a5a0449363c2f17026a4fd3abbae9c385e9f2f6a

# `basic.py`

## Summary
- エージェント呼び出しに渡すモデル種別、推論強度、ファイルアクセス権、プロンプト、Structured Output schema、作業ディレクトリなどのパラメータ型と既定値を定義する基礎モジュール。ACP 呼び出し条件やファイルアクセスモードの意味を確認する際の入口。

## Read this when
- エージェント呼び出しパラメータの構造、モデルクラス、推論強度、ファイルアクセスモード、既定の作業ディレクトリを変更・確認するとき。
- ACP builder が受け取るパラメータや Structured Output schema の指定方法を調査するとき。

## Do not read this when
- 具体的なバックエンドモデル名への解決や実際のエージェント呼び出し処理を調べるとき。
- 各ファイルアクセスモードの詳細な実行規則や Codex CLI の制約を確認するときは、対応する正本仕様を直接読む。

## hash
- f91c2bdf4465ac41f25992aa68d2b5dd683ae48609a6bb4abae4fdc63a1dbe73

# `indexing`

## Summary
- indexing 用の agent 呼び出しパラメータを構築するファイルと、INDEX.md エントリーの JSON Schema を定義するファイルを含む。`cmoc indexing` の呼び出し条件、入力の渡し方、出力形式を確認するための入口。

## Read this when
- `cmoc indexing` の目次情報生成用 agent 呼び出しの構築方法を確認するとき。
- indexing 用エントリーの入力・出力形式や検証条件を確認するとき。

## Do not read this when
- indexing の実行本体や生成された目次情報そのものを確認するとき。
- prompt の共通組み立てや、他サブコマンド向けの呼び出し設定だけを確認したいとき。

## hash
- 05d354f9306a4d79e5cdde86862b45fca33f2443725b3db2a3a55045ad235bb7

# `oracle`

## Summary
- `cmoc oracle edit`、`investigation`、`review` 各サブコマンドの agent call 構築を担う oracle src のディレクトリ。完全プロンプトの生成・保存、TUI 起動パラメータ、レビュー用 Structured Output 契約への入口を提供する。

## Read this when
- `cmoc oracle` 配下の TUI 起動パラメータ、完全プロンプト保存、モデル・推論強度・ファイルアクセス設定を確認または変更するとき。
- `cmoc oracle review` の所見列挙・判定・理由検証・マージ処理や Structured Output schema を調査するとき。
- edit、investigation、review の agent call 構成と、それぞれの入力・出力契約の対応関係を確認するとき。

## Do not read this when
- 共通 ACP パラメータ定義、パス解決、共通 prompt builder の仕様だけを確認するとき。
- oracle file の編集内容、編集担当 agent のプロンプト仕様、またはレビュー基準そのものを確認するとき。
- 特定のサブコマンドの実装や schema だけを確認でき、ディレクトリ全体の構成を知る必要がないとき。

## hash
- b1b1b746e4b7e045b8b7df9033ac277af178355e499f4bc5440956e6b24423ae

# `session`

## Summary
- `cmoc session join` の merge conflict 解消に向けて、AI 呼び出しへ渡す入力条件・指示内容・実行設定を組み立てる入口。競合ファイルの正規化と、conflict 解消に必要な範囲の制御が中心。

## Read this when
- `cmoc session join` で merge conflict marker を解消する呼び出し条件や、AI に渡す指示内容・実行設定を確認したいとき。
- 競合ファイルの扱いを変えたいとき、または conflict 解消時に許される編集範囲や品質設定の根拠を確認したいとき。

## Do not read this when
- session join の通常の接続や同期処理を探しているときは、join 本体の実装や周辺の session モジュールを先に読む。
- merge conflict 解消の実行結果そのものや後段の適用処理を知りたいときは、このパラメータ生成ではなく、呼び出し先の実行経路を読む。

## hash
- bf40a25ab5021c33ab48527dccecbcbea01a82485dd3232f13b96888e803c66f

# `tui`

## Summary
- cmoc tui の AI エージェント呼び出しに関する oracle src 群をまとめた領域。TUI 用の構造化パラメータスキーマ、実行プロンプトとアクセス規則の解決、起動パラメータ生成を扱う。

## Read this when
- cmoc tui のプロンプト構成、AgentCallParameter、モデル・推論設定、ファイルアクセスモード、標準フラグ、または関連する構造化スキーマを変更・調査するとき。

## Do not read this when
- 共通の完全プロンプト生成規則だけを調査するときは、共通プロンプトビルダーを直接読む。
- TUI の画面表示・対話処理・エージェント実行処理だけを調査するときは、それぞれの担当実装を直接読む。

## hash
- 13d2ed4368c319ae10cc7524b05177e2950a04539cf0a17f7bb7b06baceea2cc

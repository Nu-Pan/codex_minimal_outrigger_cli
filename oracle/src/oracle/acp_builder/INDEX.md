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

# `common`

## Summary
- oracle ACP builder の共通部品を定義する oracle src 群への入口。ACP builder の各生成処理で共有される状態、ルール、出力結果の正本仕様断片を扱う。
- 個別の builder 実装ではなく、builder 間で共有される概念や型の仕様を確認するためのまとまり。

## Read this when
- ACP builder 全体で共通して使う状態、ルール、結果表現の正本仕様断片を確認したいとき。
- ACP builder の複数領域にまたがる挙動を実装・テストへ反映する前に、共有概念の境界を確認したいとき。
- 下位要素のどれを読むべきか、共通部品の責務から絞り込みたいとき。

## Do not read this when
- 特定の builder の個別仕様だけを確認したいとき。
- realization code 側の実装詳細やテスト構成を確認したいとき。
- ACP builder と無関係な oracle src の仕様を探しているとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `edit`

## Summary
- `cmoc oracle edit` の TUI 起動パラメータを構築する実装。ユーザー指示を組み込んだ完全プロンプトを保存し、固定のモデル・推論強度・ファイルアクセス・実行前インデックス設定を持つ `AgentCallParameter` を返す。

## Read this when
- `cmoc oracle edit` の TUI 起動条件、プロンプト生成、ユーザー指示の組み込み、起動パラメータの固定値を変更・確認するとき。
- 完全プロンプトの保存先や oracle 専用ファイルアクセス設定との連携を確認するとき。

## Do not read this when
- `cmoc oracle edit` の編集プロンプト本文や oracle 編集規則そのものを確認したいとき。
- TUI 起動以外の agent call パラメータ構築や一般的な prompt builder の挙動だけを調べるとき。

## hash
- 79050f6a20d5e9e5eac5d9a1925591b3976ac1d0d06bfbd59452344cfd99077b

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

# `review`

## Summary
- oracle review の Structured Output schema と prompt 構築実装をまとめたディレクトリ。所見の生成・採否判定・重複整理・妥当性検証における出力契約とエージェント呼び出し設定の入口。

## Read this when
- `cmoc oracle review` の所見生成、採否判定、重複整理、賛否理由検証の出力契約を確認するとき。
- レビュー用 prompt の入力、oracle-only 読み取り制約、モデル設定、Structured Output の接続を調査・変更するとき。
- 所見の重複排除・統合、既知理由との差分抽出、所見がない場合の出力境界を確認するとき。

## Do not read this when
- oracle review の所見探索手順や判定基準そのものを確認するとき。
- agent call parameter の共通生成処理や共通 Structured Output 定義だけを確認するとき。
- レビュー結果の CLI 表示、永続化、実際のファイル編集処理を調査するとき。

## hash
- b23b0373eb00b94bd0b62153a55976a236986732df4bbf20330d8be2b3c7ee9e

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
- `launch_tui.py` は `cmoc tui` 起動時の呼び出し条件を組み立てる入口で、編集後プロンプトの保存や起動用 `AgentCallParameter` の生成に関心があるときに読む。TUI 本体や画面制御ではなく、起動前に固定されるモデル・推論強度・ファイルアクセス方針を確認するための位置づけ。
- `resolve_parameter.json` は AI Agent CLI/TUI に渡す実行条件の構造と検証基準を定める。役割・概要・ゴール・ファイルアクセスモード、そして読むべき標準文書の要否判定を変更・確認するときに読む。
- `resolve_parameter.py` は `cmoc tui` の実行パラメータ決定の正本で、TUI から AI 呼び出しへ渡すモデル選択、推論強度、ファイル参照方針、生成プロンプトの組み立てを追うときに読む。

## Read this when
- `cmoc tui` の起動パラメータ、保存される完全プロンプト、または起動時に固定されるモデル・推論強度・ファイルアクセス方針を変えたいとき。
- 元プロンプトを共通プロンプトへどう束ねて、どのファイルへ保存してからエージェント呼び出しに渡すかを確認したいとき。
- AI Agent CLI/TUI の実行条件を構造化する JSON Schema、またはそれに基づく判定結果を扱うとき。
- `cmoc tui` の実行パラメータ決定の根拠や、固定で強制している方針を追いたいとき。

## Do not read this when
- `cmoc tui` の実行本体、エディタ選択、対話 UI の制御を追いたいだけのとき。
- 実行パラメータ解決や別の prompt 構築経路ではなく、TUI 起動用の呼び出し条件そのものを見たいとき。
- INDEX.md 用エントリーの書き方やルーティング文の品質基準だけを確認したいときは、別の標準定義を直接読む。
- oracle file と realization file の一般的な責務境界だけを確認したいときは、個別の実装定義ではなく基本定義側を読む。

## hash
- b215db884778a47f38c78337213eb69d402dcc2dc53ec27964b91c7a4d7c0507

# `__init__.py`

## Summary
- `oracle.acp_builder.apply.fork` と同じ import 経路を実装側に用意するための互換 package 初期化ファイル。本文は互換 package であることを示す docstring のみを持ち、具体的な処理や公開 API の定義は持たない。

## Read this when
- `oracle.acp_builder.apply.fork` 互換 package の存在理由を確認したいとき。
- この package 直下の実装を読む前に、package 自体が処理本体ではなく互換用の入口であることだけを確認したいとき。

## Do not read this when
- fork 適用処理の具体的な実装、関数、クラス、入出力を調べたいとき。
- 互換 package ではなく oracle 側の正本仕様断片を確認したいとき。
- package 初期化 docstring 以外の実行時挙動や副作用を探しているとき。

## hash
- c5707d270af058dc9b548e1d49ffefdd38c20a0785a67a293523f2be83ebc266

# `_common.py`

## Summary
- apply fork の ACP builder 群で共通利用する補助をまとめる実装ファイル。repo root 解決、oracle builder import 経路の準備、oracle 側 ACP parameter を realization 側公開型として受け渡す境界を扱う。

## Read this when
- apply fork の ACP builder が oracle 側 builder を呼び出す前処理を確認・変更したいとき。
- packaged layout と開発 tree layout の両方で oracle builder を import 可能にする処理を確認したいとき。
- oracle 側から返る ACP parameter と realization 側の公開型の受け渡し境界を確認したいとき。

## Do not read this when
- apply fork 以外の ACP builder の個別ロジックを確認したいとき。
- ACP parameter のデータ構造や公開型そのものの定義を確認したいとき。
- oracle builder の具体的な parameter 生成内容を確認したいとき。

## hash
- 065b46638098a92fc0239c40d1f390156b48ed492dee52caa72e04a2badfbe17

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向け変更要約を組み立てる実装。agent call parameter の生成は対応する oracle 実装へ委譲し、生成結果を realization 側の型へ変換する。

## Read this when
- `cmoc apply fork` の変更要約 agent call parameter 生成、oracle builder への委譲、または oracle parameter から realization parameter への変換経路を確認・変更したいとき。

## Do not read this when
- `cmoc apply fork` 全体の実行フロー、fork 作成、branch 操作、または diff 生成そのものを調べたいときは、より上位の apply fork 実装へ進む。
- 変更要約の正本仕様や agent prompt の人間意図を確認したいときは、対応する oracle 側の builder を読む。
- 汎用的な git 操作 helper、path model、または ACP 共通型の定義を調べたいだけなら、それぞれの共通実装・基本型定義へ進む。

## hash
- 953844150e43aae9519c0790bc24357d2ab0b3efe4e05ac9ceb1064eb2c902db

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` でファイル単位の所見列挙を行うための agent call parameter を構築する薄い realization 側 builder。
- 実処理は oracle 側の同目的 builder に委譲し、repo root 解決、oracle src の import 準備、oracle parameter から realization 側 `AgentCallParameter` への変換だけを担う。

## Read this when
- `cmoc apply fork` のファイル単位所見列挙 agent を呼ぶための parameter 構築経路を確認したいとき。
- realization 側 builder が oracle 側 builder をどのように呼び出し、戻り値を `AgentCallParameter` に適合させるかを確認したいとき。
- `target_path` がファイル単位所見列挙用 parameter 構築に渡される境界だけを確認したいとき。

## Do not read this when
- 所見列挙のプロンプト内容、出力条件、正本仕様を確認したいときは、委譲先の oracle 側 builder を読む。
- repo root 解決、oracle src import 準備、oracle parameter 変換の共通挙動を確認したいときは、共通 helper の定義を読む。
- `cmoc apply fork` コマンド全体の制御フロー、CLI 引数処理、またはテスト観点を調べたいときは、それぞれの呼び出し元やテストを読む。

## hash
- 7f348f0ca54f4b074d5e43be005498ea92f45db03c66c9725e905c528f9bba40

# `finding_application.py`

## Summary
- `cmoc apply fork` の所見適用用 agent call parameter を構築する realization 側の薄い builder。repo root 解決と oracle src の import 準備を行い、対応する oracle builder の結果を realization 側の `AgentCallParameter` へ適合して返す入口を担う。

## Read this when
- `cmoc apply fork` の所見適用で、findings から agent call parameter を得る realization 側の呼び出し入口を確認したいとき。
- 対応する oracle builder を realization 実装からどのように呼び出し、戻り値を `AgentCallParameter` に変換しているか確認したいとき。

## Do not read this when
- 所見適用プロンプトや agent call parameter の正本仕様そのものを確認したいときは、対応する oracle 側の実装を読む。
- repo root 解決、oracle src の import 可能化、oracle parameter の適合処理という共通 helper の詳細を確認したいだけのときは、共通処理側を読む。

## hash
- f20f8f2dab686c194560fba1c68209b00301cb133ebd3bb06f1b4437124840f4

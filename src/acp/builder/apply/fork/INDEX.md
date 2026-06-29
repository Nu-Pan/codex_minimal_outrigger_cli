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
- apply fork 系の ACP builder が共有する補助処理を置く実装。oracle/src を import 可能にする境界処理と、oracle 側 builder が返した AgentCallParameter をそのまま runtime 側へ渡す薄い adapter を担う。
- repo-root 解決は既存の apply builder 側の import 境界を保ったまま basic.path_model に委譲し、このファイル自体は正本側 ACP 型や schema を複製しない。

## Read this when
- apply fork の ACP builder で oracle/src を import できない問題、または oracle parameter を runtime 側へ渡す境界を調べるとき。
- oracle 側 ACP builder と realization 側実行コードの型境界を変更する必要があるとき。
- apply fork 系 builder の複数箇所で共通して使う import 準備や parameter adapter の責務を確認するとき。

## Do not read this when
- 個別の apply fork prompt の本文、モデル選択、file access mode などを組み立てる条件を調べたいだけのとき。oracle 側の builder 本体を読む方が直接的。
- repo-root 解決そのものの仕様や path model の定義を確認したいとき。このファイルは解決処理を所有せず、path model 側に委譲している。
- AgentCallParameter や enum 型そのものの定義を調べたいとき。このファイルはそれらを所有せず、型定義は oracle 側 ACP basic にある。

## hash
- 1a8500a83a16c58ced3615d82f3a1a0faa597b8308fde60f2afbe75f394cf30a

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、変更要約生成用の agent call parameter を組み立てる builder 実装。repository root の解決、oracle src の import 準備、oracle 側 builder への委譲を担う。

## Read this when
- `cmoc apply fork` で raw git diff から変更要約 agent call parameter を作る経路を確認したいとき。
- 変更要約用 builder が oracle 側の対応実装をどのように呼び出し、返却 parameter を runtime 側へ渡しているかを追うとき。
- apply fork の作業レポートや変更要約生成に対応する oracle 側 JSON schema との結び付きを確認したいとき。

## Do not read this when
- 変更要約そのものの prompt 内容や出力方針を確認したいときは、oracle 側の対応する builder または JSON 定義を読む。
- repository root 解決、oracle src import 準備、oracle parameter の適用処理の共通実装を変更したいときは、共通 helper 側を読む。
- `cmoc apply fork` 全体の制御フロー、fork 作成、git 操作、または他種の agent call parameter 生成を調べたいだけのときは、それぞれの責務を持つ上位または別 builder を読む。

## hash
- f66cb8052f46a9e67df33ca46dbb96179e462c292c336b29a652cd39c9b79e75

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
- `cmoc apply fork` の所見適用向けに agent call parameter を構築する realization implementation。repository root の解決と oracle src の import 可能化を共通 helper に委ね、oracle 側 builder の結果を runtime 側へ返す入口を担う。

## Read this when
- `cmoc apply fork` で検出済み所見を適用する agent 呼び出しパラメータの組み立て経路を確認・変更したいとき。
- 所見リストが oracle 側 builder に渡され、runtime 側の `AgentCallParameter` として返るまでの橋渡しを確認したいとき。
- apply fork 系 builder のうち、計画生成や判定ではなく所見適用専用のパラメータ構築を扱う箇所を探しているとき。

## Do not read this when
- repository root の解決、oracle src の import 可能化、oracle parameter の変換規則そのものを変更したいときは、共通 helper 側を読む。
- 所見適用の prompt・指示文・詳細なパラメータ内容を確認したいときは、oracle 側 builder を読む。
- `cmoc apply fork` 以外の apply 系 command や、所見の検出・分類・生成ロジックを調べたいだけのとき。

## hash
- 3735683d336cf4b544bf4099e4ed204ceca1cdeadd5e534523d379f0e1719ff2

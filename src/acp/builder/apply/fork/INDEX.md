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
- apply fork 系の ACP builder が共有する補助処理を置く実装。oracle 側の builder で作られた parameter を runtime 側の AgentCallParameter へ変換し、oracle/src を import 可能にする境界処理を担う。
- repo-root 解決は既存の apply builder 側の import 境界を保ったまま basic.path_model に委譲し、このファイル自体は enum 値と structured output schema path の橋渡しに責務を絞っている。

## Read this when
- apply fork の ACP builder で oracle/src を import できない問題、oracle parameter から runtime AgentCallParameter への変換、または structured output schema path の受け渡しを調べるとき。
- oracle 側 ACP builder と realization 側実行コードの型・enum 境界を変更する必要があるとき。
- apply fork 系 builder の複数箇所で共通して使う import 準備や parameter adapter の責務を確認するとき。

## Do not read this when
- 個別の apply fork prompt の本文、モデル選択、file access mode などを組み立てる条件を調べたいだけのとき。oracle 側の builder 本体を読む方が直接的。
- repo-root 解決そのものの仕様や path model の定義を確認したいとき。このファイルは解決処理を所有せず、path model 側に委譲している。
- AgentCallParameter や enum 型そのものの定義を調べたいとき。このファイルはそれらを利用して変換するだけで、型定義は basic.acp 側にある。

## hash
- 4fd222442ce030d64d138f103f7d4bbad4dc69bbdfd7e3cadca5e37d1f5ea714

# `change_summary.json`

## Summary
- 変更内容を意味上のカテゴリごとにまとめ、各カテゴリで何を変えたかと根拠となる主要な変更箇所を記録するための出力契約を定義する。
- 差分適用や派生作業の結果を、人間がレビューしやすい変更要約として構造化する場面への入口になる。

## Read this when
- 差分適用後の変更要約をどの粒度でカテゴリ分けするか確認したいとき。
- 変更カテゴリ、変更内容の説明、主要な変更箇所をまとめた機械可読なレポートを生成・検証するとき。
- 空ではない変更要約を前提に、レビュー用の結果データを組み立てる処理を確認するとき。

## Do not read this when
- 個々の差分の検出方法、パッチ適用手順、fork 作成や実行制御の挙動を確認したいとき。
- 変更要約の表示文面や CLI 出力全体の整形だけを確認したいとき。
- 特定カテゴリに含めるべき具体的な変更ファイルを調べたいだけのとき。

## hash
- 51ffe6e61588c7c347494a36267c02b8d48f69f6e264fcaf396096938cdd672d

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向けに、変更要約生成用の agent call parameter を組み立てる builder 実装。repository root の解決、oracle src の import 準備、oracle 側 builder への委譲、realization 側 JSON 定義への適用を担う。

## Read this when
- `cmoc apply fork` で raw git diff から変更要約 agent call parameter を作る経路を確認したいとき。
- 変更要約用 builder が oracle 側の対応実装をどのように呼び出し、realization 側の parameter へ変換しているかを追うとき。
- apply fork の作業レポートや変更要約生成に対応する JSON 設定ファイルとの結び付きを確認したいとき。

## Do not read this when
- 変更要約そのものの prompt 内容や出力方針を確認したいときは、oracle 側の対応する builder または JSON 定義を読む。
- repository root 解決、oracle src import 準備、oracle parameter の適用処理の共通実装を変更したいときは、共通 helper 側を読む。
- `cmoc apply fork` 全体の制御フロー、fork 作成、git 操作、または他種の agent call parameter 生成を調べたいだけのときは、それぞれの責務を持つ上位または別 builder を読む。

## hash
- eef0e38ef46b45a9341331b84b1043d14a5fadb5ee3029bda87d30841b5d4013

# `file_finding_enumeration.json`

## Summary
- 実装調査で見つかった問題点を、根拠位置・要求仕様・観測された実装・修正方針とともに列挙するための JSON Schema。
- apply fork 周辺の実装レビュー結果を機械的に検証できる形で返すための出力契約を定める。

## Read this when
- 実装に対する所見を出力する処理の契約を確認したいとき。
- 仕様・実装ファイル上の根拠位置を含むレビュー結果を生成または検証するとき。
- 所見ごとに要求、現状、問題理由、修正方針を揃えて扱う必要があるとき。

## Do not read this when
- 実装差分そのものや修正対象のコードを調べたいだけのとき。
- ファイル探索や fork apply の制御フローを理解したいとき。
- INDEX.md 用のルーティング文書の一般規約を確認したいとき。

## hash
- 0bed168a2a89c47730cdc914c08c08f2a3ad4022595c4b910c5d8ff9ca335524

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` のファイル単位の所見列挙用 agent call parameter を組み立てる realization 側 builder。repo root 解決と oracle src import 準備を行い、対応する oracle builder の結果を realization 側の JSON 定義に合わせて変換して返す入口である。

## Read this when
- `cmoc apply fork` でファイル単位の所見列挙を行う agent call parameter の生成経路を確認・変更したいとき。
- apply fork 系 builder が oracle builder を呼び出し、realization 側の JSON 定義へ適用する委譲パターンを確認したいとき。
- 対象 path を受け取る所見列挙 builder の呼び出し境界、repo root 解決、oracle src import 準備の流れを確認したいとき。

## Do not read this when
- 所見列挙プロンプトや parameter の正本仕様そのものを確認したいとき。この対象は oracle builder へ委譲する薄い adapter であり、仕様本文は対応する oracle 側を読む。
- agent call parameter の共通変換処理、repo root 解決、oracle src import 準備の実装詳細を変更したいとき。この対象ではなく共通 helper 側を読む。
- `cmoc apply fork` の他の段階や、ファイル単位ではない builder の生成経路を確認したいとき。

## hash
- 9922592f7cfe4a928d0e5ad56bc1a8131d656e26617b69cbd4a3ddc4e81e7b34

# `finding_application.py`

## Summary
- `cmoc apply fork` の所見適用向けに agent call parameter を構築する realization implementation。repository root の解決と oracle src の import 可能化を共通 helper に委ね、oracle 側 builder の結果を ACP 側の `AgentCallParameter` へ変換する入口を担う。

## Read this when
- `cmoc apply fork` で検出済み所見を適用する agent 呼び出しパラメータの組み立て経路を確認・変更したいとき。
- 所見リストが oracle 側 builder に渡され、realization 側の `AgentCallParameter` として返るまでの橋渡しを確認したいとき。
- apply fork 系 builder のうち、計画生成や判定ではなく所見適用専用のパラメータ構築を扱う箇所を探しているとき。

## Do not read this when
- repository root の解決、oracle src の import 可能化、oracle parameter の変換規則そのものを変更したいときは、共通 helper 側を読む。
- 所見適用の prompt・指示文・詳細なパラメータ内容を確認したいときは、oracle 側 builder を読む。
- `cmoc apply fork` 以外の apply 系 command や、所見の検出・分類・生成ロジックを調べたいだけのとき。

## hash
- c47f9ecd8345949948ceb13d2f7edcc6e104993091f6298b7467f47610bdbaee

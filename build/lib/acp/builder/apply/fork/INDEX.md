# `__init__.py`

## Summary
- `oracle.acp_builder.apply.fork` と互換の package であることだけを示す初期化ファイル。互換 package としての存在確認や import 境界を判断するための入口になる。

## Read this when
- `oracle.acp_builder.apply.fork` 互換 package の有無や package 初期化位置を確認したいとき。
- apply fork 周辺で、互換 package として扱われる import パスを確認したいとき。

## Do not read this when
- apply fork の具体的な処理内容、関数、クラス、状態遷移を調べたいとき。
- 互換 package ではなく、実装ロジックやテスト対象の詳細を確認したいとき。

## hash
- c5707d270af058dc9b548e1d49ffefdd38c20a0785a67a293523f2be83ebc266

# `_common.py`

## Summary
- apply fork ACP builder が共通して使う補助処理を置く。リポジトリルートの解決、oracle src を実行時 import 可能にするための探索と sys.path 追加、runtime ACP 型に合わせるための parameter 受け渡しを扱う。
- fork 系 builder 本体の処理ではなく、oracle 側 builder 実装を参照するための import 準備と ACP parameter の境界調整を担う入口である。

## Read this when
- apply fork ACP builder で oracle 側 module を import できない問題を調べるとき。
- apply fork ACP builder が使うリポジトリルート解決、oracle src 探索、sys.path 追加の挙動を変更するとき。
- basic 側 ACP 型と oracle 側 runtime ACP 型の受け渡し境界を確認するとき。

## Do not read this when
- apply fork ACP builder の個別の生成内容や分岐ロジックを調べたいだけのとき。
- oracle file そのものの正本仕様、oracle src の実装内容、または oracle 側 ACP 型定義を確認したいとき。
- fork 以外の ACP builder、CLI 全体の routing、または path placeholder の一般仕様を調べたいとき。

## hash
- 8f2faead7113a3f665f4405f064544614a0165f567433fa39fc0fe8e779dfbd1

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向け変更要約 agent call parameter を構築する builder。oracle 側の変更要約 builder を呼び出し、repository root 解決、oracle src import 準備、oracle parameter から realization 側 parameter への変換を担う。

## Read this when
- `cmoc apply fork` の変更要約生成に渡す agent call parameter の組み立て経路を確認したいとき。
- raw git diff が変更要約用の oracle builder に渡され、realization 側の `AgentCallParameter` へ変換される流れを確認したいとき。
- apply fork 系 builder で oracle src を import 可能にする共通処理の利用箇所を確認したいとき。

## Do not read this when
- 変更要約 prompt や parameter の正本仕様そのものを確認したいときは、対応する oracle src を読む。
- repository root 解決、oracle src import 準備、oracle parameter 変換の共通処理を確認したいときは、apply fork builder の共通処理を読む。
- `cmoc apply fork` 全体の CLI 実行制御や git 操作を確認したいときは、この builder ではなく apply fork の実行側を読む。

## hash
- 953844150e43aae9519c0790bc24357d2ab0b3efe4e05ac9ceb1064eb2c902db

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` で対象ファイルごとの所見列挙を行うための agent call parameter builder。
- repository root の解決、oracle src の import 準備、oracle 側 builder の呼び出し、realization 側の `AgentCallParameter` への変換を担う薄い adapter。

## Read this when
- `cmoc apply fork` のファイル単位所見列挙 agent call parameter がどこで構築されるか確認したいとき。
- oracle 側の所見列挙 builder を realization 側から呼び出す経路や、oracle parameter から `AgentCallParameter` への変換点を調べるとき。
- 対象パスを受け取って所見列挙用 parameter を返す処理の実装を変更・確認するとき。

## Do not read this when
- 所見列挙の正本仕様や prompt 構成そのものを確認したいときは、対応する oracle src を読む。
- `cmoc apply fork` 全体の制御フロー、実行手順、他の agent call 種別を調べたいときは、より上位の apply/fork 実装へ進む。
- oracle parameter の変換共通処理、repository root 解決、oracle src import 準備の詳細を調べたいときは、共通 adapter 実装を読む。

## hash
- 7f348f0ca54f4b074d5e43be005498ea92f45db03c66c9725e905c528f9bba40

# `finding_application.py`

## Summary
- `cmoc apply fork` で所見適用用の agent call parameter を構築する builder。
- 正本側の所見適用 builder を呼び出し、repository root 解決、oracle src import 準備、oracle parameter から実行側 parameter への変換を担う薄い adapter。

## Read this when
- `cmoc apply fork` の所見適用処理で、findings から agent call parameter を作る経路を確認・変更したいとき。
- oracle src の builder を realization 側から利用するための import 準備や parameter 変換の接続点を確認したいとき。
- 所見適用用 builder がどの正本実装に委譲しているかを確認したいとき。

## Do not read this when
- 所見そのものの形式、内容、生成規則を確認したいとき。
- agent call parameter の共通変換処理や repository root 解決の詳細を確認したいとき。
- `cmoc apply fork` の所見適用以外の builder や apply fork 全体の制御フローを調べたいとき。

## hash
- f20f8f2dab686c194560fba1c68209b00301cb133ebd3bb06f1b4437124840f4

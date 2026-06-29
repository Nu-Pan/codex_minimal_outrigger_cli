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
- apply fork の ACP builder 群で共通して使う、リポジトリルート解決、oracle 側 ACP builder パッケージの import 経路補正、ACP パラメータ型の受け渡しを担う補助モジュール。
- oracle 側実装が実行時に import 可能であることと、実装側の ACP 型が oracle 側の実行時型を再公開している前提を、この領域の builder から共有する入口として位置づける。

## Read this when
- apply fork の builder 実装で、リポジトリルートをどう解決して oracle 側モジュールを読み込める状態にしているか確認したいとき。
- packaged layout と開発ツリー layout の違いにより、oracle 側 ACP builder の import が失敗する問題を調査するとき。
- apply fork の builder が受け取る ACP パラメータを oracle 側 API へ渡す際の型境界や変換有無を確認するとき。

## Do not read this when
- 個別の apply fork 用 ACP の組み立て内容、プロンプト、引数構造を確認したいだけのとき。
- oracle 側の ACP builder の正本仕様や実装内容そのものを確認したいとき。
- リポジトリルート解決や oracle 側 import 経路補正と関係しない、他領域の builder や CLI 挙動を調査しているとき。

## hash
- 8f2faead7113a3f665f4405f064544614a0165f567433fa39fc0fe8e779dfbd1

# `change_summary.py`

## Summary
- `cmoc apply fork` の作業レポート向け変更要約を組み立てる実装。agent call parameter の生成は対応する oracle 実装へ委譲し、生成結果を realization 側の型へ変換する。
- ACP branch diff を読み、差分ヘッダーから変更 path を抽出して、変更がある場合とない場合の要約ペイロードを出力先へ保存する。

## Read this when
- `cmoc apply fork` の変更要約 agent call parameter 生成、oracle builder への委譲、または oracle parameter から realization parameter への変換経路を確認・変更したいとき。
- ACP branch diff から作業レポート用の変更 path 一覧を作る処理、変更なしの場合の要約生成、または要約ファイルの保存処理を確認・変更したいとき。
- git diff の `diff --git` 行から path を取り出す最小限の parsing 挙動を確認・変更したいとき。

## Do not read this when
- `cmoc apply fork` 全体の実行フロー、fork 作成、branch 操作、または diff 生成そのものを調べたいときは、より上位の apply fork 実装へ進む。
- 変更要約の正本仕様や agent prompt の人間意図を確認したいときは、対応する oracle 側の builder を読む。
- 汎用的な git 操作 helper、path model、または ACP 共通型の定義を調べたいだけなら、それぞれの共通実装・基本型定義へ進む。

## hash
- cc2a9e6219cee7568fdf4f24f83575f00d22129c50d3f56a842be80ccfbf1228

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

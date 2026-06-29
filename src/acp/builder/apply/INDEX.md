# `__init__.py`

## Summary
- oracle 側の apply builder package と対応する互換 package であることだけを示す package 初期化要素。実処理や公開 API の定義ではなく、同領域を package として扱うための入口に位置づけられる。

## Read this when
- apply builder 領域が oracle 側の package 構造と対応しているかを確認したいとき。
- package 初期化部分に実装意図や互換性メモがあるかを確認したいとき。

## Do not read this when
- apply builder の具体的な処理、変換、適用ロジックを調べたいとき。その場合は同 package 内の実装本体を読む。
- 公開関数、クラス、入出力仕様、エラー処理を確認したいとき。この対象にはそれらの定義は含まれない。

## hash
- a6df93a5897c266e6f48287739c8bf8192733ea9fb19e2f6eb05a302f4165b06

# `fork`

## Summary
- apply fork 系の agent call parameter builder 群をまとめる realization 側 package。oracle 側 builder への委譲、repository root 解決、oracle src import 準備、runtime 側 parameter への橋渡しを担う。
- 変更要約、ファイル単位の所見列挙、検出済み所見の適用など、`cmoc apply fork` の各段階で使う agent 呼び出しパラメータ生成の入口を置く。

## Read this when
- `cmoc apply fork` で agent call parameter がどの realization 側 builder から作られ、oracle 側 builder へどう委譲されるかを確認したいとき。
- apply fork 系 builder 共通の repository root 解決、oracle src import 準備、oracle parameter を runtime 側へ渡す境界を調べたいとき。
- 変更要約、ファイル単位の所見列挙、所見適用に対応する builder の入口を探しているとき。
- oracle 側 ACP builder と realization 側実行コードの型境界や adapter 責務を変更する必要があるとき。

## Do not read this when
- apply fork の prompt 本文、JSON schema、モデル選択、file access mode などの正本仕様を確認したいときは、対応する oracle 側 builder や schema を読む。
- `cmoc apply fork` 全体の制御フロー、fork 作成、git 操作、実行 orchestration を調べたいときは、上位の apply fork 実装へ進む。
- repository root 解決そのものの仕様や path model の定義を確認したいときは、path model 側を読む。
- AgentCallParameter や enum 型そのものの定義を調べたいときは、ACP basic 側の型定義を読む。
- apply fork 以外の apply 系 command や、所見の検出・分類・生成ロジックを調べたいだけのとき。

## hash
- 54543fb718f22cf570ddc6de6604977c32eb4d9ae0b40be48edaf783b96dc5c1

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
- apply fork 向け ACP builder 群を置く領域。各 builder は realization 側の入口として、必要に応じてリポジトリルート解決や oracle 側 import 準備を行い、oracle 側 builder の結果を realization 側の agent call parameter 型へ適合させる。
- 変更要約、ファイル単位所見列挙、所見適用など、`cmoc apply fork` の個別 agent 呼び出しパラメータ構築に関する本文へ進むための入口になる。

## Read this when
- `cmoc apply fork` で呼び出す agent call parameter の realization 側 builder 群から、目的に合う本文を選びたいとき。
- oracle 側 builder への委譲、oracle src の import 準備、または oracle parameter から realization 側 `AgentCallParameter` への変換に関わる apply fork 用実装を調べたいとき。
- 変更要約、ファイル単位所見列挙、所見適用のいずれかについて、呼び出し入口や保存・変換の境界を確認したいとき。

## Do not read this when
- `cmoc apply fork` 全体の制御フロー、fork 作成、branch 操作、CLI 引数処理、または diff 生成そのものを調べたいときは、上位の apply fork 実装へ進む。
- agent prompt、正本仕様、人間意図、出力条件そのものを確認したいときは、対応する oracle 側 builder や oracle 文書へ進む。
- apply fork に限らない汎用 git helper、path model、ACP 共通型、または他領域の builder を調べたいときは、それぞれの共通実装や対象領域へ進む。

## hash
- 4e035e0dd667d29d58127487c7eea0700beca76ca4d525785ea294b3ba84006f

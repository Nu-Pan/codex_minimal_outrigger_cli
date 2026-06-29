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
- apply fork 系の realization 側 ACP builder をまとめる package。各 builder は `cmoc apply fork` の変更要約、ファイル単位所見列挙、所見適用に必要な agent call parameter 構築入口を提供し、実処理は対応する oracle 側 builder に委譲する。
- この階層は、oracle src の import 準備、repo root 解決、oracle 側 parameter を runtime 側 `AgentCallParameter` へ渡す共通 adapter と、それを使う個別 builder への入口として位置づく。

## Read this when
- `cmoc apply fork` で agent call parameter を作る realization 側の入口を探しているとき。
- 変更要約、ファイル単位所見列挙、所見適用のいずれかで、oracle 側 builder への委譲経路と runtime 側 parameter への適合境界を確認したいとき。
- apply fork 系 builder に共通する oracle src import 準備、repo root 解決、oracle parameter adapter の責務を確認したいとき。

## Do not read this when
- apply fork の prompt 本文、出力 schema、モデル選択、file access mode などの正本仕様を確認したいとき。対応する oracle 側 builder や JSON 定義を読む。
- `cmoc apply fork` コマンド全体の制御フロー、fork 作成、git 操作、CLI 引数処理を調べたいとき。上位の command 実装や git 操作側を読む。
- repo-root 解決そのものの仕様、path model、`AgentCallParameter` や enum 型の定義を確認したいとき。この階層はそれらを所有せず、別の定義へ委譲している。

## hash
- 05186d93a9adaf3e96bfc4164f8cadacbba0d61e7244520e7c98c3760a576f65

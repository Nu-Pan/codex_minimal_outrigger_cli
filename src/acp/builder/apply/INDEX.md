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
- apply fork 系の ACP builder 実装をまとめるディレクトリ。各 builder は `cmoc apply fork` の変更要約、ファイル単位所見列挙、所見適用などの agent call parameter 構築入口を担い、実処理の多くを oracle 側 builder へ委譲する。
- この階層は、realization 側で repository root 解決、oracle src import 準備、oracle parameter から runtime 側 parameter への橋渡しを行う薄い adapter 群と、その共通 helper への入口として位置づく。

## Read this when
- `cmoc apply fork` で使う agent call parameter builder の realization 側入口を探すとき。
- 変更要約、ファイル単位所見列挙、所見適用など、apply fork 用 agent 呼び出しの種類ごとにどの builder を読むべきか切り分けたいとき。
- oracle 側 ACP builder と runtime 側実行コードの境界、特に oracle src import 準備や parameter adapter の責務を確認したいとき。
- apply fork 系 builder が oracle 側実装へ委譲する構造を把握してから、個別 builder または共通 helper へ進みたいとき。

## Do not read this when
- prompt 本文、出力 schema、モデル選択、file access mode などの正本仕様を確認したいときは、委譲先の oracle 側 builder や JSON 定義を読む。
- `cmoc apply fork` 全体の制御フロー、fork 作成、git 操作、CLI 引数処理を調べたいだけのときは、上位の command 実装を読む。
- repository root 解決そのものや path model の仕様を調べたいときは、path model 側の定義を読む。
- AgentCallParameter や enum 型そのものの定義を確認したいときは、ACP basic 側の型定義を読む。
- oracle 互換 package の存在確認だけで足り、個別 builder や共通 helper の挙動を読む必要がないとき。

## hash
- 7d1aec3d3b6469b62339576e4752f0b1d277ece9aa35137715b8779011fdbf5d

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
- apply fork 系の agent call parameter builder 実装をまとめる領域。各 builder は realization 側の入口として、repo root 解決、oracle src の import 準備、oracle 側 builder への委譲、oracle parameter から runtime 側 parameter への薄い適合を担う。
- 変更要約、ファイル単位所見列挙、所見適用など、`cmoc apply fork` の各 agent 呼び出しで使う parameter 構築経路と、それらが共有する import 境界・型境界の補助処理への入口になる。
- この領域自体は prompt 本文や ACP の正本仕様を所有せず、正本仕様断片を持つ oracle 側 builder と realization 側実行コードを接続する委譲層として位置づけられる。

## Read this when
- `cmoc apply fork` の agent call parameter 構築が、realization 側から oracle 側 builder へどのように委譲されているかを確認したいとき。
- apply fork 系の変更要約、ファイル単位所見列挙、所見適用のいずれかで、入力値から runtime 側 parameter へ至る薄い入口を探しているとき。
- oracle src を import 可能にする処理、repo root 解決、oracle parameter を realization 側へ渡す adapter など、apply fork 系 builder 間で共有される境界処理を確認したいとき。
- `oracle.acp_builder.apply.fork` と同じ import 経路を realization 側に用意する互換 package の存在理由を確認したいとき。

## Do not read this when
- apply fork の prompt 内容、モデル選択、file access mode、出力条件、AgentCallParameter の正本仕様そのものを確認したいとき。正本仕様断片を持つ oracle 側 builder を読む方が直接的。
- `cmoc apply fork` 全体の CLI 制御、git 操作、fork 適用処理、作業レポート全体の生成フローを調べたいとき。この領域は agent call parameter 構築の委譲入口に限られる。
- repo root 解決そのものの仕様、path model の定義、ACP 型や enum 型の定義を調べたいとき。この領域はそれらを所有せず、外部の定義へ委譲または依存している。
- package 初期化 docstring 以外の実行時挙動や副作用を探しているときは、互換 package の入口だけを読む必要はない。

## hash
- 8bf0c9d853176094f1a45df32c67777ceb93115bc71fcfcc3536947e4efd3b6b

# `__init__.py`

## Summary
- 旧来の import 経路を維持するための互換 package。
- 既存の参照を壊さないために残されており、realization 側と利用者向け公開面から同参照がなくなった時点で削除候補になる。

## Read this when
- 旧来の import 経路に対する互換性維持や削除可否を確認する。
- この package が残されている理由や、削除条件を確認する。

## Do not read this when
- 新しい実装責務や公開 API の仕様を確認したい場合。
- 互換 import 経路ではなく、実際の review oracle 処理本体を調べたい場合。

## hash
- 1cc0bee48cb44a0d598bc18b30385b88d2a2c6d769d3f20ac96b52c29afcd7f9

# `enumerate_finding.py`

## Summary
- レビュー finding 列挙用の互換 import 経路。canonical oracle 実装へ委譲し、symlink 経由でレビューした場合は prompt 内の oracle path を lexical path に戻して呼び出し事実を保持する。既存の互換 import 呼び出し元を調査・変更する際の入口。

## Read this when
- `acp.builder.review.oracle.enumerate_finding` の import 経路や呼び出し元を変更するとき
- symlink 経由の oracle path が review prompt にどう反映されるかを確認するとき
- canonical builder への移行完了と互換経路の削除可否を判断するとき

## Do not read this when
- canonical な finding 列挙処理そのものの仕様や実装を確認したいとき
- レビュー finding 列挙と無関係な builder や oracle path の処理を調査するとき

## hash
- 2ffda7572a382caaacc41ce17c74586aea14e3b5d05b26e53c02bd5df8572d34

# `judge_finding.py`

## Summary
- `acp.builder.review.oracle.judge_finding` からの既存 import を維持するための互換 shim です。レビュー finding 判定用の正本実装へ進む必要があるか、呼び出し元を整理してこの経路を廃止できるかを判断する入口として使います。

## Read this when
- この import 経路をたどっている呼び出し元を洗い出したいとき。
- 互換層を削除できるか確認したいとき。
- レビュー finding 判定の正本実装そのものを追いたいときは、ここではなく対応する oracle 側へ進むとき。

## Do not read this when
- レビュー finding 判定の実装詳細を知りたいだけのとき。
- この互換 import を残す必要がないかを判断するのではなく、正本実装の仕様や挙動だけを確認したいとき。

## hash
- 6f61d68f3f224bc69e03ab25a86f2453986f1efb8afe4c63183567815ef49ac7

# `merge_finding.py`

## Summary
- `cmoc review oracle` の所見マージ用パラメータを作る薄い実装層。正本 builder の戻り値に対して、`oracle-root` プレースホルダ定義の既知 typo だけを後処理で直す必要があるときに読む。

## Read this when
- review oracle の所見マージ用パラメータの実装を追うとき
- 正本 builder の出力をそのまま使わず、`prompt` だけを最小修正する理由を確認したいとき
- `oracle-root` のプレースホルダ定義 typo の互換対応や削除条件を確認したいとき

## Do not read this when
- 正本の所見マージ prompt 本体を変更したいときは、まず oracle 側の実装を読む
- `cmoc review oracle` 以外のサブコマンドのパラメータ生成を追いたいとき
- prompt の共通組み立てや Structured Output schema 全般を見たいだけのとき

## hash
- a34513231db4381f9b8519b2c7b44b837db8193587fe5de292d9f1ee860852f7

# `validate_finding_advocate.py`

## Summary
- `cmoc review oracle` の所見を擁護する理由を集めるための `AgentCallParameter` を組み立てる。正本側の prompt を受け取り、実装側で必要な最小の補正を加える薄いラッパーなので、この層を読む。

## Read this when
- `cmoc review oracle` の擁護側パラメータ生成の流れを追いたいとき。
- oracle 側の prompt から、実装側でどこだけ補正しているか確認したいとき。
- 所見本文と既知理由をそのまま保持したまま、返却パラメータだけを整形する責務を確認したいとき。

## Do not read this when
- review oracle の所見を新規に生成する本体の仕様を追うなら、対応する oracle 側の実装を先に読む。
- 補正後 prompt の文字列差分そのものだけを見たいなら、この薄いラッパーより正本側の実装を読む。
- 擁護側ではなく反証側の入力組み立てを見たいなら、`validate_finding_challenger` 系を読む。

## hash
- 57f0c360bd224ea691aad7be0384b972d17d79436a13a6ea3c5a16d24f2dc080

# `validate_finding_challenger.py`

## Summary
- `acp.builder.review.oracle.validate_finding_challenger` から正本の oracle 実装へ橋渡しする互換エントリ。呼び出し元の移行を終えるまで、この薄い再公開だけを担う。

## Read this when
- 旧い import 経路をまだ使っている呼び出し元があり、どの正本実装に移るべきか確認したいとき。
- 互換層を削除できる条件や、どの参照先が canonical かを確認したいとき。

## Do not read this when
- 実際の検証ロジックや引数仕様を知りたいときは、正本の oracle 実装を直接読む。
- 新しい機能追加や挙動変更をこの互換層で行う必要はない。

## hash
- 49ae85b7f6188d91ac9ed2f305777a1857bec0b65e41620c62d58ad6bf1c73f7

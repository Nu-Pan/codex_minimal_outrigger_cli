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
- review finding enumeration の互換 import 経路を提供するモジュール。canonical oracle builder を呼び出し、絶対 symlink が指定された場合は prompt 内の oracle path を解決済み path から lexical path に戻して、レビュー対象の指定を保持する。canonical 実装への移行完了後に削除できる。

## Read this when
- review finding enumeration の parameter builder の互換 import 経路や symlink 指定時の prompt path 保持を確認・変更するとき
- `acp.builder.review.oracle.enumerate_finding` からの既存 import を canonical oracle path へ移行するとき

## Do not read this when
- canonical な parameter builder の仕様や実装を確認したいときは、参照先の canonical 実装を直接読む
- review finding enumeration と無関係な review builder や一般的な AgentCallParameter 処理を確認するとき

## hash
- 6061e81cb1410b8a466e350703d2f1c48ac2f5bfd30596c98f8c6124e87f3e65

# `judge_finding.py`

## Summary
- review finding judgment の互換 import 経路を提供する薄いラッパー。canonical 実装を再公開し、旧 import caller の移行期間を支える。全 caller が canonical oracle path を直接参照するまでの暫定入口。

## Read this when
- review finding judgment の旧 import 経路や caller の移行状況を確認するとき
- 互換 import の削除可否を判断するとき

## Do not read this when
- review finding judgment の本体仕様や実装を確認したいときは、canonical oracle 実装を直接読む
- 旧 import 経路と無関係な review 処理を調査するとき

## hash
- b9e8169ee22552391a2c28b6c095b015d05dca902fac7f122146ee888e7aef4f

# `merge_finding.py`

## Summary
- 正本の review/oracle merge-finding builder を呼び出し、既知 typo に限って生成 prompt の placeholder 定義を補正する realization 実装。補正 helper は対象 marker 内の定義を限定的に置換し、該当しなければ prompt を変更しない。

## Read this when
- merge-finding review 用 agent-call parameter の生成や、既知の oracle-root placeholder typo 補正の挙動を確認・変更するとき。

## Do not read this when
- 正本 builder の仕様や prompt 本文そのものを確認したいときは、参照先の oracle src を直接読む。merge-finding 以外の review builder を扱うとき。

## hash
- 2aa8e85799039efc1a74937d43a4ce1e2ac667e709754c7612882b61e314db3e

# `validate_finding_advocate.py`

## Summary
- canonical advocate builder のパラメータ生成処理をラップし、生成された prompt に残る oracle root placeholder の既知 typo を一箇所だけ補正する実装。finding と既知の advocate/challenger 理由はそのまま canonical builder に渡し、補正後の AgentCallParameter を返す。

## Read this when
- validate finding の advocate 用 AgentCallParameter 生成や prompt の typo 補正を変更・レビューするとき
- canonical builder との委譲関係、dynamic input の byte-for-byte 保持、oracle root placeholder の補正条件を確認するとき

## Do not read this when
- advocate builder の canonical prompt 仕様そのものを確認したいときは、委譲先の oracle builder を直接読む
- review routing や finding の検証ロジック自体を変更・確認するとき
- prompt の共通仕様を確認するだけで、この補正ラッパーの挙動に関係しないとき

## hash
- c8395a666dc0e65d4a4b7c05858669399d98cee6c32622c90a7bf2d0029dbe6a

# `validate_finding_challenger.py`

## Summary
- challenger finding validation の互換 import 経路を提供する薄いラッパー。canonical oracle 実装から検証用パラメータ生成関数を再公開する。

## Read this when
- challenger finding validation の import 経路や互換 caller を調査・変更するとき
- canonical oracle 実装への移行状況や削除条件を確認するとき

## Do not read this when
- canonical な検証ロジック自体を変更・確認するとき
- challenger finding validation と無関係な review builder の処理を調査するとき

## hash
- 8db5befdf20ae0fbb8d94f7123529495f2ca943a246a3a07f275907ed242130b

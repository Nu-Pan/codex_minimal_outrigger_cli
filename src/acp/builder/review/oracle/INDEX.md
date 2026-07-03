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
- review finding enumeration の旧 import 経路を維持する互換 shim。canonical 実装の関数を再 export し、既存呼び出し元が移行するまでの入口としてだけ機能する。

## Read this when
- review finding enumeration について、旧 import 経路から canonical 実装へつながる互換層を確認したいとき。
- 旧 import 経路を使う呼び出し元の移行や、この互換層の削除可否を判断したいとき。

## Do not read this when
- review finding enumeration の実処理や parameter 構築内容を確認したいとき。canonical 実装を直接読む。
- 新しい review finding enumeration の仕様や挙動を調べたいだけで、旧 import 経路との互換性が関係しないとき。

## hash
- 805a7b8cd6d94fa944dc4c2db6b83efdde249951781858f5652ec2531168d438

# `judge_finding.py`

## Summary
- review finding judgment 用の旧 import path を維持する互換モジュール。実体は canonical oracle path 側にあり、この対象は既存 caller が旧 path から関数を import している間だけ再 export する入口である。

## Read this when
- 旧 path からの import 互換性、再 export 対象、または canonical oracle path への移行状況を確認したいとき。
- review finding judgment の caller を canonical oracle path へ移す作業で、削除可能条件を確認したいとき。

## Do not read this when
- review finding judgment の実装内容や parameter 生成ロジックを確認したいときは、canonical oracle path 側を読む。
- 新しい review 判定仕様や挙動を調べたいだけで、旧 import path の互換維持に関係しないとき。

## hash
- c2e355ca77538012de3c69dadd0dc317c82169763711c3e520541922c02e544d

# `merge_finding.py`

## Summary
- review oracle merge finding 用の agent call parameter を oracle src の builder から生成し、prompt 内の oracle root placeholder 表記だけを最小補正して返す薄い実装。
- oracle src 側の placeholder 生成不具合を吸収する一時的な互換処理を持ち、oracle src が正しい表記を出すようになった後に削除できる境界をコメントで示している。

## Read this when
- review oracle merge finding の agent call parameter 生成経路を確認・変更する場合。
- known findings を入力として渡す review oracle merge finding prompt の組み立て結果や structured output schema への接続を追う場合。
- prompt の placeholder 定義で oracle root 表記が補正される理由、範囲、削除条件を確認する場合。

## Do not read this when
- review oracle merge finding の正本 prompt 内容そのものを確認したい場合は、対応する oracle src を直接読む。
- placeholder 表記補正と無関係な review workflow 全体、CLI、永続状態、git 操作を調べる場合。
- agent call parameter の基本データ構造や共通 builder の仕様を調べる場合は、共通定義側を読む。

## hash
- 80e3f3d9dad597c0d434205368fa5b1ceecda22c8fbc650780e6ef7bd9c6ff11

# `validate_finding_advocate.py`

## Summary
- review oracle の finding advocate 検証用 AgentCallParameter を生成する realization 実装。oracle src の builder 結果を利用しつつ、正本側に残る `<oracle_root>` 表記ゆれだけをプロンプト上で最小補正して返す。

## Read this when
- review oracle の finding advocate 検証プロンプトを組み立てる経路を確認・変更したいとき。
- oracle src 由来の AgentCallParameter を realization 側で包み直す理由や、プロンプト中の `<oracle_root>` から `<oracle-root>` への限定的な補正条件を確認したいとき。
- dynamic input である finding や既知理由を変更せず、静的な oracle src の typo だけを扱う実装境界を確認したいとき。

## Do not read this when
- review oracle 以外の agent call parameter builder を調べたいとき。
- finding advocate 検証の正本プロンプト内容そのものを確認したいとき。この対象ではなく対応する oracle src または prompt standard を読む。
- typo 補正の方針ではなく、AgentCallParameter 型そのものや共通 builder 基盤を調べたいとき。

## hash
- 7111c4192cff8b09164626ba9bfec3d3a543e0d17313460e5ca6019bfab38d4c

# `validate_finding_challenger.py`

## Summary
- 旧 import path を維持するための互換モジュール。正本実装を canonical oracle path から再公開し、既存 caller が移行するまでの入口として機能する。

## Read this when
- 旧 import path から challenger finding validation の builder を import している呼び出し元との互換性を確認するとき。
- canonical oracle path への移行状況や、この互換モジュールを削除できる条件を確認するとき。

## Do not read this when
- challenger finding validation の実装内容や parameter 構築ロジックを確認したいときは、canonical oracle path の実装を読む。
- 新規 caller が利用すべき import path を確認したいだけなら、canonical oracle path 側を読む。

## hash
- 193a5392c8f2941fe14476d297db143c523c67a4970540d017d65eb5035c19bf

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
- review oracle の finding merge 用 AgentCallParameter を正本 builder から生成し、正本 prompt に残る `<oracle-root>` placeholder 定義 typo だけを限定補正する薄い adapter。
- 正本側の bug を realization 側で最小補正するための一時的な処理を持ち、known findings の扱いや parameter 本体の構成は正本 builder に委譲する。

## Read this when
- review oracle の merge finding 用 agent call parameter がどこで組み立てられるかを確認したいとき。
- 正本 prompt の placeholder 定義 typo に対する realization 側の補正範囲、削除条件、根拠コメントを確認したいとき。
- known findings を渡した後の prompt 補正が、parameter の他要素を変えずに適用されるかを調べるとき。

## Do not read this when
- review oracle 以外の builder や agent call parameter 全般の構造を調べたいとき。
- 正本 prompt の内容そのもの、または merge finding の正本仕様を確認したいとき。
- placeholder typo 補正ではなく、review finding の解析・統合ロジック本体を調べたいとき。

## hash
- 23e268b53d2c94a31254521af78903039cd5fe98b5c6e9d283463d1fb79810fb

# `validate_finding_advocate.py`

## Summary
- レビュー用 oracle finding 検証の advocate 側 agent call parameter を、oracle src の builder から取得しつつ、既知の静的 typo だけを最小補正する realization 実装。
- 動的入力である finding と既知理由は改変せず、prompt 内の oracle root 表記 typo だけを 1 回置換してから同型の parameter として返す。

## Read this when
- review oracle validate finding advocate 用の agent call parameter 生成経路を確認・変更する。
- oracle src 由来 prompt の静的 typo 補正、またはその補正を削除できる条件を確認する。
- finding や known reasons を byte-for-byte で保持する必要がある処理境界を確認する。

## Do not read this when
- review oracle validate finding advocate 以外の builder や validator を確認したい。
- oracle src 側の正本 prompt 内容そのものを確認・変更したい。
- INDEX.md 用エントリー生成、path model、または一般的な oracle file 定義を確認したい。

## hash
- d416fda47a6fb6bed4efab0f376caa38e172459d6fe7531296bf4962ea8135f6

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

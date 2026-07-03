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
- レビュー用 oracle finding 統合プロンプトを組み立てる公開関数を提供する薄いラッパー。
- 正本側ビルダーの戻り値を保ったまま、正本側の既知の placeholder 表記不具合だけを最小補正する互換処理を担う。
- 補正対象は prompt 内の placeholder 定義ブロックに限定され、既知 finding の内容や他のパラメータは変更しない。

## Read this when
- レビュー用 oracle finding 統合の agent call parameter が、どの正本ビルダーを経由して作られるか確認したいとき。
- prompt 内の oracle root placeholder 表記補正がどこで行われているか調べるとき。
- 正本側の placeholder 表記不具合に対する一時的な realization 側補正や、その削除条件を確認するとき。

## Do not read this when
- レビュー一般の finding 統合仕様や prompt 本文そのものを確認したいだけのときは、対応する oracle 側の定義を直接読む。
- agent call parameter の基本構造や型の責務を確認したいだけのときは、基礎パラメータ定義を読む。
- placeholder 表記補正と無関係なレビュー処理、ファイルアクセス、構造化出力 schema の詳細を調べたいとき。

## hash
- a7e8e1c98ef881912e56cf2367360407162b30eb80ecb5cb21848496405ca3b6

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

# `__init__.py`

## Summary
- oracle.acp_builder.common に対応する互換 builder package の入口を示す。

## Read this when
- acp builder common 領域で oracle 側との互換 package の有無や入口を確認したいとき。
- builder common 配下の import 経路や package 初期化の扱いを確認したいとき。

## Do not read this when
- builder common の具体的な処理内容や個別機能を調べたいときは、下位 module を直接読む。
- oracle 側の正本仕様断片を確認したいときは、対応する oracle file を読む。

## hash
- 39723a6719db306a6db964d9bcc53626a73d1311f463c76d706234e142954b99

# `file_access_rule_vaolation_recovery.py`

## Summary
- ファイルアクセス規則違反のリカバリー用 AgentCallParameter を作る realization 側 wrapper。oracle 側 builder を import 可能にして委譲し、realization 側の型へ変換したうえで、違反 call log 名から得る `<time-stamp>` の値だけを補正する。

## Read this when
- ファイルアクセス規則違反リカバリー用の AgentCallParameter 構築処理を確認・変更したいとき。
- oracle 側 builder の出力を realization 側でどのように適応・補正しているかを確認したいとき。
- 違反 agent call log のファイル名条件や `<time-stamp>` prompt 置換の挙動を調べたいとき。

## Do not read this when
- リカバリー prompt や parameter の正本仕様そのものを確認したいときは、対応する oracle 側 builder を読む。
- oracle src の import 経路解決や AgentCallParameter 変換の共通処理を調べたいときは、共通 helper 側を読む。
- ファイルアクセス規則全体の定義や違反判定ロジックを調べたいだけなら、この wrapper ではなく規則定義や判定処理を読む。

## hash
- af3d885b63f17ae7f53351878e75ea3512867a0dc68160a2484e818a182260db

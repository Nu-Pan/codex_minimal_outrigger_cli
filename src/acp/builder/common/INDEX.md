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
- ファイルアクセス規則違反からの復旧用 AgentCallParameter を、oracle 側の正本 builder に委譲して構築する wrapper。
- oracle src を import 可能にしたうえで正本 builder の戻り値を realization 側の型へ適応する。

## Read this when
- ファイルアクセス規則違反の recovery 用 agent call parameter がどこで構築されるかを確認する。
- oracle 側 builder への委譲と、oracle parameter から realization parameter への適応を調べる。
- ファイルアクセス規則違反リカバリーの prompt/model/reasoning/file access mode の由来を追う入口を探す。

## Do not read this when
- ファイルアクセス規則そのものの定義や違反判定ロジックを調べる場合。
- AgentCallParameter や FileAccessMode の基本構造を調べる場合。
- oracle 側の正本 builder が生成する具体的な prompt 内容を確認したい場合。

## hash
- 3265b75d5761607a988bea17e0471066619386d48a29e199d188a364b9986da9

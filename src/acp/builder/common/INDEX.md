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
- ファイルアクセス規則違反からの recovery 用 agent call parameter 生成を、正本側 builder に委譲する互換 wrapper。
- 正本側の import 準備、repo root 解決、oracle parameter から realization 側 parameter への変換を行う入口を提供する。

## Read this when
- ファイルアクセス規則違反 recovery の builder 呼び出し口を確認したいとき。
- 正本側 builder を realization 側の AgentCallParameter として利用する互換層を変更するとき。
- oracle src の builder を import 可能にする処理や、oracle parameter の変換経路を追うとき。

## Do not read this when
- recovery builder の正本仕様断片そのものを確認したいときは、対応する oracle src を読む。
- agent call parameter の変換処理の詳細を確認したいときは、共通 helper 側を読む。
- ファイルアクセス規則違反の検出ロジックやログ収集処理を調べたいだけのとき。

## hash
- 2dc90fa458824bc3adc247982446795609ea1b5f55cc3bd22cd10f1ed0b701a1

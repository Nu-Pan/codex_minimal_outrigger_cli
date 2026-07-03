# `__init__.py`

## Summary
- 既存の acp.builder.common.* import を維持するためだけに存在する互換 package。
- oracle.acp_builder.common 由来の参照経路を realization 側と利用者向け公開面から段階的に外すまでの暫定入口として位置づけられる。

## Read this when
- acp.builder.common.* の既存 import 互換性を確認する。
- この互換 package を削除できる条件を確認する。
- oracle.acp_builder.common と acp.builder.common の参照関係を調べる。

## Do not read this when
- 互換 import 経路ではなく、common 配下の具体的な実装内容を確認したい。
- 新規機能の実装場所や API 詳細を探している。
- realization 側と利用者向け公開面に acp.builder.common.* 参照が残っているかを、呼び出し元から調査したい。

## hash
- 79afa093b284cae71da7d53b057c3b20b9988352691eacf3ce8d5221458c03b4

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

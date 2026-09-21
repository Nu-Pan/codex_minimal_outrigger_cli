# `oracle`

## Summary
- cmoc の正本ソースを集約するディレクトリ。prompt の構築、agent call の起動パラメータ、パス・設定・文書構造モデル、editor handoff、feedback、ACP 処理などを扱う。
- prompt_builder は agent 向け規定と完全 prompt を組み立て、acp_builder は各サブコマンドの実行用パラメータと構造化出力定義を提供する。
- other は共有モデルと補助機能、editor_input_handoff と feedback は入力引き継ぎおよび問題報告関連の正本実装を担う。

## Read this when
- cmoc の prompt、agent call、ACP 実行フロー、パスモデル、設定モデル、または editor handoff・feedback の正本実装を調査・変更するとき。
- 対象となる機能の正本ソースが prompt_builder、acp_builder、other、editor_input_handoff、feedback のどこにあるかを判断するとき。

## Do not read this when
- realization 側の実装やテストの挙動だけを確認したいときは、この oracle ソースではなく src または test 配下を直接読む。
- 特定機能の詳細実装を確認する段階では、このディレクトリ全体ではなく prompt_builder、acp_builder、other、editor_input_handoff、feedback の該当サブディレクトリまたはファイルへ直接進む。

## hash
- 6b58bddd2082da49793ebaedeb853277f586a7c3720df98f84c33dc588845d3d

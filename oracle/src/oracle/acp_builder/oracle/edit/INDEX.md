# `fork`

## Summary
- 現時点で本文ファイルを含まない空のディレクトリです。

## Read this when
- このディレクトリにファイルが追加され、その内容や用途を確認する必要があるとき。

## Do not read this when
- このディレクトリ配下の具体的なファイルを直接確認できる場合。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `launch_tui.py`

## Summary
- `cmoc oracle edit` の対話型 TUI 起動パラメータを構築する関数を定義する。oracle file 編集用の完全 prompt を生成・保存し、固定モデル・推論強度・ファイルアクセス権・作業ディレクトリ・indexing preflight を含む `AgentCallParameter` を返す。関連する prompt 構築、パス解決、構造化文書レンダリング、agent call 基本型の実装を確認する入口となる。

## Read this when
- `cmoc oracle edit` の TUI 起動条件、起動パラメータ、oracle file 編集用 prompt の構築または保存方法を変更・調査するとき。
- oracle 編集 agent call のモデル、推論強度、アクセスモード、作業ディレクトリ、preflight 設定の責務を確認するとき。

## Do not read this when
- oracle 編集用の完全 prompt の共通構築規則だけを確認したい場合は、prompt builder の実装を直接読む。
- agent call の基本型やアクセスモードの定義だけを確認したい場合は、acp builder の基本型定義を直接読む。
- oracle 編集処理の実行本体や TUI UI 自体を調査する場合は、それぞれの実装入口へ直接進む。

## hash
- a1a4b2a680aa8e647859b2c399f5fb6b437f7ce36b17d578ace963f846911714

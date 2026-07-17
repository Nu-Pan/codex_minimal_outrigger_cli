# `oracle`

## Summary
- ACP builder、設定・共通データ構造、プロンプト builder など、cmoc の oracle src を構成する主要な仕様・生成部品への入口。エージェント呼び出し条件、設定や文書モデル、プロンプトへ注入する標準・規則を扱う。

## Read this when
- ACP builder の oracle 正本仕様や、呼び出しパラメータ・prompt・Structured Output schema・実行設定を調査するとき。
- cmoc の設定モデル、パス解決、規範データ、StructDoc、Markdown 文書生成の仕様を確認するとき。
- oracle / realization の定義、各種 standard、レビュー・ファイルアクセス・ルーティング規則を確認するとき。

## Do not read this when
- realization code の実装・テスト、CLI の実行フロー、表示、永続化、実際のファイル編集処理だけを調査するとき。
- 個別の Enum、StructDoc、標準文書、Requirement など、下位対象の定義そのものだけを確認したいとき。
- oracle file の配置・命名といった上位方針や、対象本文の具体的な INDEX.md 要約だけを確認するとき。

## hash
- 2e2ead4621cf467e901bc0d50a24d92dd1aa36831f5b7c36afccafac8649da84

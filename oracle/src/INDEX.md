# `oracle`

## Summary
- cmoc の oracle 実装における共通モデル、設定・パス解決、agent 向け標準、構造化 Markdown 文書生成を扱う下位モジュールへの入口。prompt 構築や feedback など agent call 定義とは異なり、oracle 側の共通定義と文書表現を調査・変更するときに利用する。

## Read this when
- cmoc の oracle 共通モデル、設定、パスコンテキスト、標準定義、または構造化文書生成の実装を調査・変更するとき
- 複数の oracle 関連モジュールにまたがる責務の入口を確認し、該当する下位要素へ進むとき

## Do not read this when
- agent call の prompt、Structured Output、起動条件、実行権限の定義を調査するときは agent call 定義側を直接読む
- 特定の CLI サブコマンド、feedback、realization、session、TUI の業務ロジックを調査するときは各機能の直接の実装を読む
- 生成済み prompt の構成や prompt 部品の組み合わせを調査するときは prompt builder を直接読む

## hash
- dd231d0be5a5fff968def169cd82066b1aa67bd81366c859ffd169908c2eca29

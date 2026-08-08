# `oracle`

## Summary
- cmoc の各種 Agent call フローで使う正本ソースをまとめた領域。共通パラメータ、用途別 prompt・起動設定、Structured Output schema、feedback や prompt 構築などの下位要素への入口を提供する。

## Read this when
- 特定フローの Agent call に関する prompt、モデル・推論設定、権限、作業ディレクトリ、実行前設定を調査・変更するとき。
- Agent call の出力契約や Structured Output schema、共通パラメータ、feedback、prompt 構築の入口を確認するとき。

## Do not read this when
- 通常の realization 実装・テスト、CLI／TUI の実行フローを調査するとき。
- 正本仕様、Codex CLI の一般的な sandbox・permission 規則、共通 prompt 構築の詳細だけを調査するときは、各専用仕様・実装を直接読む。
- 特定用途の prompt や schema だけを調査するときは、対応する下位ディレクトリを直接読む。

## hash
- 0b81261eb28eadd75e82e12ee30ece9fbb40199cc40ddc9bba6355b962852f7f

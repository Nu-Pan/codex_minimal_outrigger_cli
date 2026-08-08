# `oracle`

## Summary
- cmoc の AI Agent 呼び出しを構成する正本ソース群です。Agent Call の論理パラメータ、用途別の呼び出し設定、Structured Output schema、feedback 入力契約、パス・設定・構造化 Markdown の基盤、および完全な prompt 構築を扱います。
- 用途別の Agent call 設定、prompt builder、基礎モデル、feedback 契約へ進むための入口です。

## Read this when
- AI Agent 呼び出しのモデル種別、推論強度、ファイルアクセスモード、作業ディレクトリ、indexing preflight などの共通パラメータを確認するとき。
- oracle review、realization、session、TUI、indexing、feedback など、特定フローの呼び出し設定や Structured Output schema を調査・変更するとき。
- prompt の組み立て、静的・動的 prompt の構成、placeholder、oracle／realization 規則、feedback reporting 規則を確認するとき。
- cmoc の設定モデル、root placeholder と call-scoped path context、Standard や構造化 Markdown の実装を確認するとき。

## Do not read this when
- 通常の CLI／TUI 実行フローや realization 実装・テストの挙動を調査するときは、呼び出し側または realization 側を直接読む。
- oracle の正本仕様や Codex CLI の一般的な sandbox・permission 規則を確認するときは、対応する仕様文書を直接読む。
- 特定用途の prompt 本文や schema の詳細だけを確認したいときは、該当する下位領域へ直接進む。
- feedback の collector による保存・集約・重複判定だけを確認したいときは、collector 側の実装を直接読む。

## hash
- 061877faaad19b1d3830b443981028c5383d67801b0cd2cbce934f5bed7581cc

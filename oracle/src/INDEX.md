# `oracle`

## Summary
- cmoc の oracle 実装を構成する領域です。agent call パラメータ、feedback 入力契約、設定・パス・構造化文書の共通モデル、完全 prompt の構築を扱います。各責務の調査・変更時に、対応する下位ディレクトリへ進むための入口です.

## Read this when
- oracle 関連の agent call 構築、prompt 構成、Structured Output、ファイルアクセス制御、作業ディレクトリ、indexing preflight を調査・変更するとき
- feedback reporter の入力契約や、問題の構造化・検証を調査・変更するとき
- cmoc 設定、root placeholder とパス解決、agent call の path context、構造化 Markdown 文書を調査・変更するとき
- 完全 prompt、editor 入力文面、oracle・realization・feedback・routing などの policy の構成を調査・変更するとき

## Do not read this when
- oracle の実行制御や CLI の通常フローを調査するときは、呼び出し側の実装を直接読む
- 個別の oracle file の正本仕様や、realization の実装・仕様を確認するときは、対象の oracle または realization 要素を直接読む
- feedback の collector 側の保存・集約・重複判定だけを確認するときは、collector の実装を直接読む
- Codex CLI 共通の実行仕様やモデル解決仕様だけを確認するときは、対応する実装または oracle 文書を直接読む

## hash
- 46d402b708a8be8227ee68bc0b6a2517a6eb34c49f77ca4e0fb29fdd4b3251a9

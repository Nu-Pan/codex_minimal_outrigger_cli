# `oracle`

## Summary
- cmoc の oracle src を構成する主要な正本仕様断片への入口。ACP builder、設定・パス・規範・Markdown 処理、agent 用 prompt builder などを扱う下位要素に分かれる。

## Read this when
- agent 呼び出し条件、設定・パス解決、規範データ、Markdown 文書処理、oracle／realization の標準や routing 規則を調査・変更するとき。
- 対象領域に対応する oracle src の下位要素を選び、個別の正本仕様断片へ進む必要があるとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、通常の実行フロー、realization code の実装・テスト詳細だけを調査するとき。
- 対象となる個別の下位要素が既に特定できており、その本文だけを確認すればよいとき。

## hash
- dfa22d2647f55a03aa17e40bb509ced2db5f2f9febdc4b7d946a44ed13c54d07

# `doc`

## Summary
- cmoc の正本ドキュメント群への入口。アプリケーション仕様、branch・run モデル、開発規則、設計上の代替案など、実装や利用手順の判断根拠となる文書へ振り分ける。

## Read this when
- cmoc の利用者向け挙動や CLI の正本仕様を調査するとき。
- session・run の branch 境界や worktree の扱いを確認するとき。
- Python 開発環境、CLI 設計・配置、テスト規則などの開発手順を確認するとき。
- 採用しなかった設計案と、その不採用理由を確認するとき。

## Do not read this when
- 個別仕様文書の所在が明確で、その本文を直接確認できるとき。
- 個別モジュールの実装詳細や既存テストの内容だけを確認したいとき。
- INDEX.md の構成や生成結果だけを確認したいとき。

## hash
- 5253e15d1477d0d63e5a63f8c5faacfd37aeb45598976a40348688f610e20af1

# `src`

## Summary
- cmoc の oracle src を構成する主要な正本仕様断片への入口。ACP builder、設定・パス解決、規範、Markdown 処理、agent 用 prompt builder などの下位要素を扱う。

## Read this when
- agent 呼び出し条件、設定・パス解決、規範データ、Markdown 文書処理、oracle／realization の標準や routing 規則を調査・変更するとき。
- 対象領域に対応する oracle src の下位要素を選び、個別の正本仕様断片へ進む必要があるとき。

## Do not read this when
- 個別サブコマンドの業務ロジック、通常の実行フロー、realization code の実装・テスト詳細だけを調査するとき。
- 対象となる個別の下位要素が既に特定できており、その本文だけを確認すればよいとき。

## hash
- a8c6f509da48fd3295af4332cd126e6ee29bb854ac5b9af28d84f1541c7bae12

# `doc`

## Summary
- cmoc の正本ドキュメントを機能・開発規則・設計判断ごとに整理したディレクトリ。アプリケーション仕様、branch model、不採用案、Python 開発規則への入口を提供する。

## Read this when
- cmoc の機能仕様、branch・commit・worktree のモデル、Python 開発・CLI 設計・テスト規則を調査・変更・検証するとき
- 対象の詳細仕様や開発ルール文書を特定し、責務境界や関連文書への入口を確認するとき
- 採用されなかった realization refactor の方式や判断理由を確認するとき

## Do not read this when
- 確認したい特定の機能仕様、開発環境手順、テスト手順、CLI 設計、コーディング規則が既に分かっているときは該当文書を直接読む
- 実装構造やテストコードの内容を確認するときは対応する realization code・realization test を直接読む
- INDEX.md の自動生成規則や oracle の一般原則だけを確認するときは、それぞれの専用仕様を直接読む

## hash
- be3d734e9af5847b21ec2ae967fc9311915ebe9076d661faba0d9743e6ed9499

# `src`

## Summary
- oracle の正本実装群を格納するディレクトリです。Agent Call Parameter、各種 prompt、Structured Output schema、パス・設定・構造化文書の共通処理を定義し、下位ディレクトリから indexing、oracle 操作、realization 操作、session、TUI の用途別実装へ進みます。

## Read this when
- cmoc の agent call パラメータ、prompt、Structured Output schema、oracle・realization の扱い、または TUI・session 起動の正本実装を調査・変更するとき。
- 用途別の ACP builder、共通 prompt builder、パスモデル、設定、構造化文書処理の入口を選ぶ必要があるとき。

## Do not read this when
- 実際の CLI 実装や差分適用、競合解消、git 操作など、oracle の正本実装を呼び出す realization 側の処理を調査するとき。
- 特定の用途が明確で、indexing、oracle、realization、session、TUI、prompt builder などの下位ディレクトリへ直接進めるとき。
- 個別の prompt 部品、Structured Output フィールド定義、または特定の設定・パスモデルだけを確認するとき。

## hash
- d15c71e92ca4f9aa8e7b78017625c19bfe2b714eb4921a791d18c6503ea78552

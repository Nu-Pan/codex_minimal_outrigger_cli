# `doc`

## Summary
- cmoc のアプリケーション仕様を定める oracle 文書群。自動補完、managed ollama、Codex CLI 呼び出し、ログ、doctor 前処理、プロンプト、run 隔離、session 状態、主要サブコマンド、割り込み、利用手順など、個別機能の正本仕様を調査する入口。
- session と run の branch・worktree 境界、fork/join、管理対象の branch 名や commit 名の責務を定める仕様。
- cmoc の設計で採用しなかった代替案と不採用理由を記録した判断メモ群。現行仕様ではなく、orchestration、事後検査、permission profile 連携、AI-generated memory、作業計画レビューなどの設計背景を確認する入口。
- Python 開発、CLI の設計・配置、開発環境、realization test に関する正本ドキュメント群。実装・テストの開発手順を確認する入口。

## Read this when
- cmoc の利用者向け機能、サブコマンド、CLI 前処理、補完、ログ、エラー処理、プロンプト、Codex CLI 呼び出し、run 隔離、session 状態、managed ollama の仕様を調査・実装・レビューするときは、アプリケーション仕様の文書群を読む。
- session の開始・終了、branch や worktree の生成・merge、apply や review などの run の実行領域を確認するときは、branch モデルの仕様を読む。
- 現行仕様や実装ではなく、採用しなかった設計案やその理由、設計上の背景を確認するときは、代替案の判断メモを読む。
- Python のコーディング規則、CLI のエントリーポイントや共有処理の配置、Python/venv・依存関係、pytest や結合テストの方針を確認するときは、開発規則の文書群を読む。

## Do not read this when
- 対象機能やコマンドが明確な場合は、このディレクトリ全体を読むのではなく、該当する個別仕様を直接読む。
- 実装ファイルの具体的なコードや INDEX.md の生成方法だけを確認したい場合は、対応する実装本文または専用の routing 文書を読む。
- cmoc 以外の通常の git 運用や、現在の file access rule・差分検査・permission profile の仕様を確認したい場合は、branch モデルや代替案メモではなく直接の仕様・実装対象を読む。
- 採用済み workflow の操作方法、個別機能の実装・テスト仕様、個別モジュールの実装詳細を確認したい場合は、判断メモや開発規則の文書群ではなく直接の対象を読む。

## hash
- d49b0777d2803a4222b28ef3fc8ec1a79cad7375fcacab274442e4f89ec6ea63

# `src`

## Summary
- cmoc の oracle src を構成する実装群。ACP agent call の設定、oracle review・apply・indexing などの prompt と Structured Output schema、共通 prompt 規範、設定・パス・構造化文書モデルを扱う。各サブディレクトリは個別機能の prompt 実装や共通モデルへの入口となる。

## Read this when
- oracle src 全体の責務分担や、ACP builder・prompt builder・共通モデルの関係を確認するとき。
- oracle review、apply fork、indexing、session join などの agent call 設定や Structured Output schema の実装を調査するとき。
- cmoc 設定、モデル・推論強度、ファイルアクセス、パス解決、構造化文書変換の実装を確認するとき。

## Do not read this when
- 特定の oracle review 操作、prompt 部品、設定モデル、パスモデルの詳細だけを調べるとき。
- CLI サブコマンドの呼び出し経路や永続化処理など、oracle src 外の上位実装を直接確認すべきとき。
- 既存の Structured Output schema や prompt 本文を変更せず、realization 側の実装だけを調査するとき。

## hash
- 8f7ad14c12fa3be8209bdc255974511dd0ac0d8548d0df716d0e46f050c56fec

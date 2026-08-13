# `doc`

## Summary
- cmoc の正本文書を集約するドキュメント領域。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった設計案の検討記録、開発ルールへの入口を提供する。各領域の詳細確認が必要な場合は、対応する下位対象へ進む。

## Read this when
- cmoc の利用者向け挙動や機能間の責務境界を確認するとき
- session・run の分岐、commit、worktree の用語や関係を確認するとき
- realization refactor で不採用となった作業方式や設計案の理由を確認するとき
- Python 実装、CLI 設計、開発環境、テスト要件、テスト実行手順の正本文書を探すとき

## Do not read this when
- 確認対象の仕様本文、開発ルール、検討記録がすでに特定できており、その対象を直接読めばよいとき
- 実装コード、realization file、テスト内容、ログ、実行成果物の詳細を調べるとき
- INDEX.md の生成規則やルーティング情報だけを確認するとき

## hash
- db3b2317d3ce9c74020f6f1d2c764ffefc98c59bace4b5f94fef2a10cbc65c89

# `src`

## Summary
- cmoc の oracle 実装を構成する下位領域への入口。AI agent 呼び出しのパラメータ・用途別起動定義、feedback 入力の検証と正規化、共通設定・パス・構造化文書モデル、prompt の構築と標準定義を扱う。
- agent call のモデル・推論強度・ファイルアクセス・cwd などの起動パラメータや、oracle/realization の調査・編集・レビュー・適用フローを確認するときは acp_builder へ進む。
- feedback の入力検証・正規化や Structured Output 契約を確認するときは feedback へ進む。
- 設定、モデル指定、パスプレースホルダ、構造化文書、標準の共通モデルを確認するときは other へ進む。
- 完全な prompt の組み立て、prompt 部品、agent 向け標準・アクセス規則・ルーティング規則を確認するときは prompt_builder へ進む。

## Read this when
- oracle 実装の担当領域を特定し、acp_builder、feedback、other、prompt_builder のどこから調査または変更を始めるか判断するとき。
- agent call、feedback、共通モデル、prompt 構築の複数領域にまたがる変更や調査で、下位入口を選ぶとき。

## Do not read this when
- 対象となる下位領域や個別ファイルが明確で、そこへ直接進めるとき。
- oracle の正本仕様、realization の実装、または INDEX.md のルーティング規則そのものを確認するとき。

## hash
- eab64a844e6f21eb6ba0f257e89c743836544ab775cbb7de6c80fbb074e47989

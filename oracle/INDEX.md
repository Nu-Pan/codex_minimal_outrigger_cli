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
- AIエージェント呼び出しの共通パラメータ、モデル・推論強度・ファイルアクセス、および呼び出し単位のパスコンテキストを定義する実装領域。
- 用途別の agent call 構築、完全な prompt の組み立て、oracle・realization・review・feedback・indexing・session・TUI・quota probe の起動定義を扱う。
- 設定モデル、構造化文書、prompt 規範、パス placeholder、feedback 入力契約など、agent call 構築を支える共通部品への入口となる。

## Read this when
- AIエージェント呼び出しの共通契約や、用途別の起動パラメータ・prompt 構築を調査または変更するとき。
- oracle、realization、review、feedback、indexing、session、TUI、quota probe の agent call 定義へ進む必要があるとき。
- prompt の共通規範、パスコンテキスト、設定、構造化文書、feedback reporter の入力契約を確認するとき。

## Do not read this when
- 通常のサブコマンド実行処理や、構築済み agent call の実行実装だけを確認するとき。
- 個別の agent call 定義や prompt 部品の具体的な挙動を調査するときは、対応する下位対象を直接読む。
- Structured Output の項目・型・形式だけを確認するときは、対応する schema を直接読む。
- バックエンド固有のモデル解決や一般的なファイルアクセス処理だけを確認するときは、それぞれの直接の実装へ進む。

## hash
- 73a45966355df1ce464780fa6087688f28c7f23a7afa332b5522393565a4b7d5

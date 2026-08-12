# `doc`

## Summary
- cmoc の正本仕様を分類して読むための入口。アプリケーション共通仕様、branch・commit・worktree のモデル、開発・テスト規則、および採用しなかった設計案の記録を扱う。個別の挙動や判断根拠を確認する場合は、該当する下位文書へ進む。

## Read this when
- cmoc の仕様・設計・開発規則のどの文書を読むべきか判断するとき
- CLI の共通挙動、Codex 呼び出し、ログ、feedback、session/run、通知、サブコマンド契約の仕様入口を探すとき
- branch・commit・worktree の関係や session/run の分岐モデルを確認するとき
- Python 実装、CLI 設計、開発環境、テスト要件、テスト実行手順の正本を探すとき
- 採用しなかった作業方式や状態管理方式の理由を確認するとき

## Do not read this when
- 確認したい仕様本文や開発規則が既に特定できており、対応する下位文書へ直接進めるとき
- 実装ファイル、テストファイル、実行ログ、生成成果物の具体的内容を調査するとき
- 現行仕様ではなく、特定の不採用案の詳細だけを確認したい場合を除き、検討記録を読む必要がないとき

## hash
- 43e12eec3e84ad5002cd26b117106f5644d6feb48d2ff0440e651714fb0076a1

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

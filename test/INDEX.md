# `test_basic_and_cli.py`

## Summary
- cmoc の realization test として、path model、設定既定値、エラー描画、CLI preflight、初期化、session/apply/review/indexing サブコマンド、Codex CLI 呼び出しラッパーの外部挙動と状態遷移を広く検証する統合寄りのテスト群。
- 一時 Git リポジトリと fake Codex CLI、monkeypatch を使い、ブランチ・worktree・状態 JSON・レポート・ログ・標準出力・終了コード・設定同期・quota 再開制御など、利用者から見える副作用と制御ロジックを確認する。
- 同階層の単体的な補助テストではなく、主要 CLI コマンドと runtime 結合部の回帰確認へ入る入口になる。

## Read this when
- CLI サブコマンドの終了コード、標準出力、エラーレポート、preflight、completion probe、init の副作用を変更・確認するとき。
- session fork/join/abandon、apply fork/join/abandon、review oracle、indexing のブランチ・worktree・状態ファイル・レポート生成・cleanup の挙動を調べるとき。
- Codex CLI 呼び出しの stdin 渡し、profile/config 生成、structured output schema、ログ出力、認証環境検証、quota polling/resume、並列呼び出し制御を変更・検証するとき。
- INDEX.md 生成処理や indexing preflight が Codex 呼び出し前に走る条件、または特定目的で skip される条件を確認するとき。
- 実装変更に対して、主要な外部挙動を既存テストがどう固定しているかを把握したいとき。

## Do not read this when
- oracle file の正本仕様そのものや、人間が管理する仕様断片の内容を確認したいとき。
- 個別 helper の詳細実装だけを追えば足り、CLI 経由の外部挙動・Git 副作用・状態遷移を確認する必要がないとき。
- テスト対象の production code の責務や実装構造を直接調べたいときは、対応する realization implementation を先に読む。
- INDEX.md エントリー生成規則やルーティング文書の書式だけを確認したいとき。

## hash
- 496b2c093d75298dcf8b46d9cccf4b97717a8bc8a858977125865bf24d123b4a

# `test_prompt_parts.py`

## Summary
- プロンプト部品ビルダーと TUI 実行パラメータ解決用ビルダーのテスト群。各標準文書ビルダーが期待する見出し・主要語句を含む構造化文書を返すこと、完全プロンプトが指定フラグに応じて標準文書を含める／省くこと、解決パラメータ用プロンプトと JSON schema が論理 enum や必須項目に一致することを検証する。

## Read this when
- プロンプト部品の出力内容、見出し、主要キーワードを変更した影響を確認したいとき。
- 完全プロンプト生成で routing rule、review standard、realization standard、index entry standard などの標準文書を含める条件を確認したいとき。
- TUI の実行パラメータ解決用ビルダーが埋め込むプロンプト、モデル種別、推論 effort、ファイルアクセスモード、構造化出力 schema の期待値を確認したいとき。
- 標準文書ビルダーやパラメータ解決 schema の変更に合わせて、既存テストの期待語句や enum 整合性チェックを更新する必要があるとき。

## Do not read this when
- プロンプト部品の実装そのものや、標準文書の本文生成ロジックを変更したいだけで、テスト上の期待挙動を確認する必要がないとき。
- CLI コマンド実行、ファイルアクセス制御、パスモデルなど、プロンプト生成以外の挙動を調べたいとき。
- INDEX.md ルーティング文書の生成規則そのものを読む必要があり、テストで検証される断片的な期待語句ではなく仕様本文を確認すべきとき。

## hash
- df383e8e79df703b318954599bbf486e27db7ee9aa5fb8c32b6a8992d1c541ff

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
- プロンプト部品を生成する関数群について、生成結果が構造化文書として返ること、期待する見出しや主要語句を Markdown 出力に含むこと、完全なプロンプトに各標準文書を含めるオプションが正しく効くことを検証する realization test。
- ルーティング規則、実装標準、レビュー標準、索引エントリー標準など、プロンプトに組み込まれる標準文書の存在確認と、既定では任意標準を含めない挙動の確認を担う。

## Read this when
- プロンプト部品生成関数の出力タイトル、構造化文書型、Markdown レンダリング内容に関するテスト期待値を確認したいとき。
- 完全なプロンプト生成で、必須のルーティング規則が常に含まれることや、レビュー標準・実装標準・索引エントリー標準などの任意セクションがフラグで出し分けられることを確認したいとき。
- 標準文書の文言変更やプロンプト構成変更により、どの主要語句がテスト上の互換性境界になっているかを把握したいとき。

## Do not read this when
- 個々の標準文書の本文生成ロジックそのものを変更したいだけで、テスト上の期待語句やプロンプト統合挙動を確認する必要がないとき。
- 構造化文書や Markdown レンダリングの汎用実装を調べたいとき。
- CLI 実行、ファイルアクセス、パスモデル、永続状態など、プロンプト部品以外の挙動を調べたいとき。

## hash
- 9f08832d3a39183e60fae9693de586201d35908abe92564092d1b78fc819b537

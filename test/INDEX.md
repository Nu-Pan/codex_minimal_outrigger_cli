# `test_basic_and_cli.py`

## Summary
- cmoc の基本モデル、CLI サブコマンド、セッション・apply・review・indexing の制御フロー、Codex CLI 呼び出しラッパーを横断的に検証する realization test。
- 一時 Git リポジトリと fake Codex CLI、monkeypatch を使い、外部挙動、状態ファイル、ブランチ・worktree 操作、ログ、エラー出力、設定同期、quota retry などの統合的な期待値を定義する。
- 個別ユニットというより、主要ユーザー操作とランタイム境界の回帰検知入口として位置づけられる。

## Read this when
- path token 変換、設定デフォルト、sandbox mode 変換、構造化エラー表示などの基本挙動を変更する。
- CLI の init、tui、session fork/join/abandon、review oracle、apply fork/join/abandon、indexing の外部出力・副作用・状態遷移を変更する。
- Git ブランチ、worktree、merge conflict、INDEX.md conflict、禁止差分、dirty worktree の扱いに関わる実装を変更する。
- Codex CLI 呼び出しの stdin 渡し、profile 生成、CODEX_HOME/auth.json 検証、ログ出力、schema validation retry、quota polling/resume の挙動を変更する。
- 既存の広い回帰テストにケース追加できるか判断したい。

## Do not read this when
- 特定の小さな helper や純粋関数の詳細だけを確認したい場合で、より局所的なテストが存在する。
- oracle file の正本仕様を確認したい場合。この対象は realization test であり、仕様本文の代替ではない。
- UI 文面や内部実装の整理方針だけを調べたい場合で、CLI 外部挙動、状態遷移、Codex 呼び出し境界に影響しない。
- INDEX.md エントリー生成・描画の形式だけを確認したい場合は、indexing 専用の実装や schema を先に読む方が直接的。

## hash
- b65fa21f05e21d3ead0a9c030dcb37367f2d8edbf239dec644528fbd2262816d

# `test_prompt_parts.py`

## Summary
- プロンプト部品と実行パラメータ生成が、期待する文書タイトル・必須文言・既定の含有/省略条件・Structured Output schema の論理構造を満たすことを検証する realization test。
- レビュー基準、ルーティング規則、ファイルアクセス規則、実現基準、索引エントリー基準、review oracle 基準など、利用者へ渡すプロンプト断片のレンダリング内容を外部挙動として固定する入口になる。
- TUI のパラメータ解決、indexing 用パラメータ、review oracle merge finding 用パラメータについて、モデル種別・reasoning effort・アクセスモード・schema 内容が意図どおり選ばれることも確認する。

## Read this when
- プロンプト断片を生成する builder の戻り値、タイトル、Markdown レンダリング結果、または必須文言を変更する。
- complete prompt が標準類を既定で含むか、フラグ指定時だけ含むかという合成条件を変更する。
- ファイルアクセスモードごとの禁止事項文言や、READONLY / PURE_ORACLE_READ / REALIZATION_WRITE / ORACLE_WRITE / REPO_WRITE の扱いを変更する。
- TUI パラメータ解決、indexing、review oracle merge finding の model class、reasoning effort、file access mode、または schema の required / enum / boolean flag 構造を変更する。
- 索引エントリー生成基準で、何を書くべきか、何を出力に混ぜないか、対象内容を根拠にするかというルールを調整する。

## Do not read this when
- CLI コマンド実行、Git 操作、worktree 操作、ファイルシステム操作など、プロンプト部品の文書レンダリングや実行パラメータ生成と無関係な挙動だけを調べる。
- 個別の oracle 文書そのものの正本仕様を確認したいだけで、生成されたプロンプト断片やそのテスト期待値を確認する必要がない。
- StructDoc や Markdown renderer の汎用的な実装詳細だけを変更し、このテストで固定している具体的なプロンプト文言やパラメータ選定には触れない。
- アプリケーション本体の業務ロジックや UI 表示を調べており、プロンプト合成・標準文書 builder・パラメータ schema の期待値に関係しない。

## hash
- 61760f748d4b30088b5a4fe9fbd6bd65b8e7a2f926559d577ef17c7b7b2375c8

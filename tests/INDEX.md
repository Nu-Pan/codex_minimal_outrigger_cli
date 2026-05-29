# `conftest.py`

## Summary

- pytest 実行時に `<cmoc-root>/src` を Python の import path 先頭へ追加するテスト共通設定ファイルです。
- `tests` 配下のテストから cmoc 本体の `src` 配下モジュールを直接 import できるようにします。
- `Path(__file__).resolve().parents[1] / "src"` で `<cmoc-root>/src` を解決し、`sys.path.insert(0, ...)` で優先的に参照されるよう設定します。

## Read this when

- pytest で `src` 配下の cmoc 実装モジュールを import できる理由を確認したいとき。
- テスト実行時の Python import path 設定や `sys.path` の変更箇所を探しているとき。
- `tests` 配下の共通 pytest 設定が何をしているか把握したいとき。

## Do not read this when

- 個別テストケースの内容や期待値を調べたいとき。
- cmoc の CLI 挙動、サブコマンド仕様、ユーザー向け出力仕様を確認したいとき。
- pytest fixture、mock、Fake Codex CLI などの具体的なテスト補助機能を探しているとき。
- 本番コードの実装ロジックやアプリケーション設定の詳細を調べたいとき。

## hash

- 70811f2ee49ed59eeb60c3c17354146e78b9c21d8ab9bfbcb46007f9d6c8eb57

# `test_codex.py`

## Summary

- `tests/test_codex.py` は `commons.codex.run_codex_exec` を中心に、Codex CLI 呼び出し時のログ生成、通知、Structured Output 検証、再試行、quota 復旧、workspace-write 保護を検証するテスト群です。
- `subcommand_log`、`_extract_session_id`、`_resume_command`、`_write_output_schema` など、Codex 実行に付随する補助関数の境界条件もまとめて確認します。
- Fake Codex CLI と一時 git リポジトリを使い、oracle 変更、commit range、reflog、特殊 path、worktree / submodule まで含む挙動を押さえます。

## Read this when

- `commons.codex.run_codex_exec` の入出力、Structured Output 検証、再試行条件、エラー詳細を変更するとき。
- quota 枯渇時の待機と resume、`_extract_session_id`、`_resume_command`、`subcommand_log` の回帰を確認したいとき。
- workspace-write の oracle 変更検知、`INDEX.md` 保守、特殊 path、linked worktree、submodule の扱いを確認したいとき。
- Codex CLI 呼び出し前後の前処理・後処理・再実行・通知仕様をまとめて追いたいとき。

## Do not read this when

- `commons.repo` の git 共通処理やリポジトリ初期化だけを確認したいとき。
- `commons.timestamps` や `commons.timing` など、Codex 実行と無関係な共通関数を調べたいとき。
- `src/sub_commands` 側の個別サブコマンド実装だけを追いたいとき。
- `INDEX.md` の生成ルールや配置規約だけを確認したいとき。

## hash

- b4aab13faf36d9aa9cfb049eb7e796cb84c1d3898b7b001772234c2c97d4ed01

# `test_file_naming.py`

## Summary

- `tests/test_file_naming.py` はリポジトリ構成のファイル名が命名規則に従うことを検証するテストです。
- 旧ルーティングファイルである `routing.md` と `ROUTING.md` が残存していないことを確認します。
- ルート直下の案内ファイルを増やさず、現行のルーティング入口を `INDEX.md` 群へ統合していることを検証します。

## Read this when

- リポジトリ直下に旧ルーティングファイルが残っていないことを確認したいとき。
- `routing.md` と `ROUTING.md` の不存在をテスト観点から確認したいとき。
- ルーティング入口を `INDEX.md` 群へ一本化する方針の回帰テストを探すとき。

## Do not read this when

- cmoc のサブコマンド仕様や Codex CLI 連携の挙動を確認したいとき。
- Python 実装規約、INDEX.md メンテナンス、git 共通処理など別機能のテストを探しているとき。
- README、AGENTS、oracles、memo などの編集可否やファイルアクセス規則だけを確認したいとき。

## hash

- 8cffbbd037cfef7eddae93b596fc8e14a5e496a69ec1a9cc344e42ba99a22f43

# `test_indexing.py`

## Summary

- `commons.indexing` の `INDEX.md` メンテナンス処理を検証する pytest 集です。
- `gitignore`、除外 root、symlink、バイナリ、非 UTF-8 path、空ディレクトリ、特殊文字、既存 INDEX の再利用と再生成を広く確認します。
- Structured Output の schema 検証、並列化、ロック、自動コミット、既存差分の扱いも確認します。

## Read this when

- `commons.indexing` の対象選別ルールや `INDEX.md` 更新ロジックを変更するとき。
- `INDEX.md` の自動コミット、差分ステージング、ロック制御、並列実行を修正するとき。
- `gitignore`、symlink、非 UTF-8 path、バイナリ判定、特殊ファイルの扱いを確認したいとき。
- `is_maintained_index_path` の配置判定や Structured Output の schema 検証、再生成条件を変えるとき。

## Do not read this when

- `INDEX.md` の配置ルールや目次フォーマットの概要だけを確認したいとき。
- `commons.indexing.py` の実装ロジックそのものを追いたいとき。
- `tests/test_codex.py` や `tests/test_repo.py` など、別のテスト群を確認したいとき。
- `cmoc` のサブコマンド仕様や利用手順だけを確認したいとき。

## hash

- ed654ce75b58b222bebfaf2c5297ffdb91178143546f6afda2de402afbdd7832

# `test_repo.py`

## Summary

- `src/commons/repo.py` の git まわり共通処理を検証するテスト群です。
- repo root 検出、ignore ルール、oracle/implementation ファイル列挙、変更・削除判定、commit 処理を広く扱います。
- session state と apply process id の読み書き、スキーマ検証、active session 判定の異常系も含みます。

## Read this when

- git リポジトリ共通処理のテスト範囲を把握したいとき。
- `.gitignore`、`oracles`、`memo`、`INDEX.md` の列挙・除外ルールを確認したいとき。
- session state、apply process id、cmoc ブランチ判定の期待動作を見たいとき。
- 削除検出、変更抽出、`commit_if_changed` の境界条件を確認したいとき。

## Do not read this when

- git 共通処理の実装ロジックそのものを追いたいとき。
- `src/commons/repo.py` の個別関数仕様を確認したいとき。
- `oracles` や `session state` の正本仕様だけを確認したいとき。

## hash

- da789f11906686e297ed01c7c7bd6d400ecbd4d1743aa4dfc5c3f7452dcca3b8

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は `cmoc` のサブコマンド群に対する決定論的な制御ロジックを検証するテスト入口です。
- `init`、`session`、`apply`、`eval-oracles` を横断して、開始・終了・破棄・統合・評価・レポート生成・状態遷移をまとめて確認します。
- 共通の実行ラッパー、エラー報告、CLI 登録、prompt、Structured Output schema、validation helper まで含めて回帰を守ります。

## Read this when

- `cmoc init`、`session fork/join/abandon`、`apply fork/join/abandon` の状態遷移や副作用を変更したいとき。
- `review oracles` / `eval-oracles` の評価対象選定、レポート生成、改善ループ、payload 検証を確認したいとき。
- `run_command`、`main`、`format_error_report`、CLI 登録や help 文言など共通入口の挙動を確認したいとき。
- prompt 文面、Structured Output schema、`_validate_*` 系ヘルパー、修正点整理や不整合調査の制約を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の一般的な git 共通処理だけを確認したいとき。
- `src/commons/codex.py` の実行詳細や Codex CLI 連携だけを確認したいとき。
- `tests/test_codex.py` や `tests/test_repo.py` など、別のテスト群で足りるとき。
- `INDEX.md` の生成ルールや `oracles` の正本仕様だけを確認したいとき。

## hash

- f00ef03be2320e70ce66062b12844512db6098fbd74e6216b3574435050daa12

# `test_timestamps.py`

## Summary

- `tests/test_timestamps.py` は `commons.timestamps.make_timestamp` と `commons.timing.format_duration` の仕様を確認するテスト群の入口です。
- タイムスタンプはローカルタイムゾーン基準で `YYYY-MM-DD_HH-MM_SS_mmm` 形式に整形されることを検証します。
- `format_duration` の固定幅表示、0.1 秒単位の切り捨て、そして同一ファイル内の補助関数が caller first, callee last で並ぶことを確認します。

## Read this when

- `commons.timestamps.make_timestamp` の出力形式や、aware / naive `datetime` の扱いを確認したいとき。
- `commons.timing.format_duration` の固定幅表示や 0.1 秒単位の切り捨てを確認したいとき。
- タイムスタンプ生成や経過時間表示の変更がこのテスト群に影響するか判断したいとき。
- 同一ファイル内の補助関数の並び順を `inspect.getsourcelines()` で検証している意図を確認したいとき。

## Do not read this when

- `commons.timestamps.make_timestamp` や `commons.timing.format_duration` 以外の CLI サブコマンド仕様を確認したいとき。
- 日時のパース、UTC 固定、その他の日時ユーティリティを探しているとき。
- `INDEX.md` の自動生成や内容ハッシュの管理方法だけを調べたいとき。
- コンソール出力、Codex CLI 呼び出し、エラー処理など別の共通実行制御を確認したいとき。

## hash

- 11dd52f0ae222154a626c7567449aff80b4ca53d28ed40f54116c98cd70908ed

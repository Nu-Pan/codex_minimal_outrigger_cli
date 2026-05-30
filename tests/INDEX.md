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

- `commons.codex` の `run_codex_exec` と関連ヘルパーの回帰テストをまとめたファイルです。
- Structured Output 用 schema の準備、JSON / text 検証、retry、quota 復旧の `resume`、`output_schema` キャッシュ、ログとコンソール出力を検証します。
- workspace-write 時の `INDEX.md` 保守、oracle 変更検知、HEAD / reflog / commit range のチェック、allowlist / conflict 例外、`skip_index_maintenance` も含めて境界条件を押さえます。

## Read this when

- `run_codex_exec` の呼び出し条件、戻り値、例外、再試行の挙動を変更したいとき。
- Structured Output の schema 検証、JSON / text validator、`reasoning_effort` の扱いを修正したいとき。
- codex 呼び出しログ、コンソール通知、`output_schema` のファイル化やキャッシュ再生成の仕様を確認したいとき。
- workspace-write 時の `INDEX.md` 保守、oracle 変更検知、HEAD / reflog / commit range の事前検査や例外判定を確認したいとき。

## Do not read this when

- `cmoc` 全体の利用手順や各サブコマンドの詳細仕様だけを確認したいとき。
- `commons.codex` 以外の共通処理や、`session` / `apply` 本体の実装を追いたいとき。
- `INDEX.md` の生成ルールや `oracles` の正本仕様だけを確認したいとき。

## hash

- 1010f8d654672f9fd867f001701ea94adb3b6703c2b5095ce681a46148739f88

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

- `INDEX.md` メンテナンス処理の pytest 集です。
- 目次エントリ生成、配置対象の判定、ハッシュ更新、既存 `INDEX.md` の再利用や再生成条件を検証します。
- gitignore、除外 root、symlink、binary、非 UTF-8 パス、並列化、ロック、自動コミットまで含む広い回帰テストをまとめています。

## Read this when

- `commons.indexing` の `maintain_indexes` や `is_maintained_index_path` の期待動作を確認したいとき。
- `INDEX.md` の再生成条件、gitignore・symlink・binary・非 UTF-8 パスの扱いを調べたいとき。
- INDEX メンテナンスの並列実行、ロック、自動コミット、再利用の回帰テストを追加・修正したいとき。

## Do not read this when

- `cmoc` の他サブコマンドの引数や実行フローだけを確認したいとき。
- `session` や `apply` の仕様など、INDEX 以外の機能のテストを探しているとき。
- 実装本体ではなく、開発ルールやディレクトリ全体のルーティング方針だけを見たいとき。

## hash

- 58aaebd998e549f93f415de22eedf2596b1bc4878756e0b31fe871f84a66d2c3

# `test_repo.py`

## Summary

- `src/commons/repo.py` の git まわり共通処理を検証するテスト群です。
- repo root 検出、`.cmoc` ignore 保証、oracle / implementation ファイル列挙、変更・削除・rename 判定、`commit_if_changed` を広く扱います。
- session state と apply process id の読み書き、スキーマ検証、active session 判定の異常系も含みます。

## Read this when

- git リポジトリ共通処理のテスト範囲を把握したいとき。
- .gitignore、`oracles`、`memo`、`INDEX.md` の列挙・除外ルールを確認したいとき。
- session state、apply process id、`cmoc` ブランチ判定の期待動作を見たいとき。
- 削除検出、変更抽出、`commit_if_changed` の境界条件を確認したいとき。

## Do not read this when

- `src/commons/repo.py` の実装ロジックそのものを追いたいとき。
- `src/commons/repo.py` の個別関数仕様だけを確認したいとき。
- `oracles` や session state の正本仕様だけを確認したいとき。

## hash

- 7debdb6b6a0420925f7d27b28f9776954f058eec3c91aa7dd6ef03edaf6e1f3f

# `test_report_files.py`

## Summary

- `src/commons/report_files.py` の `write_timestamped_report` が、同名ファイルを上書きせず別名で保存することを検証するテストです。
- タイムスタンプ衝突時の再試行と、既存レポートの内容が保持されることを確認します。
- `make_timestamp` を差し替えて衝突条件を再現し、保存処理の境界を押さえます。

## Read this when

- `write_timestamped_report` の排他的作成や再試行の仕様を変更するとき。
- レポート保存時の上書き防止や、タイムスタンプ衝突時の回帰を確認したいとき。
- `tests/test_report_files.py` が何を守っているかを把握したいとき。

## Do not read this when

- レポート本文の構成や評価結果の意味づけを確認したいとき。
- タイムスタンプ生成そのものの仕様を確認したいとき。
- `INDEX.md` の生成ルールや、他の共通ヘルパーの仕様だけを確認したいとき。

## hash

- 5d46cca82b67cc3fea042c2120193bf0b83020a0f788966ea5aad42d0aa9d587

# `test_subcommands.py`

## Summary

- `tests/test_subcommands.py` は `cmoc` サブコマンド群の決定論的な制御ロジックを横断的に検証するテスト入口です。
- `init`、`session`、`apply`、`review oracles` / `eval-oracles` の状態遷移、branch・worktree・state・report の整合性をまとめて扱います。
- 共通ランナー、エラー報告、CLI 登録、prompt、Structured Output schema、validation helper、レポート生成の回帰も含みます。

## Read this when

- `cmoc init`、`session fork/join/abandon`、`apply fork/join/abandon` の状態遷移や副作用をまとめて確認したいとき。
- `review oracles` / `eval-oracles` の評価フロー、payload 検証、改善処理、レポート出力を確認したいとき。
- `run_command`、`main`、`format_error_report`、CLI 登録、prompt 文言、Structured Output schema、validation helper の変更を確認したいとき。

## Do not read this when

- `src/sub_commands/apply/` や `src/sub_commands/session/` の個別実装だけを追いたいとき。
- `src/commons/codex.py`、`src/commons/repo.py`、`src/commons/report_files.py` など共通処理だけを確認したいとき。
- `tests/test_codex.py`、`tests/test_repo.py`、`tests/test_indexing.py` など、他の個別テストだけで足りるとき。
- `INDEX.md` の生成ルールや `oracles` の正本仕様だけを確認したいとき。

## hash

- bf0f1648cc2ba75e34a84a774d53662cdcdb6344b54003bb530d3c47cd75d0bb

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

# `apply.py`

## Summary

- `cmoc apply fork/join/abandon` の本命処理を実装する realization ファイルです。
- apply loop、finding 列挙・改善・適用、report 生成、apply branch の session branch への merge、想定外差分検査と force-resolve、INDEX.md conflict 自動解決、apply worktree/branch cleanup を扱います。
- `src/main.py` には既存テストや他処理のための compatibility wrapper を残し、このファイルが apply 系 subcommand の実処理を担当します。

## Read this when

- `cmoc apply fork` の apply loop、finding 列挙・改善・適用、commit message 生成、report 生成を確認したいとき。
- `cmoc apply join` の事前条件、想定外差分判定、force-resolve、merge、state 更新、cleanup warning を確認したいとき。
- `cmoc apply abandon` の worktree/branch 破棄、state 初期化、warning 表示を修正したいとき。

## Do not read this when

- session/review/indexing の本命処理だけを確認したいとき。
- Typer の command 登録や Codex CLI prompt builder の文面だけを確認したいとき。
- apply 系 helper の compatibility wrapper だけを `src/main.py` 側で確認したいとき。

## hash

- 600a025e951f9f61cd05e6ccdc05afe51907c243ee4b203e5ef76521cd113635

# `init.py`

## Summary

- `cmoc init` の本命処理を実装する realization ファイルです。
- `.cmoc` の git ignore 保証、config 同期、必要な `.gitignore` 差分の commit、成功時 stdout の Markdown 表示を扱います。
- `src/main.py` の Typer callback から呼び出される `cmoc_init_impl()` の入口です。

## Read this when

- `cmoc init` の副作用、commit 条件、config 同期、stdout 表示を確認したいとき。
- design rule に沿った subcommand implementation の配置を確認したいとき。
- `.cmoc` ignore 保証と config 初期化の境界を修正したいとき。

## Do not read this when

- `cmoc init` 以外の session/apply/review/indexing の実行制御を確認したいとき。
- Typer の command 登録や completion probe の program name 固定だけを確認したいとき。
- `ensure_cmoc_ignored()` や `sync_config()` の内部実装だけを直接確認したいとき。

## hash

- f50ebd2eb96fa024f3634c6b14a5882d4866a2532cf05a13d3b5fe06134d561c

# `indexing.py`

## Summary

- `cmoc indexing` と Codex CLI 呼び出し前 indexing preflight の本命処理を実装する realization ファイルです。
- INDEX.md の配置対象列挙、既存 entry の hash 検査、entry 生成、更新差分の commit、entry Markdown rendering を扱います。
- `src/main.py` には既存テストと preflight 境界のための thin wrapper を残し、このファイルが実処理を担当します。

## Read this when

- `cmoc indexing` の深い directory 優先処理、hash 判定、自動 commit を確認したいとき。
- INDEX.md entry 生成の Codex CLI 呼び出し、並列生成、Structured Output rendering を修正したいとき。
- `update_indexes()`、`build_index_entry()`、`render_index_entry()` の実処理を追いたいとき。

## Do not read this when

- session/apply/review の branch や state 遷移だけを確認したいとき。
- Typer の command 登録や completion probe の program name 固定だけを確認したいとき。
- prompt builder 自体の文面や schema だけを直接確認したいとき。

## hash

- a4f9705b93a50e6ce0a719f324ce891ba8149574d1c806f1494123659bb6c23e

# `session.py`

## Summary

- `cmoc session fork/join/abandon` の本命処理を実装する realization ファイルです。
- session branch の作成、session state 更新、session home branch への merge、merge conflict 解消依頼、session abandon の cleanup を扱います。
- `src/main.py` の Typer callback から呼び出され、Codex CLI 呼び出しと git runner は main 側から注入できます。

## Read this when

- `cmoc session fork` の branch/state 作成や active session 制約を確認したいとき。
- `cmoc session join` の merge、conflict resolution agent call、branch 削除 warning を確認したいとき。
- `cmoc session abandon` の事前条件、home branch 切り替え、state 更新、branch 削除を修正したいとき。

## Do not read this when

- `apply`、`review oracle`、`indexing` の本命処理だけを確認したいとき。
- Typer の command 登録や completion probe の program name 固定だけを確認したいとき。
- session state dataclass や git helper の内部実装だけを直接確認したいとき。

## hash

- 1ac7da085f1c6dab065f696400c7fce368e566dccb93384559fce067eaca0cb1

# `review.py`

## Summary

- `cmoc review oracle` の本命処理を実装する realization ファイルです。
- review worktree/branch の作成、oracle file 対象列挙、finding enumerate/merge/validate/judge loop、review INDEX.md 変更の merge、Markdown report 生成を扱います。
- `src/main.py` には既存テストや他処理のための compatibility wrapper を残し、このファイルが review oracle の実処理を担当します。

## Read this when

- `cmoc review oracle` の事前条件、scope、run isolation、review loop、report frontmatter を確認したいとき。
- review branch 上の INDEX.md 差分 commit/merge や conflict 解消を修正したいとき。
- `run_review_oracle_loop()`、`render_review_oracle_report()`、finding merge operation の実処理を追いたいとき。

## Do not read this when

- init/session/apply/indexing の本命処理だけを確認したいとき。
- Typer の command 登録や completion probe の program name 固定だけを確認したいとき。
- review oracle 用 prompt builder の文面や schema だけを直接確認したいとき。

## hash

- 764ded2bfb5029ee6e4e562dc675abe45a11a4f36591f0e50e2d56ece73da8d8

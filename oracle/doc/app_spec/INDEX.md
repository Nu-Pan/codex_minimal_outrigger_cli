# `cli_auto_completion.md`

## Summary

- `_CMOC_COMPLETE` 指定時の CLI 自動補完の扱いを定めた文書です。
- 通常の `cmoc` 実行とは切り分け、事前検査やエラーレポートを行わず Click/Typer の補完処理へ委譲する前提を示します。

## Read this when

- `_CMOC_COMPLETE` が付いた呼び出しを、自動補完用プローブとしてどう扱うか確認したいとき。
- 補完モードで cmoc 独自の前処理や副作用をスキップし、そのまま Click/Typer に委譲する条件を確認したいとき。
- 補完モードの stdout/stderr に混ぜてよい出力を制限したいとき。

## Do not read this when

- 通常の `cmoc` 実行時の引数処理や `init`・`session`・`apply` などの通常フローを確認したいとき。
- `<repo-root>` 探索、状態検査、エラーレポート、ログ作成など、cmoc 独自の事前処理仕様を確認したいとき。
- Click/Typer 以外の補完実装や、一般的なシェル補完の設計方針を確認したいとき。

## hash

- 480051b6d39bcaaf30039ef43ae1a8853e51bcadc27cd83c7c39a44cf76ef3c4

# `codex_call.md`

## Summary

- `cmoc` から `codex exec` を呼び出すための共通規約をまとめた文書です。
- stdin でプロンプト本文を渡す方法、プロンプトの構成要件、アクセス制限の書き方、モデル指定と出力方法を扱います。
- 失敗時の扱いとして、quota 不足時の待機・再開、サーバー一時不調時のリトライ方針まで定義しています。

## Read this when

- cmoc から `codex exec` を呼び出す方法や、stdin 経由でのプロンプト送信ルールを実装・修正・レビューしたいとき。
- プロンプトの構成、argv に載せてよい情報の制約、`--output-schema` や `--output-last-message` を含む出力規約を確認したいとき。
- sandbox の read-only / workspace-write の選択基準、Model / Reasoning Effort の指定方針、quota 不足時の待機・再開手順を確認したいとき。

## Do not read this when

- `codex exec` 以外の実行手段や、一般的なシェル呼び出し方針だけを確認したいとき。
- `INDEX.md` の生成・更新ルールや、他の仕様ファイルのルーティングだけを確認したいとき。
- この文書の対象外である、他のサブコマンド固有の手順や状態遷移だけを確認したいとき。

## hash

- 84aa53f4db8749d16c08edc74d212e3dd66868f7dcc414fe779edefd2f1bb7dc

# `console_and_file_log.md`

## Summary

- `cmoc` のサブコマンドにおけるコンソール出力とファイルログ出力の規則をまとめた仕様断片です。
- ログ保存先、必須イベント、記録粒度、コンソール表示の最低要件、時間表示フォーマット、パス表示のルールを案内します。

## Read this when

- サブコマンド呼び出し時のコンソール出力とファイルログ出力の役割分担を確認したいとき。
- <work-root>/.cmoc/logs/sub_commands/<time-stamp>.jsonl への保存規則や、イベント 1 つを 1 行として記録する方針を確認したいとき。
- 各ステップ開始通知、Codex CLI 呼び出し通知、完了サマリーの表示内容や時間表示フォーマットを実装・調整したいとき。

## Do not read this when

- 個別サブコマンドの引数や状態遷移だけを確認したいとき。
- branch モデル、session/apply の手順、エラーハンドリングなど、出力規則以外を確認したいとき。
- `README.md` や `AGENTS.md` など、リポジトリ運用ルールだけを確認したいとき。

## hash

- 52fac9d3dc3d6bc64ff434ab5f9cf85d3e93dadbcc62f2c7762486433e5993f3

# `error_handling.md`

## Summary

- cmoc 全体に適用される一般的なエラーハンドリング規則をまとめた参照先。特別な仕様がない限り、処理を中断し、エラーレポートを stdout に出し、エラー終了ステータスコードを返す。特別な記載がある場合はその指示を優先する。

## Read this when

- 処理を中断してエラーとして扱うべきかを判断したい場合
- エラーレポートとして stdout に何を出すかを確認したい場合
- エラー終了時のステータスコードや、特別な記載がある仕様との優先関係を確認したい場合

## Do not read this when

- 各サブコマンドや個別機能の仕様に、独自のエラー処理が明記されている場合
- 通常の成功系フローや出力仕様だけを確認したい場合
- エラーハンドリング以外の設計規則や実装ルールを調べたい場合

## hash

- bfaceea1701755cbe1f24db75ea9044ad4d4ed7dc98edef844bc94e39c3bbdf8

# `indexing.md`

## Summary

- `cmoc` における `<work-root>` 上の `INDEX.md` の扱いを定めた仕様です。
- `INDEX.md` の配置対象ディレクトリ、目次作成対象、除外条件、記載フォーマットを説明します。
- `INDEX.md` をどう生成・更新し、どの順序で処理し、どの条件で自動コミットするかまで含めた運用仕様です。

## Read this when

- `cmoc` における `<work-root>` 上の `INDEX.md` の配置対象、目次作成対象、フォーマット、メンテナンス手順を確認したいとき。
- `INDEX.md` を自動生成・自動更新する際の Structured Output schema、処理順序、並列実行規則、自動コミット条件を実装・レビューしたいとき。
- `INDEX.md` の記載内容を人間が直接書かない前提で、ルーティング文書の維持仕様を押さえたいとき。

## Do not read this when

- `INDEX.md` の配置ルールや自動更新の実装方針ではなく、個別サブコマンドや別の仕様ファイルだけを確認したいとき。
- `oracle` 全体の読み方や、他のドキュメント階層の入口だけをたどりたいとき。
- `INDEX.md` の生成対象・除外条件・並列化・自動コミット条件そのものを扱う必要がないとき。

## hash

- 266055d0699398866a52c918e9e2ad17fa6eb1c94d4310cf97b607268168576c

# `misc_specs.md`

## Summary

- `cmoc` 全体に共通する雑多な基礎仕様をまとめた文書です。
- 実装ファイルの列挙ルール、`<work-root>` の前提、`cmoc` 実行時のカレントディレクトリ、`<repo-root>/.cmoc` の扱いを定義します。
- タイムスタンプ形式と、`<cmoc-managed-branch>` の意味も含みます。

## Read this when

- `<work-root>` 配下の実装ファイルを機械的に列挙するルールを確認したいとき。
- `<work-root>` の探索方法や、`<work-root>/oracle`、`.gitignore`、`.git`、`INDEX.md` の扱いを確認したいとき。
- `cmoc` 実行時のカレントディレクトリの前提や、`<repo-root>/.cmoc` の追跡対象外ルールを確認したいとき。
- タイムスタンプ形式や、`<cmoc-managed-branch>` 上で何を指すかの定義を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数、手順、状態遷移を確認したいとき。
- `apply`、`review oracle`、`session fork` など特定機能の詳細仕様を確認したいとき。
- リポジトリ固有の実装方針やドメイン知識を確認したいとき。

## hash

- 570240583dd1a527ce2631a1ca3e548873e33542a53e2f2eca539b6253a0b443

# `oracle`

## Summary

- `oracle files` の基本定義と記述標準への入口となる目次です。
- `basics.md` では `oracle files` の条件、役割、Codex CLI による読み書き可否を案内します。
- `.md` では `oracle files` の書き方の原則、用語統一、未定義部分の扱いを案内します。

## Read this when

- `oracle files` の定義、役割、読み書き可否をまとめて確認したいとき。
- `oracle` 配下の正本仕様断片を書く前に、記述標準と人間意図の扱いを確認したいとき。
- `basics.md` と `.md` のどちらを先に読むべきか迷ったとき。

## Do not read this when

- `oracle files` の定義だけを確認したいときは、`basics.md` に直接進めるとき。
- `oracle files` の書き方や原則だけを確認したいときは、`.md` に直接進めるとき。
- `INDEX.md` の生成・更新ルールや、上位階層のルーティングを確認したいとき。

## hash

- 1279debf71273f0c7a4711e91213dc659ad4a8c8ddd852bbe009fb5489e5589f

# `realization`

## Summary

- `realization` 配下の目次で、`basics.md` と `.md` への入口をまとめた文書です。
- `basics.md` では `realization files` の定義と、`realization code` / `implementation` / `test` / `ancillary` の区分を扱います。
- `.md` では `realization files` に適用する編集・設計標準を扱います。

## Read this when

- `realization files` に該当するかどうかを判定したいとき。
- 実装・テスト・補助ファイルのどれに当たるかを切り分けたいとき。
- `.md` を読む前に、`realization` の基本定義と対象範囲を確認したいとき。

## Do not read this when

- `realization files` の定義がすでに分かっていて、`basics.md` または `.md` に直接進みたいとき。
- `realization` 以外のサブコマンド仕様や共通仕様を探しているとき。
- `oracle` 全体の読み方や、他の階層の `INDEX.md` だけを確認したいとき。

## hash

- 8554baa92e2715173c50008cee42dabac901452c0061b76549ec99fd3c55d511

# `run_isolation.md`

## Summary

- cmoc サブコマンドの run を、人間の操作と衝突しないよう git branch と worktree で隔離する規則をまとめた文書です。
- run は `<cmoc-session-branch>` の HEAD を起点に `<cmoc-run-branch>` を作成し、`<cmoc-run-worktree>` 上で実行・記録する前提を示します。
- `<run-root>` 内のみを原則として読み書き可能にしつつ、ログやステートなど明示された例外では `<repo-root>` 配下への書き込みを許す方針を示します。

## Read this when

- cmoc サブコマンドの run を人間の作業と衝突しないように隔離する規則を確認したいとき。
- `<cmoc-session-branch>` を基点に `<cmoc-run-branch>` と `<cmoc-run-worktree>` をどう作るか、どう checkout して作業するかを確認したいとき。
- `<run-root>` 外への書き込み例外として、どのケースで `<repo-root>` 配下への読み書きが許されるかを確認したいとき。
- sub command 実行時の作業環境分離や、ブランチ・worktree の責務分担を実装・修正・レビューしたいとき。

## Do not read this when

- 各サブコマンド固有の引数や処理手順だけを確認したいとき。
- 通常の git branch / worktree の一般論だけを確認したいとき。
- `session` / `apply` など、run 隔離以外のフローや `INDEX.md` 生成ルールを確認したいとき。

## hash

- e3da9e6971aaffa3211df28d9fd840d6aad8ebc7582087745e6f3324e234dcd9

# `session_state.md`

## Summary

- `cmoc` ワークフローで発生する fork/join の状態を、セッションごとの JSON ファイルとして永続化するための仕様です。
- `session` と `apply` の 2 つの領域に分けて状態を保持し、初期値と `ready` 遷移時の初期化方針を定めています。
- 保存先は `<repo-root>/.cmoc/sessions/<session-id>.json` です。

## Read this when

- `cmoc` の fork/join に伴うセッション状態をどこにどう永続化するか確認したいとき。
- `<repo-root>/.cmoc/sessions/<session-id>.json` に保存する状態項目や初期値、遷移条件を確認したいとき。
- `session` と `apply` の状態管理を実装・レビューするときに、保持すべき情報を整理したいとき。

## Do not read this when

- `cmoc session` や `cmoc apply` の操作手順そのものだけを確認したいとき。
- `oracle` 全体のルーティング方針や `INDEX.md` の生成ルールだけを確認したいとき。
- このファイルの保存先や永続化スキーマではなく、実装コードやテストコードだけで足りるとき。

## hash

- 20f190b37350878524db1e9e118719639fde9dd568a7e2ffe0951ccafeb6e818

# `sub_commands`

## Summary

- `cmoc` の個別サブコマンド仕様をまとめた入口で、`apply` 系、`session` 系、`review oracle`、`init`、`indexing` へ案内するディレクトリです。
- この配下には `apply_abandon.md`、`apply_fork.md`、`apply_join.md`、`session_abandon.md`、`session_fork.md`、`session_join.md`、`review_oracle.md`、`init.md`、`indexing.md` が並びます。
- 用途ごとに読むべき仕様を切り分けるための目次として使います。

## Read this when

- `cmoc` の apply 系・session 系・`review oracle`・`init`・`indexing` のどの仕様を読むべきか迷ったとき。
- 個別サブコマンドの実装、修正、テスト、レビューの前に、該当する仕様断片への入口を確認したいとき。
- `cmoc` のサブコマンド仕様全体を、このディレクトリの目次からたどりたいとき。

## Do not read this when

- 読むべき対象のサブコマンド仕様がすでに分かっていて、`apply_abandon.md`、`apply_fork.md`、`apply_join.md`、`session_abandon.md`、`session_fork.md`、`session_join.md`、`review_oracle.md`、`init.md`、`indexing.md` のいずれかへ直接進めるとき。
- `docs/` や `oracle/` の上位目次、あるいは別階層のルーティング文書だけを確認したいとき。
- 個別サブコマンドの引数や状態遷移ではなく、`INDEX.md` の生成・更新ルールそのものを確認したいとき。

## hash

- 81d1137ecec3ad6fee25beb91eb4667d76b76c6720623c5a8515265e86f79bc9

# `usage.md`

## Summary

- `cmoc` の利用方法と、ユーザーが日常的にたどる基本ワークフローをまとめた入口です。
- `cmoc init` を最初に一度だけ実行する前提、`session fork` でのセッション開始、`review oracle` と `apply` 系コマンドを交えた反復作業の流れを示します。
- `apply fork` 実行中の `oracle` 変更はその実行には反映されず、別周回になる点など、運用上の重要な前提を説明します。

## Read this when

- エンドユーザーが `cmoc` をどう呼び出すか、`PATH` 設定を含めて確認したいとき。
- `cmoc init` を最初に一度だけ実行する前提と、その後の基本ワークフローを把握したいとき。
- `session fork` から `review oracle`、`apply fork`、`apply join`、`session join` までの流れと、`oracle` の変更がどの時点で反映されるかを確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や内部手順など、`cmoc init`・`session fork`・`review oracle`・`apply` 系の正本仕様そのものを確認したいとき。
- `INDEX.md` の生成ルールや、`oracle` 全体のルーティング方針だけを確認したいとき。
- `cmoc` の実装コードやテストコードだけで足りる作業で、この利用方法の入口を参照する必要がないとき。

## hash

- 7f1642bb9cd287e4b9efa5612eebeadf977ea4280447a729e822d466708b6325

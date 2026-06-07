# `branch_model.md`

## Summary

- `cmoc` における session branch と apply branch の役割分担、および通常 branch との関係をまとめた文書です。
- session 開始時に checkout 中の local branch を session home branch として扱い、session branch は `cmoc/session/<session-id>`、apply branch は `cmoc/apply/<session-id>/<apply-run-id>` という命名規則を定めます。
- default branch を特別扱いしないこと、1 つの session home branch に対して active な session branch は高々 1 つであること、apply は開始時点の oracle snapshot commit を基準に進めること、そして apply worktree の配置規則を示します。

## Read this when

- `cmoc session fork` の分岐元や最終的な merge 先をどう扱うか確認したいとき。
- session branch と apply branch の命名規則、用途、ユーザーが編集してよい branch を確認したいとき。
- apply 実行中にどの HEAD を snapshot として固定し、どの変更を取り込まないか、また apply worktree の扱いを確認したいとき。

## Do not read this when

- branch 以外の共通規約や実装ルールを確認したいときは、`dev_rules` や他の仕様文書を読むべきです。
- 個別サブコマンドの引数や手順だけを確認したいときは、該当するサブコマンド仕様を直接参照すべきです。
- `INDEX.md` の生成や更新ルールだけを確認したいときは、この文書ではなく `indexing.md` を読むべきです。

## hash

- c7f96b4e052ffd604c91086c43283b41bd348783f03d5f7b8ef2a1f32da5101b

# `cli_auto_completion.md`

## Summary

- `_CMOC_COMPLETE` 指定時の CLI 自動補完の扱いを定めた文書です。
- 通常の `cmoc` 実行とは切り分け、事前検査やエラーレポートを行わず Click/Typer の補完処理へ委譲する前提を示します。

## Read this when

- `_CMOC_COMPLETE` が付いた呼び出しを、補完用プローブとしてどう扱うか確認したいとき。
- 補完モードで cmoc 独自の前処理をスキップし、そのまま Click/Typer に委譲する条件を確認したいとき。
- 補完モードの stdout/stderr に混ぜてよい出力を制限したいとき。

## Do not read this when

- 通常の `cmoc` コマンド実行時の引数処理や、`init`・`session`・`apply` などの通常フローを確認したいとき。
- `<repo-root>` 探索、状態検査、エラーレポートなど、cmoc 独自の事前検査仕様を確認したいとき。
- Click/Typer 以外の補完実装や、一般的なシェル補完の設計を調べたいとき。

## hash

- 2912e64448aee29837419de534354caf083e50f043db646cd8f15b05fc45b4ac

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

- d1c4b25e255f7114041ef9c3ea420b50aedb3adcf1188674f7b887d0b7fe3051

# `console_and_file_log.md`

## Summary

- サブコマンド呼び出しごとのコンソール出力とファイルログ出力の規則をまとめた文書です。
- ログ保存先、追跡可能性、ステップ開始通知、Codex CLI 呼び出し通知、完了報告の見分け方を扱います。
- 標準出力に流す時間表示フォーマットと、コンソール表示の最低限の項目を定めています。

## Read this when

- サブコマンド実行時の標準出力とログファイルの出し分け、または tee 出力の実装を確認したいとき。
- .cmoc/logs/sub_commands/<time-stamp>.jsonl への保存や、過去の実行を追跡できるログ構造を設計・修正したいとき。
- ステップ開始通知や Codex CLI 呼び出し通知、経過時間表示、完了報告の表示形式を実装・調整したいとき。
- 標準出力に流す時間表示を <hour>h <minute>m <sec>.<msec>s 形式に揃える必要があるとき。

## Do not read this when

- 個別サブコマンドの引数、状態遷移、業務ロジックだけを確認したいときは、この文書ではなく該当するサブコマンド仕様を直接読むべきです。
- branch model や session/apply の手順など、出力規則以外の仕様を確認したいときは、別の正本仕様を読むべきです。
- README や AGENTS などのリポジトリ運用ルールだけを確認したいときは、この文書を読む必要はありません。

## hash

- 7e35c3f6da39d2ad82facfac92b54cfa43609f3e336397ccbf53ae1a9269bf3f

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

- `cmoc` における `<repo-root>` 上の `INDEX.md` の配置対象、目次作成対象、フォーマット、メンテナンス手順を定めた仕様です。
- `INDEX.md` を自動生成・自動更新するための Structured Output schema、処理順序、並列実行規則、自動コミット条件を扱います。
- `INDEX.md` の記載内容を人間が直接書かない前提で、`cmoc` が維持すべきルーティング文書の仕様をまとめています。

## Read this when

- `cmoc` が `<repo-root>` 配下に `INDEX.md` をどう配置・更新するかを確認したいとき。
- `INDEX.md` に載せる目次情報の書式、対象除外条件、ハッシュの扱いを確認したいとき。
- `INDEX.md` メンテナンスの実行タイミング、並列化、差分の自動コミット方針を実装・レビューしたいとき。

## Do not read this when

- `cmoc` の個別サブコマンドの引数や処理手順だけを確認したいとき。
- `cmoc` の日常的な利用フローや `init` / `session` / `apply` の使い方だけを確認したいとき。
- `INDEX.md` の生成・更新・配置ルールではなく、実装コードやテストコードの内容だけを追いたいとき。

## hash

- 4bd126573c8aef0b41c825568c53e4f203f740a8d4683763c006646450ea76d1

# `misc_specs.md`

## Summary

- `cmoc` 全体に共通する雑多な基礎仕様をまとめたファイルです。
- 実装ファイルの列挙ルール、`<repo-root>` 探索とカレントディレクトリ変更、`<repo-root>/.cmoc` の扱いを定義します。
- タイムスタンプ形式と、`<cmoc-managed-branch>` 上で何を指すかの定義も含みます。

## Read this when

- `<repo-root>` 配下の実装ファイルを機械的に列挙するルールを確認したいとき
- `<repo-root>` の探索方法や、`<repo-root>/oracles`・`.gitignore`・`.git`・`INDEX.md` の扱いを確認したいとき
- `<repo-root>` を git 管理リポジトリとしてどう仮定するか、また `cmoc` 実行時のカレントディレクトリの扱いを確認したいとき
- `<repo-root>/.cmoc` の追跡対象外ルールや、タイムスタンプ形式、`<cmoc-managed-branch>` の定義を確認したいとき

## Do not read this when

- `cmoc` の個別サブコマンドの手順や入出力仕様を確認したいとき
- `apply` / `review oracles` / `session fork` など個別機能の詳細仕様を探しているとき
- リポジトリ固有の実装方針やドメイン知識を確認したいとき

## hash

- b57356613036c55ede3a587810317a6f29ebf70b513b08906623426bd92ee474

# `oracles.md`

## Summary

- `oracles ファイル` の定義、役割、自動処理上の扱いをまとめた入口です。
- `<repo-root>/oracles` 配下の非 `INDEX.md` ファイルが対象であり、AI は提案できても編集は人間が行う前提を示します。
- Codex CLI が読み書きしてよい範囲と、workspace-write 後に差分がないことを機械的に検査する規則を確認できます。

## Read this when

- `oracles ファイル` の定義を確認したいとき。
- `oracles ファイル` を人間が所有し、AI が編集しない前提を確認したいとき。
- `oracles` 配下のファイルに対する読み書き可否や自動処理規則を確認したいとき。

## Do not read this when

- `INDEX.md` の作成手順やメンテナンス規則だけを確認したいとき。
- `cmoc` のサブコマンド仕様や実装方針を確認したいとき。
- `oracles` 配下の個別仕様ファイルそのものを編集したいとき。

## hash

- 6ca91e5371d86a6fa925f5b9af6d2d3a2407cb43bd76910f1cb9bdc6cf0d4545

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
- `oracles` 全体のルーティング方針や `INDEX.md` の生成ルールだけを確認したいとき。
- このファイルの保存先や永続化スキーマではなく、実装コードやテストコードだけで足りるとき。

## hash

- 4c11f81874bca682ac3338924ef13c338b5123df38601393eeaff5054c3df260

# `sub_commands`

## Summary

- `apply_abandon.md`、`apply_fork.md`、`apply_join.md`、`init.md`、`review_oracles.md`、`session_abandon.md`、`session_fork.md`、`session_join.md` への入口です。
- `cmoc` の個別サブコマンド仕様を、用途ごとに分岐して辿るための目次ディレクトリです。
- 各ファイルは、個別サブコマンドの手順、前提条件、状態遷移、終了条件をまとめています。

## Read this when

- `apply` 系、`session` 系、`review oracles`、`init` のどの仕様断片を読むべきか迷っているとき。
- 特定のサブコマンドの実装、修正、テスト、レビューに入る前に、入口となる仕様を確認したいとき。
- `apply` / `session` の開始・終了・破棄・統合のどれに関係するかを整理してから個別文書へ進みたいとき。

## Do not read this when

- branch モデル、ログ、エラーハンドリングなどの共通仕様だけを確認したいとき。
- 個別サブコマンドの引数や状態遷移を知りたい場合は、この入口ではなく該当する正本仕様を直接読むべきとき。
- `INDEX.md` の生成・更新ルールや `oracles` 全体のメンテナンス方針だけを確認したいとき。

## hash

- 40bcb4ae7e1867d2cd1b59881147d53446692b6677d3581741f0e7683a3d56ef

# `usage.md`

## Summary

- `cmoc` の利用方法と、ユーザーが日常的にたどる基本ワークフローをまとめた入口です。
- `cmoc init` を最初に一度だけ実行する前提、`session fork` でのセッション開始、`review oracles` と `apply` 系コマンドを交えた反復作業の流れを示します。
- `apply fork` 実行中の `oracles` 変更はその実行には反映されず、別周回になる点など、運用上の重要な前提を説明します。

## Read this when

- エンドユーザーが `cmoc` をどう呼び出すか、`PATH` 設定を含めて確認したいとき。
- `cmoc init` を最初に一度だけ実行する前提や、その後の基本的なワークフローを確認したいとき。
- `session fork` から `review oracles`、`apply fork`、`apply join`、`session join` までの全体の流れと、`oracles` の変更がどの時点で反映されるかを把握したいとき。

## Do not read this when

- 各サブコマンドの引数や内部手順など、個別仕様そのものを確認したいときは、この文書ではなく該当する正本仕様を読むべきです。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいときは、この文書を読む必要はありません。
- `cmoc` の実装コードやテストコードだけで足りる作業では、この文書を参照しなくて構いません。

## hash

- 66d3f08c8efdcd5478e588555add6a5aa7ab3b333cf9322a8582e5babff47f32

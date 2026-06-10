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

- サブコマンドごとのコンソール出力とファイルログ出力の規則を定めた文書です。
- ログ保存先、必須イベント、追跡可能性のための記録粒度、コンソール表示の最低限の項目を扱います。
- 標準出力に流す時間表示フォーマットと、パス表示の基本ルールも定めています。

## Read this when

- サブコマンド呼び出し時のコンソール出力とファイルログ出力の分担を確認したいとき。
- `.cmoc/logs/sub_commands/<time-stamp>.jsonl` への保存規則や、イベント 1 つを 1 行として記録する方針を確認したいとき。
- ステップ開始通知、Codex CLI 呼び出し通知、完了サマリー、時間表示フォーマットを実装・調整したいとき。

## Do not read this when

- 個別サブコマンドの引数や状態遷移だけを確認したいとき。
- branch モデル、session/apply の手順、エラーハンドリングなど、出力規則以外の仕様を確認したいとき。
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
- `oracles` 全体の読み方や、他のドキュメント階層の入口だけをたどりたいとき。
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
- `<work-root>` の探索方法や、`<work-root>/oracles`、`.gitignore`、`.git`、`INDEX.md` の扱いを確認したいとき。
- `cmoc` 実行時のカレントディレクトリの前提や、`<repo-root>/.cmoc` の追跡対象外ルールを確認したいとき。
- タイムスタンプ形式や、`<cmoc-managed-branch>` 上で何を指すかの定義を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数、手順、状態遷移を確認したいとき。
- `apply`、`review oracles`、`session fork` など特定機能の詳細仕様を確認したいとき。
- リポジトリ固有の実装方針やドメイン知識を確認したいとき。

## hash

- 570240583dd1a527ce2631a1ca3e548873e33542a53e2f2eca539b6253a0b443

# `oracles`

## Summary

- `oracles` 配下の基本定義と記述標準への入口です。
- `basic_definitions.md` では `oracles` ファイルの定義・役割・扱いを案内します。
- `writing_standards.md` では `oracles` ファイルの書き方の原則と規則を案内します。

## Read this when

- `oracles` ファイルの基本的な定義、役割、読み書き可否を確認したいとき。
- `oracles` ファイルをどう書くべきか、記述標準や原則を確認したいとき。
- この配下のどの文書から読むべきかを切り分けたいとき。

## Do not read this when

- この配下の個別文書をすでに読む先として決めていて、`basic_definitions.md` か `writing_standards.md` に直接進むとき。
- `oracles` の基本定義や記述標準ではなく、別の仕様階層や別ディレクトリの目次を確認したいとき。
- `INDEX.md` の役割よりも、個別の正本仕様断片そのものだけを確認したいとき。

## hash

- 7710c43a4e92859b7a765fd226f68a4b791288c46c09b82ede374a9a472cd6c1

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
- `oracles` 全体のルーティング方針や `INDEX.md` の生成ルールだけを確認したいとき。
- このファイルの保存先や永続化スキーマではなく、実装コードやテストコードだけで足りるとき。

## hash

- 3239264f00d0b908202b32898ac3f126e33629d36653c5fc0ef8e4d3d8c0f1bf

# `sub_commands`

## Summary

- `cmoc` の個別サブコマンド仕様への入口で、`apply` 系、`session` 系、`review oracles`、`init` を用途別に辿るための目次です。
- `apply_abandon.md`、`apply_fork.md`、`apply_join.md`、`init.md`、`review_oracles.md`、`session_abandon.md`、`session_fork.md`、`session_join.md` へのルーティング情報をまとめます。
- 各ファイルは、個別サブコマンドの手順、前提条件、状態遷移、終了条件を確認するための仕様断片です。

## Read this when

- `apply` 系、`session` 系、`review oracles`、`init` のどの仕様断片へ進むべきか迷うとき。
- 特定のサブコマンドの実装、修正、テスト、レビューの前に入口を確認したいとき。
- `apply` / `session` の開始・終了・破棄・統合を整理してから個別文書へ進みたいとき。

## Do not read this when

- branch モデル、ログ、エラーハンドリングなどの共通仕様だけを確認したいとき。
- 個別サブコマンドの引数や状態遷移を知りたい場合は、ここではなく該当する仕様断片を直接読むとき。
- `INDEX.md` の生成・更新ルールや `oracles` 全体のメンテナンス方針だけを確認したいとき。

## hash

- cadfda72cc80d5f04fc44a22897cfbe933ec7832306b2d0635ddd541fda51279

# `usage.md`

## Summary

- `cmoc` の利用方法と、ユーザーが日常的にたどる基本ワークフローをまとめた入口です。
- `cmoc init` を最初に一度だけ実行する前提、`session fork` でのセッション開始、`review oracles` と `apply` 系コマンドを交えた反復作業の流れを示します。
- `apply fork` 実行中の `oracles` 変更はその実行には反映されず、別周回になる点など、運用上の重要な前提を説明します。

## Read this when

- エンドユーザーが `cmoc` をどう呼び出すか、`PATH` 設定を含めて確認したいとき。
- `cmoc init` を最初に一度だけ実行する前提と、その後の基本ワークフローを把握したいとき。
- `session fork` から `review oracles`、`apply fork`、`apply join`、`session join` までの流れと、`oracles` の変更がどの時点で反映されるかを確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や内部手順など、`cmoc init`・`session fork`・`review oracles`・`apply` 系の正本仕様そのものを確認したいとき。
- `INDEX.md` の生成ルールや、`oracles` 全体のルーティング方針だけを確認したいとき。
- `cmoc` の実装コードやテストコードだけで足りる作業で、この利用方法の入口を参照する必要がないとき。

## hash

- 7f1642bb9cd287e4b9efa5612eebeadf977ea4280447a729e822d466708b6325

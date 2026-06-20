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

# `codex_exec_rule.md`

## Summary

- cmoc から `codex exec` を呼び出すための共通規約をまとめた文書です。
- stdin 経由のプロンプト受け渡し、codex profile の生成、ログ保存、Structured Output、失敗時の再実行方針を扱います。
- Codex CLI 呼び出しに関するファイルアクセス制限と実行条件を定める入口です。

## Read this when

- cmoc から `codex exec` を呼び出す共通規約を確認したいとき。
- stdin でのプロンプト受け渡し、`--profile`、`--json`、`--output-last-message`、Structured Output、失敗時のリトライ方針を確認したいとき。
- ファイルアクセス制限、Model、Reasoning Effort、呼び出しログの保存方針を実装・調整したいとき。

## Do not read this when

- 通常のシェル実行や `codex exec` 以外のコマンド運用だけを確認したいとき。
- `session`、`apply`、`review oracle` など別フローの詳細だけを確認したいとき。
- `INDEX.md` の生成・更新ルールだけを確認したいとき。

## hash

- 15bd5a6d2656d125d02fcd7e174d0a6c1d963fc771abe0b8d53f33243ecbe532

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

- `cmoc` における `<work-root>` 上の `INDEX.md` の扱いを定めた仕様で、`INDEX.md` の配置対象・除外対象・記載フォーマットを説明する。
- `INDEX.md` の生成・更新手順として、深いディレクトリからの処理、差分の検査、必要時の再生成、自動コミットまでを扱う。
- 目次情報の生成は `codex exec` に依頼し、Structured Output で `summary`・`read_this_when`・`do_not_read_this_when` を受け取る前提を示す。
- 目次情報生成の並列実行条件と、インデクシングを cmoc 実行前に直列化して行う運用も含む。

## Read this when

- `<work-root>` 配下の `INDEX.md` の配置対象、目次作成対象、除外条件を確認したいとき。
- `INDEX.md` の生成順序、並列実行、自動コミット条件を実装・レビューしたいとき。
- `codex exec` に目次情報を Structured Output で返させる仕様や、目次情報の JSON schema を確認したいとき。
- `INDEX.md` の人手編集ではなく、自動インデクシングの運用ルールを押さえたいとき。

## Do not read this when

- 通常の `cmoc` 利用手順や、個別サブコマンドの引数・状態遷移だけを確認したいとき。
- `INDEX.md` の配置対象、除外条件、記載フォーマット、並列化、自動コミットなどのルールを扱う必要がないとき。
- 一般的な git commit / branch / worktree の運用だけを確認したいとき。

## hash

- b531b34a7d4cf49e9b285d5b6144632fa8721319bfd553acb9111e54f57a7c0b

# `misc_spec.md`

## Summary

- cmoc 全体に共通する雑多な基礎仕様をまとめた文書です。
- 実装ファイルの列挙ルール、`<work-root>` の前提、cmoc 実行時のカレントディレクトリ、`<repo-root>/.cmoc` の扱いを定義します。
- タイムスタンプ形式と、`<cmoc-managed-branch>` の意味も含みます。

## Read this when

- `<work-root>` 配下の実装ファイルを機械的に列挙するルールを確認したいとき。
- `<work-root>` の探索方法や、`<work-root>/oracle`、`.gitignore`、`.git`、`INDEX.md` の扱いを確認したいとき。
- cmoc 実行時のカレントディレクトリの前提や、`<repo-root>/.cmoc` の追跡対象外ルールを確認したいとき。
- タイムスタンプ形式や、`<cmoc-managed-branch>` 上で何を指すかの定義を確認したいとき。

## Do not read this when

- 個別サブコマンドの引数、手順、状態遷移を確認したいとき。
- `apply`、`review oracle`、`session fork` など特定機能の詳細仕様を確認したいとき。
- リポジトリ固有の実装方針やドメイン知識を確認したいとき。

## hash

- 69c963981887477d4763539bc1d4d802043f5e3795d0dc6c923a41eab08016c7

# `prompt_standard.md`

## Summary

- cmoc が AI エージェントへ渡すプロンプトの標準規則をまとめた文書です。
- cmoc 固有の用語や概念をプロンプトに含めず、ファイル・ディレクトリ・ブランチは具体的なパスへ解決し、エージェントのメタ認知や特定スキルの存在を前提にしない方針を定めています。

## Read this when

- Codex CLI に渡すプロンプトの標準ルールを確認したいとき。
- cmoc 固有の概念をプロンプトへ含めないこと、具体パスへ解決すること、メタ認知や特定スキルの前提を置かないことを整理したいとき。
- プロンプトの自然言語部分を日本語で扱う原則と例外を確認したいとき。

## Do not read this when

- cmoc 全体の利用手順やサブコマンド仕様だけを確認したいとき。
- すでに渡すプロンプトの構成が決まっていて、この標準のルールを参照する必要がないとき。
- プロンプト標準ではなく、個別サブコマンドや別の oracle 文書を確認したいとき。

## hash

- a9131c69d1df568d6c225c66cc279c5e2adc01d56b422581bb1728607ce275bc

# `run_isolation.md`

## Summary

- cmoc サブコマンドの run を、git branch と worktree で人間の操作から隔離する規則をまとめた文書です。
- run は `<cmoc-session-branch>` の HEAD を起点に `<cmoc-run-branch>` を作成し、`<cmoc-run-worktree>` 上で実行・記録します。
- 原則として `<run-root>` 内のみを扱い、明示された例外では `<repo-root>` 配下への読み書きを許します。

## Read this when

- cmoc の run を、人間の操作と衝突しないように隔離する規則を確認したいとき。
- `<cmoc-session-branch>` を起点に `<cmoc-run-branch>` と `<cmoc-run-worktree>` をどう作成し、どう checkout して作業するかを確認したいとき。
- `<run-root>` 外への書き込み例外として、どのケースで `<repo-root>` 配下への読み書きが許されるかを確認したいとき。

## Do not read this when

- 個別サブコマンドの引数や処理手順だけを確認したいとき。
- 通常の git branch / worktree の一般論だけを確認したいとき。
- `session` / `apply` など、run 隔離以外のフローや `INDEX.md` 生成ルールを確認したいとき。

## hash

- 4ce051fea17daf64aa2c0285f4381244608cf0dd073cac8d85e6990a94db17d4

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

- 3e56c02becb452f6181e383b125f3aff1f3010d8158e2ab309df379bead1824b

# `sub_command`

## Summary

- このディレクトリのルーティング文書で、`cmoc` のサブコマンド仕様への入口です。
- `apply` 系、`session` 系、`init`、`indexing`、`review oracle` の個別仕様へ進むための目次として機能します。
- どのサブコマンドの文書を読むべきか迷ったときに、最初に参照する案内です。

## Read this when

- `cmoc apply` 系、`cmoc session` 系、`cmoc init`、`cmoc indexing`、`cmoc review oracle` のうち、どの仕様を先に読むべきか整理したいとき。
- `cmoc apply abandon`、`cmoc apply fork`、`cmoc apply join`、`cmoc session abandon`、`cmoc session fork`、`cmoc session join` の入口をまとめて把握したいとき。
- サブコマンドごとの役割分担や、実装・修正・テスト・レビュー前の読み順を決めたいとき。
- このディレクトリ配下の仕様断片へ進むための入口を確認したいとき。

## Do not read this when

- 読む対象のサブコマンドがすでに分かっていて、この `INDEX.md` を経由せず個別の `*.md` に直接進めるとき。
- この階層の目次だけでなく、個別仕様の本文そのものだけを確認したいとき。
- `oracle` 配下の別ルートや、開発規約・実装規約だけを確認したいとき。

## hash

- f2b986ab492f319ae42ded4922411ae58b5daabcaa7161939e075ff7a970740f

# `usage.md`

## Summary

- `cmoc` の呼び出し方法、初回の `cmoc init`、標準的な作業フローを説明する利用案内です。
- `cmoc session fork` でセッションを開始し、`cmoc apply fork` と `cmoc apply join` を経て、最後に `cmoc session join` で戻る流れをまとめています。
- `apply fork` 時点の `oracle` スナップショットを正本として実装を追従させる、運用上の前提も含みます。

## Read this when

- `cmoc` の基本的な呼び出し方と、利用開始時に最初に何をするか確認したいとき。
- `cmoc session fork` から `cmoc apply fork`、`cmoc apply join`、`cmoc session join` までの標準的な作業ループを把握したいとき。
- 人間が `oracle` を更新しながら、`cmoc` がどの順序で実装追従するのかを全体像として理解したいとき。

## Do not read this when

- `cmoc` の個別サブコマンド仕様をすでに把握していて、`session fork`・`apply fork`・`apply join`・`session join` の各正本仕様へ直接進むとき。
- `cmoc` の導入手順や標準ワークフローではなく、特定のサブコマンド引数や状態遷移だけを確認したいとき。
- `oracle` 配下のルーティング文書ではなく、実装やテストの規約・別階層の目次を探しているとき。

## hash

- 2cef745a630a8dce3041828d8b8004564a124ada78f21dbe0a55d79302081d95

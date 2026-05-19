# `codex_call.md`

## Summary

- `codex_call.md` は、cmoc から Codex CLI を `codex exec` で呼び出す際の実行規約、プロンプト構成、Structured Output、ログ保存、失敗時の扱い、使用言語を定義する仕様断片です。
- Codex CLI 呼び出しでは、必要に応じてサンドボックスモードを読み取り専用にし、`.agents` 配下を直接編集できない制約をプロンプトで緩和する方針を説明しています。
- Codex CLI に渡すプロンプトは、エージェントのロール、作業概要、完了条件、任意の詳細作業内容で構成し、`<cmoc-root>` や `<repo-root>` のような cmoc 固有の抽象表記ではなく具体的なパスを埋め込むことを求めています。
- Structured Output を要求する場合は `codex exec --output-schema <schema.json>` を使い、cmoc 側でも機械的検証を行うこと、また意味的な失敗は最大 3 回リトライすることを定めています。
- `codex exec` のフルログ保存先や、想定外エラー時に即時失敗させる方針、Codex CLI が扱う自然言語部分を原則日本語にする方針も含みます。

## Read this when

- cmoc から Codex CLI を起動する処理や `codex exec` の引数組み立てを実装・変更するとき。
- Codex CLI に渡すプロンプトの構成、禁止表現、具体パスの埋め込み、ファイルシステムアクセス制限指示を確認したいとき。
- 読み取り専用実行や書き込み可能実行で、プロンプトに含めるべき編集禁止・読み書き禁止ルールを判断するとき。
- Structured Output を Codex CLI に要求する実装で、`--output-schema` の使用、cmoc 側検証、パース失敗時のリトライ方針を確認するとき。
- `codex exec` のフルログ保存先や、Codex CLI 呼び出し失敗時のコマンド全体の扱いを確認するとき。
- Codex CLI に渡す入力プロンプト、作業レポート、評価レポート、エラー説明、INDEX.md 目次情報などの自然言語の使用言語を確認するとき。

## Do not read this when

- cmoc のサブコマンドごとのユーザー向け仕様やワークフローだけを調べたいとき。
- Codex CLI 呼び出しと関係しないコンソール出力、共通エラーハンドリング、実行時間表示、終了ステータスだけを確認したいとき。
- cmoc 自体の Python コーディング規約、テスト規約、開発環境、実装ファイル配置を調べたいとき。
- `<cmoc-root>/README.md`、`AGENTS.md`、`oracles`、`memo` などのリポジトリ運用上の編集可否だけを確認したいとき。
- 対象が Codex CLI 連携ではなく、oracle ファイルの列挙、`.cmoc` ディレクトリ管理、タイムスタンプ、INDEX.md 自動更新の詳細仕様に限られるとき。

## hash

- dd8a1da333895c51bfe2808eb00e76afbb28f83ebfafaca44f94bffa5d0bc9fd

# `console_output.md`

## Summary

- cmoc の各サブコマンドが標準出力へ流す進捗表示の正本仕様。
- ステップ名・ステップ数、入れ子ループ時の内側ループ表示、`codex exec` 呼び出し情報、完了時の時間レポートなど、全サブコマンド共通のコンソール出力項目を定義する。
- コンソール出力は詳細ログではなく、実行中であることを利用者が確認できる程度の情報を出す方針を示す。

## Read this when

- サブコマンド実行中に stdout へ表示する進捗メッセージを実装・修正するとき。
- `cmoc apply` などのステップ名、ステップ数、入れ子ループの進捗表示形式を確認したいとき。
- `codex exec` に渡したプロンプト先頭80文字や、実行結果から回収した出力先頭80文字の表示仕様を確認するとき。
- サブコマンド完了時に、ステップ別経過時間とサブコマンド全体の経過時間をレポートする仕様を確認するとき。
- ユーザーに見える標準出力と、詳細ログとして保存・扱う情報の粒度を切り分けたいとき。

## Do not read this when

- 個別サブコマンドの処理内容、引数、終了条件、ワークフロー詳細を調べたいとき。
- 共通エラーハンドリング、異常終了時の stderr や終了ステータスの仕様だけを調べたいとき。
- `codex exec` のプロンプト生成、サンドボックス指定、Structured Output パース、リトライなどの呼び出し内部仕様を調べたいとき。
- 実行ログの保存先、ログファイル形式、`.cmoc` 配下の永続化仕様だけを調べたいとき。
- cmoc 自体の開発ルール、Python 実装規約、テスト方針、ディレクトリ構成だけを確認したいとき。

## hash

- b3616b008e72e2333a2bfb5f5658937a64d0f74d4fe3387b185f5ff94fee610d

# `error_handling.md`

## Summary

- cmoc の仕様で個別指定がない場合の標準エラーハンドリング規則を定義する。
- 処理中断、stdout へのエラーレポート出力、エラー終了を示すステータスコード返却を要求する。
- エラーレポートに含める内容として、簡単な説明、次に取るべきアクション、詳細説明、コールスタックを定める。
- 個別仕様に特別なエラー処理指定がある場合は、その指定を優先することを定める。

## Read this when

- cmoc 全体で共通のエラー終了時の挙動を実装または確認するとき。
- 個別仕様にエラー処理の明記がないケースで、どのように処理を中断し報告するべきか判断するとき。
- エラー時に stdout へ出力するレポート項目や終了ステータスの扱いを設計するとき。
- 例外や想定外状態の扱いについて、個別仕様と共通規則の優先関係を確認するとき。

## Do not read this when

- 特定サブコマンドの正常系フローや入出力仕様だけを調べたいとき。
- 開発環境、コーディング規約、設計規約などアプリケーション実行時エラー以外の開発ルールを調べたいとき。
- 個別仕様に明記された専用のエラー処理だけで判断でき、共通フォールバック規則を確認する必要がないとき。
- README や CLI の利用者向け説明文を更新するための情報だけが必要なとき。

## hash

- bfaceea1701755cbe1f24db75ea9044ad4d4ed7dc98edef844bc94e39c3bbdf8

# `indexing.md`

## Summary

- cmoc が `<repo-root>` 配下に自動配置・自動メンテナンスする `INDEX.md` の仕様を定めるファイル。
- `INDEX.md` の配置対象ディレクトリ、目次作成対象ファイル・ディレクトリ、除外対象、フォーマットを説明している。
- 目次情報の生成を Codex CLI に依頼する手順、Structured Output schema、ハッシュの責任分担、深い階層から処理するメンテナンス順序を定めている。
- Codex CLI 実行前に `INDEX.md` メンテナンスを行うタイミングと、目次生成・merge コンフリクト解決時の例外を説明している。

## Read this when

- `<repo-root>` 配下の `INDEX.md` をどのディレクトリに配置するか実装・確認するとき。
- `INDEX.md` の目次対象から `.gitignore` 対象、ドット始まり、`memo`、`INDEX.md` 自身、バイナリファイルなどを除外する規則を確認したいとき。
- `INDEX.md` の目次情報に含める Summary、Read this when、Do not read this when、hash の形式を実装・検証するとき。
- `INDEX.md` メンテナンス処理で新規作成、欠落目次の追加、存在しない対象の削除、ハッシュ不一致時の再生成、自動コミットを扱うとき。
- Codex CLI に目次情報生成を依頼する Structured Output の schema や、ファイル名・ハッシュなどを cmoc 側で扱う責務分担を確認するとき。
- Codex CLI 実行前に `INDEX.md` メンテナンスを走らせるべきか、または例外として除外すべきか判断するとき。

## Do not read this when

- cmoc 自体の Python コーディング規約、CLI 実装配置、テスト規約など開発者向けルールだけを確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge`、`cmoc eval-oracles` の個別コマンド挙動だけを調べたいとき。
- Codex CLI の一般的な呼び出し方法、サンドボックス指定、プロンプト生成、ログ保存など、`INDEX.md` メンテナンス以外の連携仕様を調べたいとき。
- `<cmoc-root>` 側の `oracles/INDEX.md` ルーティング運用や AGENTS.md のファイルアクセス禁止規則だけを確認したいとき。
- 対象が `<repo-root>` の自動生成 `INDEX.md` ではなく、通常のアプリケーション機能やユーザー向け出力仕様に限られるとき。

## hash

- 15984367fe9fbecd03996ac286f423461d24ce983143582a1b47f2b96f462ee1

# `misc_specs.md`

## Summary

- Defines miscellaneous cmoc application behavior not specific to a single subcommand or workflow.
- Specifies how to mechanically enumerate oracle files under `<repo-root>/oracles`, excluding gitignored files and `INDEX.md`.
- States assumptions about the target `<repo-root>` repository, including git management, fragmented oracle documentation, and repository-local implementation of task-specific knowledge.
- Defines how cmoc discovers and switches to `<repo-root>` by walking upward from the invocation directory to find a directory containing `.git`.
- Specifies that `<repo-root>/.cmoc` is untracked by git and that `cmoc init` guarantees this.
- Defines the timestamp format `<year>-<month>-<day>_<hour>-<minute>_<sec>_<msec>` using zero-padded local time components.

## Read this when

- Implementing or testing oracle-file enumeration behavior.
- Implementing or testing target repository root discovery from the current working directory.
- Working on behavior that depends on cmoc changing its current directory to `<repo-root>` before execution.
- Implementing or testing `.cmoc` directory creation, gitignore handling, or log isolation in target repositories.
- Clarifying what assumptions cmoc may make about repositories it operates on.
- Implementing or testing timestamp generation or parsing for cmoc artifacts.

## Do not read this when

- You only need detailed behavior for a specific cmoc subcommand covered by another app_specs file.
- You are looking for development rules, coding conventions, design rules, or local development environment setup.
- You need cmoc implementation source code rather than canonical specification fragments.
- You need test code organization or test implementation details.
- You are investigating README-facing documentation wording rather than canonical runtime behavior.

## hash

- 8c01e5cb96806de404ea5df9c4fc4fbcef81b6f90cb257ddf666f0c558fa6b73

# `sub_commands`

## Summary

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の各サブコマンド仕様断片を集約するディレクトリです。
- 各サブコマンドの引数、事前条件、実行手順、git 操作、Codex CLI 連携、レポート保存、終了条件など、サブコマンド固有の正本仕様へのルーティングを提供します。
- `init.md` は `<repo-root>` を cmoc で作業可能に初期化し、`<repo-root>/.cmoc` を git 追跡対象外に保証する仕様を扱います。
- `branch.md` は cmoc 作業用ブランチ `<cmoc-branch>` の作成、命名規則、作成元コミット記録を扱います。
- `apply.md` は `<repo-root>` の実装を `<repo-root>/oracles` の正本仕様断片へ追従させる処理、不整合調査・修正ループ、apply レポートを扱います。
- `eval-oracles.md` は `<repo-root>/oracles` の現在スナップショットを部分評価または全体評価し、致命的な問題の有無を人間向けレポートとして保存・提示する仕様を扱います。
- `merge.md` は `<cmoc-branch>` を現在の `HEAD` へマージする処理、マージ元ブランチの自動解決、コンフリクト解決支援、ブランチ削除条件を扱います。

## Read this when

- cmoc の個別サブコマンド仕様のうち、どのファイルを読むべきか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の引数、事前条件、処理順序、終了条件を調べたいとき。
- `<repo-root>/.cmoc` の git 追跡対象外保証が、各サブコマンドでどのタイミングで必要になるか確認したいとき。
- cmoc が作成する `<cmoc-branch>` の命名、作成元コミット記録、マージ元ブランチ自動解決など、作業用ブランチ関連の仕様を探しているとき。
- `cmoc apply` の不整合調査、Structured Output の `discrepancies`、不整合修正ループ、実装変更のコミット、apply レポート保存先を調べたいとき。
- `cmoc eval-oracles` の `--full`、部分評価・全体評価の切り替え、変更済み oracle ファイルの定義、評価レポート形式を調べたいとき。
- `cmoc merge` の precondition、`git merge` コンフリクト時の Codex CLI 依頼範囲、cmoc 側の `git add`・merge commit 作成・ブランチ削除条件を確認したいとき。

## Do not read this when

- Codex CLI 呼び出し表示、stdout 進捗表示、共通エラー処理、タイムスタンプ生成、`<repo-root>` 探索など、サブコマンド横断の共通仕様だけを確認したいとき。
- `INDEX.md` 自動メンテナンス、oracle ファイル列挙、Structured Output による目次生成など、個別サブコマンドに閉じないアプリケーション仕様を調べたいとき。
- cmoc 自体の Python コーディング規約、CLI モジュール配置、共通処理の設計方針、テスト規約、開発環境など、開発者向けルールだけを調べたいとき。
- `<cmoc-root>` の README、AGENTS、oracles、memo などの閲覧・編集可否やリポジトリ運用ルールだけを確認したいとき。
- `<repo-root>/oracles` に書かれる対象プロジェクト固有の正本仕様断片そのものを探しているとき。
- git、Codex CLI、pytest などの一般的な使い方だけを調べており、cmoc の個別サブコマンド仕様が不要なとき。

## hash

- 16329a0f529b7f7d4c6f5c09d60e6434d14c8f3d0beeb7d9a0d5d5276064784e

# `usage.md`

## Summary

- cmoc のエンドユーザー向け利用手順を説明する仕様断片。
- `cmoc` コマンドの呼び出し前提として、`<cmoc-root>/bin` を `PATH` に追加することを示す。
- 初回セットアップとして人間が `cmoc init` を一度実行する流れを定義する。
- 通常利用の想定ワークフローとして、分岐元ブランチでの `cmoc branch`、`<repo-root>/oracles` の記述・評価、`cmoc apply` による実装反映、マージ先ブランチでの `cmoc merge` までの全体手順をまとめる。
- `<repo-root>/oracles` の修正ループでは、`cmoc eval-oracles` による評価レポート確認と、人間による仕様修正を繰り返すことを示す。

## Read this when

- cmoc をエンドユーザーがどの順番で実行するか確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` を使った全体ワークフローを把握したいとき。
- cmoc コマンドを呼び出すために `<cmoc-root>/bin` を `PATH` に追加する前提を確認したいとき。
- `<repo-root>/oracles` を人間が更新し、評価レポートを読みながら仕様を改善する利用フローを確認したいとき。
- cmoc による実装作業を開始してから、最終的にマージ先ブランチへ反映するまでの利用者視点の手順を調べたいとき。

## Do not read this when

- 各サブコマンドの詳細な引数、入出力、エラー処理、内部処理を調べたいとき。
- cmoc 自体の実装方針、Python コーディング規約、テスト規約、開発環境ルールを確認したいとき。
- Codex CLI 呼び出し、Structured Output、サンドボックス、ログ保存などの詳細仕様を調べたいとき。
- `INDEX.md` 自動生成・更新や oracle ファイル列挙など、cmoc の内部的な共通処理仕様を調べたいとき。
- 既に特定のサブコマンド仕様ファイルを読むべきことが分かっており、利用者向けの全体手順が不要なとき。

## hash

- 8b06fc15b6b50983c7695a9aa351c4bbf8df7b262059233fe5f2bc941612e17f

# `codex_call.md`

## Summary

- cmoc から Codex CLI を `codex exec` で呼び出す際の共通規約を定めた仕様断片です。
- プロンプトの構成、`<cmoc-root>` などの cmoc 固有語の禁止、アクセス制限指示の入れ方を扱います。
- Model / Reasoning Effort の選び方、サンドボックスモード、`--json`・`--output-last-message`・`--output-schema` の指定方法を定義します。
- `codex exec` のフルログ保存先、失敗時のリトライ方針、quota 枯渇時の待機・再開方法を扱います。
- cmoc で扱う自然言語は原則日本語とし、`.agents` 配下の編集不可問題への対処方針を含みます。

## Read this when

- cmoc から Codex CLI を呼び出す実装や仕様を確認したいとき。
- Codex CLI に渡すプロンプトの構成、ロール説明、作業内容、完了条件の書き方を確認したいとき。
- `<cmoc-root>` や `<repo-root>` といった抽象語をプロンプトに入れてよいか判断したいとき。
- 読み取り専用実行・書き込み可実行のどちらでサンドボックスを設定すべきか確認したいとき。
- Model / Reasoning Effort の選択基準、Structured Output の使い方、出力 JSON の検証方針を実装したいとき。
- `codex exec` のログ保存、リトライ、quota 待機、再開の挙動を確認したいとき。
- cmoc が出力する説明文やエラーメッセージを日本語に統一すべきか確認したいとき。
- `.agents` 配下を編集しない前提で `codex exec` の指示を組み立てたいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など個別サブコマンドの入出力や手順だけを確認したいとき。
- `INDEX.md` の配置対象、除外対象、目次フォーマットなどのメンテナンス仕様だけを確認したいとき。
- `<repo-root>` の探索、oracle ファイル列挙、実装ファイル列挙、タイムスタンプ形式などの共通補助仕様だけを確認したいとき。
- cmoc 自体の Python 実装規約、設計規約、テスト規約、開発環境ルールを確認したいとき。
- README や AGENTS、`oracles`、`memo` の編集可否や運用ルールだけを確認したいとき。
- Codex CLI の一般的な使い方だけを知りたくて、cmoc 固有の呼び出し規約が不要なとき。

## hash

- 1c410c43fc7b725ee598060d362de335bd6704e7dc69e7d74edb5464f223b75a

# `console_and_file_log.md`

## Summary

- cmoc のサブコマンド呼び出し時に、標準出力とファイルの両方へ出力するログ規則をまとめた仕様断片です。
- サブコマンド呼び出しログと `codex exec` 呼び出しログの役割、記録すべき項目、表示フォーマットを定めています。
- ステップ開始通知、`codex exec` 呼び出し通知、ステップ別経過時間、全体経過時間、待機時間、戻り値の扱いを含みます。
- 標準出力に表示する時間表記の桁幅、スペースパディング、小数 1 桁の切り捨て規則を定義しています。

## Read this when

- サブコマンド実行時に、コンソール表示とログファイル出力をどう分けるか確認したいとき。
- サブコマンド呼び出しログに、どのような進捗通知や経過時間を記録すべきか確認したいとき。
- `codex exec` ごとの詳細ログを markdown と YAML Front Matter で残す仕様を確認したいとき。
- 標準出力に出す時間表示の書式や丸め規則を実装・検証したいとき。
- 過去の `cmoc` 実行をログファイル起点で追跡できるようにしたいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など個別サブコマンドの手順だけを確認したいとき。
- Codex CLI の呼び出し引数、サンドボックス、Structured Output など実行制御の仕様だけを調べたいとき。
- 共通エラーハンドリングや終了ステータスなど、ログ出力以外のエラー仕様を調べたいとき。
- cmoc 自体の Python 実装規約、テスト規約、開発環境ルールを確認したいとき。
- `INDEX.md` の配置対象や自動生成ルールだけを確認したいとき。

## hash

- 0c35d4f364b82c432f78e5f02eadf7d3c64ec7d444905ef6c70af7865cc065b5

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

- cmoc 実行時の横断的な補助仕様をまとめた雑多仕様ファイルです。
- `oracles` ファイル列挙と実装ファイル列挙の対象範囲、除外条件、`INDEX.md` の除外を定義します。
- cmoc が操作対象とする `<repo-root>` の前提条件、`.git` を基準にした `<repo-root>` 探索、実行時カレントディレクトリ変更を定義します。
- `<repo-root>/.cmoc` を git 追跡対象外にする理由と、その保証が `cmoc init` の責務であることを説明します。
- タイムスタンプ `<time-stamp>` のフォーマット、ゼロ埋め、ローカルタイムゾーン使用を定義します。
- `<cmoc-branch>` 上で発生した変更の範囲として、作成元 commit から `HEAD` までの commit、working tree、staging area を含め、削除済みファイル除外や rename 後パス採用を定義します。

## Read this when

- `<repo-root>/oracles` 配下の正本仕様ファイルを機械的に列挙する処理を実装または確認したいとき。
- 実装ファイルの列挙対象と、`oracles`、`.gitignore` 対象、`.git`、`INDEX.md` などの除外規則を確認したいとき。
- cmoc が現在位置からどのように `<repo-root>` を発見し、サブコマンド実行時のカレントディレクトリをどこにするか調べたいとき。
- cmoc が操作対象とする `<repo-root>` にどのような前提を置いているか確認したいとき。
- `<repo-root>/.cmoc` を git 管理外にする仕様や、ログファイルが未コミット差分に混入しないようにする理由を確認したいとき。
- ログ名や一時ファイル名などで使う `<time-stamp>` の具体的な文字列フォーマットを実装したいとき。
- `<cmoc-branch>` 上で変更のあったファイルを判定する処理で、commit 履歴、working tree、staging area、削除、rename の扱いを確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の個別サブコマンド挙動だけを詳しく調べたいとき。
- Codex CLI 呼び出し、プロンプト構成、Structured Output、リトライ、ログ保存などの Codex 連携仕様を調べたいとき。
- `INDEX.md` の自動生成、目次フォーマット、ハッシュ不一致時の再生成など、目次メンテナンス仕様だけを調べたいとき。
- `comconfig.json` や `CMOConfig` の設定項目、補完、過剰パラメータ削除の仕様を確認したいとき。
- cmoc 自体の Python コーディング規約、設計規約、テスト規約、開発環境ルールを調べたいとき。
- README、AGENTS、oracles、memo など、このリポジトリ内ファイルの編集可否やアクセス制限だけを確認したいとき。

## hash

- 0704639401fd1a07d339e28bde82f125c0ac2579b7ba2944ef239c7133cb9d4b

# `sub_commands`

## Summary

- `cmoc` のサブコマンド仕様断片を集約するディレクトリの目次である。
- `cmoc apply` / `branch` / `eval-oracles` / `init` / `merge` の個別仕様への入口をまとめる。
- 各サブコマンドの引数、事前条件、実行手順、終了条件、エラー挙動を参照するための案内を担う。

## Read this when

- 特定の `cmoc` サブコマンド仕様を読み始める前に、どの個別仕様ファイルへ進むべきか判断したいとき。
- `cmoc apply` / `branch` / `eval-oracles` / `init` / `merge` のどれかの実装や確認を始めるとき。
- サブコマンド横断ではなく、個別サブコマンドの詳細仕様へすばやく辿りたいとき。

## Do not read this when

- `cmoc` 全体の実行時共通仕様や `INDEX.md` 自動生成規則だけを調べたいとき。
- `cmoc` の開発ルール、コーディング規約、テスト規約などの開発者向けルールだけを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` などの運用ルールや編集可否だけを確認したいとき。

## hash

- 8c3d0afb68d52d26b6cc921e1c19a6aef06d36042197129821cecb6cf6d32dce

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

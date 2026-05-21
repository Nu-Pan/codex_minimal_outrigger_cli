# `console_output.md`

## Summary

- cmoc の各サブコマンドが標準出力へ流す進捗表示の仕様を定義する文書。
- 全サブコマンド共通で必ず出力するステップ名・ステップ数、入れ子ループの表示、`codex exec` 呼び出し時のプロンプト先頭 80 文字と回収出力先頭 80 文字、完了時の時間レポートを扱う。
- 標準出力に表示する経過時間のフォーマットとして、時・分・秒の桁幅、スペースパディング、小数 1 桁表示と切り捨て規則を定める。

## Read this when

- サブコマンド実行中に stdout へ表示する進捗メッセージの内容や粒度を実装・確認するとき。
- ステップ名、ステップ数、入れ子ループの進捗表示をどのように出すべきか確認したいとき。
- `codex exec` 呼び出し時に、渡したプロンプトや回収した出力をどの範囲までコンソール表示するか調べたいとき。
- サブコマンド完了時に、ステップ別経過時間と全体経過時間を標準出力へ出す処理を実装・検証するとき。
- 経過時間表示を `<hour>h <minute>m <sec>.<msec>s` 形式で整形する際の桁幅、スペースパディング、小数桁の扱いを確認するとき。

## Do not read this when

- 詳細ログの保存先、ログファイル形式、永続化ルールなど、標準出力ではないログ仕様だけを調べたいとき。
- 特定サブコマンドの処理手順、入力、成果物、終了条件など、コンソール表示以外の個別仕様を確認したいとき。
- 共通エラーハンドリング、例外時の stderr 表示、終了ステータスなど、エラー報告仕様だけを調べたいとき。
- Codex CLI 呼び出しの引数、サンドボックス、Structured Output、リトライなど、実行制御の詳細仕様を調べたいとき。
- cmoc 自体の Python 実装規約、テスト規約、ファイル配置など、開発者向けルールだけを確認したいとき。

## hash

- 6b4f937d8b273ed346e887253cec0852ef1adef17a9e3bd8857ab74a00481fad

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

- `oracles/app_specs/sub_commands` は、cmoc の個別サブコマンド仕様へ案内するルーティング用の正本仕様断片ディレクトリです。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の各サブコマンドの引数、事前条件、実行手順、終了条件、レポート出力を扱います。
- `init.md` は `<repo-root>` の初期化と `<repo-root>/.cmoc` の git 追跡対象外保証を定義します。
- `branch.md` は作業用ブランチ `<cmoc-branch>` の作成、命名規則、`<repo-root>/.cmoc/branch/<cmoc-branch>.txt` への記録を定義します。
- `eval_oracles.md` は `<repo-root>/oracles` の致命的問題評価、部分評価・全体評価の切り替え、レポート保存を定義します。
- `apply.md` は `<repo-root>/oracles` と実装の不整合を調査・改善する反復ループ、コミット、作業レポート生成を定義します。
- `merge.md` は `<cmoc-branch>` のマージ、自動解決、コンフリクト処理、ブランチ削除条件を定義します。

## Read this when

- どの個別サブコマンド仕様ファイルを読むべきか判断したいとき。
- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` の仕様を確認したいとき。
- 各サブコマンドの引数、事前条件、実行順序、終了条件を調べたいとき。
- `<repo-root>/.cmoc` の追跡対象外保証が各サブコマンドでどう扱われるか確認したいとき。
- 作業用ブランチ `<cmoc-branch>` の作成や削除の仕様を確認したいとき。
- oracle 評価のレポート保存先や、実装反映の作業レポート仕様を確認したいとき。
- `cmoc apply` の反復調査・修正ループや、`cmoc eval-oracles` の評価モード切り替えを確認したいとき。
- `cmoc merge` のマージ元自動解決やコンフリクト解消の責務分担を確認したいとき。

## Do not read this when

- Codex CLI 呼び出し方法、Structured Output、ログ保存などの共通実行時仕様だけを調べたいとき。
- `<repo-root>` の発見、oracle ファイル列挙、実装ファイル列挙、タイムスタンプなどの共通補助仕様だけを調べたいとき。
- `cmoc` 自体の開発ルール、コーディング規約、テスト規約、開発環境だけを調べたいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` などのリポジトリ運用ルールだけを確認したいとき。
- 個別サブコマンドの仕様がすでに分かっていて、このディレクトリ全体のルーティングが不要なとき。
- 特定の実装不具合やテスト失敗をコード上で直接調査したいだけで、サブコマンド仕様への案内が不要なとき。
- サブコマンド以外のユーザー向け利用手順や開発者向けルールだけを確認したいとき。

## hash

- fdc07d9d3362012901f791a6511d1485b4f00ef60017d0422998b60f8ef73b0e

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

# `codex_call.md`

## Summary

- cmoc から `codex exec` で Codex CLI を呼び出す際の共通規約をまとめた仕様です。
- プロンプトの構成、`<cmoc-root>` や `<repo-root>` のような cmoc 固有語の扱い、アクセス制限指示の入れ方を扱います。
- Model / Reasoning Effort の選び方、サンドボックス、`--json`・`--output-last-message`・`--output-schema` の使い方を定めます。
- `codex exec` のログ保存、リトライ、quota 待機・再開、自然言語の日本語統一方針、`.agents` 配下を編集できない問題への対処を含みます。

## Read this when

- cmoc から Codex CLI を呼び出す実装や仕様を確認したいとき。
- Codex CLI に渡すプロンプトの構成、役割説明、作業内容、完了条件の書き方を確認したいとき。
- `<cmoc-root>` や `<repo-root>` のような抽象語をプロンプトに入れてよいか判断したいとき。
- 読み取り専用実行か書き込み可実行か、どちらのサンドボックスにするべきか確認したいとき。
- Model / Reasoning Effort の選択基準、Structured Output の使い方、出力 JSON の検証方針を実装したいとき。
- `codex exec` のログ保存、リトライ、quota 待機、再開の挙動を確認したいとき。
- cmoc が出力する説明文やエラーメッセージを日本語に統一すべきか確認したいとき。
- `.agents` 配下を編集しない前提で `codex exec` の指示を組み立てたいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など個別サブコマンドの手順だけを確認したいとき。
- `INDEX.md` の配置対象、除外対象、目次フォーマットなどのメンテナンス仕様だけを確認したいとき。
- `<repo-root>` の探索、oracle ファイル列挙、実装ファイル列挙、タイムスタンプ形式などの共通補助仕様だけを確認したいとき。
- cmoc 自体の Python 実装規約、設計規約、テスト規約、開発環境ルールを確認したいとき。
- `README.md`、`AGENTS.md`、`oracles`、`memo` の編集可否や運用ルールだけを確認したいとき。
- Codex CLI の一般的な使い方だけを知りたくて、cmoc 固有の呼び出し規約が不要なとき。

## hash

- 74e99e6b9c41c8b159bbd7ba0db59d376472f7e467874f716fffe7bb8fb740be

# `console_and_file_log.md`

## Summary

- `cmoc` のサブコマンド呼び出し時における、標準出力とログファイルへの出力規則をまとめた仕様です。
- サブコマンド呼び出しログと `codex exec` 呼び出しログの役割、記録すべき項目、表示フォーマットを定めています。
- ステップ開始通知、`codex exec` 呼び出し通知、経過時間、待機時間、戻り値、時間表示フォーマットの規則を扱います。

## Read this when

- サブコマンド実行時のコンソール表示とログファイル出力をどう分けるか確認したいとき。
- サブコマンド呼び出しログに、進捗通知や経過時間をどう記録するか確認したいとき。
- `codex exec` ごとの詳細ログを残す形式や、標準出力の時間表記・丸め規則を実装または検証したいとき。
- 過去の `cmoc` 実行をログファイル起点で追跡できるようにしたいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など個別サブコマンドの手順だけを確認したいとき。
- Codex CLI の呼び出し引数、サンドボックス、Structured Output など実行制御の仕様だけを調べたいとき。
- 共通エラーハンドリングや終了ステータスなど、ログ出力以外のエラー仕様を調べたいとき。
- `INDEX.md` の配置対象や自動生成ルールだけを確認したいとき。

## hash

- 7eb84e1d97b41b7321cd2db126adaa399cd400cfb7cba464c2e161acaed1f7ae

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

- `cmoc` の各サブコマンド仕様ファイルへのルーティング用目次です。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` の個別仕様をまとめています。
- 初期化、作業用ブランチ作成、調査・修正ループ、oracle 評価、マージ解決までの流れを案内します。

## Read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` のどれを読むべきか判断したいとき。
- 作業用ブランチ作成、`oracles` 評価、修正反映、マージ解決の仕様を確認したいとき。
- 各サブコマンドの引数、事前条件、実行手順、終了条件を見分けたいとき。

## Do not read this when

- `cmoc` 自体の開発規約、コーディング規約、テスト規約だけを調べたいとき。
- すでに読みたい個別仕様ファイルが決まっていて、この目次が不要なとき。
- `README.md`、`AGENTS.md`、`oracles` の運用ルールだけを確認したいとき。

## hash

- 4cd75f2e028152469a6d2253db38c34e8129efb18932d7d01e49facb636ab0f2

# `usage.md`

## Summary

- `cmoc` の使い方と、人間が `cmoc` を呼び出すための基本ワークフローをまとめた仕様です。
- `cmoc init` の初回手順と、`cmoc branch`、`cmoc eval-oracles`、`cmoc apply`、`cmoc merge` を使う想定フローを案内します。

## Read this when

- `cmoc` の起動方法や、利用者がどの順番でコマンドを実行すべきか確認したいとき。
- 初回セットアップとして `cmoc init` をいつ呼ぶか知りたいとき。
- `cmoc branch` から `cmoc merge` までの利用手順全体を把握したいとき。

## Do not read this when

- `cmoc` の実装コードやテストコードの配置を探したいとき。
- 個別サブコマンドの詳細な入出力仕様や内部動作だけを知りたいとき。
- `oracles` 配下の正本仕様そのものを編集・確認したいとき。

## hash

- fbdd3943a6658a919f34edab7cfcbdb4de897c47c55479b66e864c2948f8a1b5

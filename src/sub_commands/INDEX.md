# `__init__.py`

## Summary

- `src/sub_commands/__init__.py` は `src.sub_commands` パッケージを宣言するだけの最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src.sub_commands` が Python パッケージとして宣言されていることを確認したいとき。
- `src/sub_commands` ディレクトリの入口として、最小限の役割だけを把握したいとき。
- パッケージとしての存在確認だけで足り、追加の公開 API や実行処理が不要なとき。

## Do not read this when

- `src.sub_commands` 配下の個別サブコマンド実装や実行フローを確認したいとき。
- `apply`、`session`、`init`、`eval_oracles` などの各モジュールの仕様を追いたいとき。
- `src.sub_commands` のパッケージ宣言ではなく、実際の業務ロジックや CLI 入口を見たいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply`

## Summary

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンドのパッケージ入口です。
- この配下には `abandon.py`、`fork.py`、`join.py` と、パッケージ宣言だけを担う `__init__.py` があります。
- 個別の実行フローや状態遷移は各モジュール側で扱います。

## Read this when

- `src/sub_commands/apply` が `cmoc apply` 系サブコマンドのパッケージであることを確認したいとき。
- `cmoc apply abandon` / `cmoc apply fork` / `cmoc apply join` の実装モジュールの入口をまとめて把握したいとき。
- このディレクトリ配下の構成と、どのモジュールにどの処理が置かれているかを素早く確認したいとき。

## Do not read this when

- `cmoc apply` 以外のサブコマンドの仕様や実装を確認したいとき。
- `oracles` 配下の仕様断片だけを読みたいとき。
- `apply` の個別モジュールではなく、共通の branch / state / ログ / エラーハンドリング仕様を確認したいとき。

## hash

- a9051b948efe416051329955f92ffe315b21dcd169558c77c90f885f7de7c08b

# `eval_oracles.py`

## Summary

- `src/sub_commands/eval_oracles.py` は `cmoc review oracles` の本体実装で、`oracles` 配下の仕様断片を Codex CLI で評価し、問題点をまとめた Markdown レポートを生成するモジュールです。
- 現在ブランチと `--full` に応じて部分評価・全体評価を切り替え、評価対象 oracle の列挙、`INDEX.md` の整備、各ファイルへの評価依頼、改善済み issue list の反復、レポート保存までを一括で扱います。
- Structured Output の検証、評価結果の再配分、エラー時のレポート生成、レポートの集計・整形もこのファイルにまとまっています。

## Read this when

- `cmoc review oracles` の処理順や、部分評価・全体評価の切り替え条件を確認したいとき。
- Codex CLI への評価プロンプト生成、Structured Output の検証、問題点リストの改善ロジックを追いたいとき。
- `INDEX.md` の保守を含む `oracles` のスナップショット評価と、`.cmoc/reports/review_oracles` への出力仕様を修正・レビューしたいとき。
- エラー時でもレポートを残す実装や、評価結果の集計・整形を確認したいとき。

## Do not read this when

- `cmoc review oracles` のユーザー向け仕様、前提条件、出力形式だけを確認したいときは、`oracles/app_specs/sub_commands/review_oracles.md` を読むべきです。
- `cmoc` のコマンド登録や `--help` 相当の引数定義だけを確認したいときは、`src/main.py` を読むべきです。
- `apply` や `session` など、`review oracles` 以外のサブコマンド実装を追いたいときは、このファイルではなく該当モジュールを読むべきです。

## hash

- d0f9f0518ad78de50b29da189a9f01bad2f21e9a534684b37918aad4a8767e2e

# `init.py`

## Summary

- `cmoc init` の本体処理を実装している。
- 直接呼び出し時は共通 runner に委譲し、`.cmoc` の ignore 保証と初期化差分の commit を進める。

## Read this when

- `cmoc init` の実際の処理順や、`repo_root` 未指定時に共通 runner へ委譲する流れを確認したいとき。
- `.cmoc` を git 追跡対象外にする保証や、初期化時に発生した差分の commit 処理を実装・修正・レビューしたいとき。
- `src/sub_commands/init.py` の役割と、関連する共通処理の入口を把握したいとき。

## Do not read this when

- `cmoc init` 以外のサブコマンドの処理を見たいとき。
- `.cmoc` の git ignore 追加や tracked ファイル解除、初期化差分の commit が論点に含まれないとき。
- 初期化後の session/apply の運用仕様だけを確認したいとき。

## hash

- 766eb4ef5567a176766be2bb55dbc8f955c55af92c1ddc3f64043c1be4bda4ee

# `session`

## Summary

- `src/sub_commands/session` は `cmoc session` 系サブコマンドのパッケージ入口で、`__init__.py`、`fork.py`、`join.py`、`abandon.py` に各コマンド本体を持つディレクトリです。
- `fork.py` は session branch の作成と session state 記録を担当し、`join.py` は session branch の merge と conflict 解消、`abandon.py` は session branch の破棄を担当します。
- この配下は session の開始・統合・破棄を扱う実装の入口であり、個別の処理詳細は各モジュールへ分かれています。

## Read this when

- `cmoc session` 系サブコマンドの実装入口と、`fork` / `join` / `abandon` の配置を把握したいとき。
- session パッケージ全体の役割や、どのモジュールがどのコマンドを担当しているかを確認したいとき。
- `src/sub_commands/session` 配下の実装・修正・レビュー・テストを始める前に、関連ファイルの入口を整理したいとき。

## Do not read this when

- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` のうち 1 つだけの詳細仕様を確認したいときは、この目次ではなく該当モジュールを直接読むべきです。
- `cmoc apply` 系の開始・終了や破棄の仕様だけを確認したいときは、このディレクトリではなく apply 側の仕様を読むべきです。
- `src/sub_commands/session` のパッケージ宣言だけを確認したいときは `__init__.py` を直接見れば足ります。

## hash

- 22357c5f275509c4fb6d75f2f1f2b9858c33de4bfe2e3778a3552dbccc978c94

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

- `src/sub_commands/apply` は cmoc apply 系サブコマンドの実装入口で、`__init__.py`、`fork.py`、`join.py`、`abandon.py` をまとめるディレクトリです。
- `fork.py` は apply 本体処理を担い、session state の検証、apply branch / worktree の作成、不整合調査・修正ループ、レポート生成までを扱います。
- `join.py` は apply branch の取り込み、想定外差分の検査と強制解決、`INDEX.md` conflict の自動解消を扱い、`abandon.py` は未 join の apply run の破棄を扱います。

## Read this when

- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` の責務分担や処理の流れを把握したいとき。
- `src/sub_commands/apply` 配下の実装モジュールへの入口を探したいとき。
- cmoc apply の実装・修正・レビュー・テストで、どのモジュールを読むべきか判断したいとき。
- apply 系のパッケージ構造として `__init__.py`、`fork.py`、`join.py`、`abandon.py` がどう並んでいるか確認したいとき。

## Do not read this when

- `cmoc apply` の利用手順や仕様断片だけを確認したいときは、`oracles/app_specs/sub_commands/apply_*.md` を直接読むべきです。
- `cmoc session` 系や `review oracles` など、apply 以外のサブコマンドの入口を確認したいときは、このディレクトリではなく該当する入口を読むべきです。
- apply 系の共通ルールや設計方針だけを確認したいときは、`oracles/app_specs/` や `oracles/dev_rules/` 側を先に読むべきです。
- `fork.py`、`join.py`、`abandon.py` のうち特定の 1 つだけを深く追いたいときは、この目次ではなく該当モジュールを直接読むべきです。

## hash

- 0550ef69ca61f3513375790bcc3ab1df4d09e0908194038fe1e69f289825a0fe

# `eval_oracles.py`

## Summary

- `cmoc review oracles` の本体実装で、`oracles` 配下の仕様断片を Codex CLI で評価し、結果をレポート化する処理をまとめたモジュールです。
- 現在ブランチと `--full` から部分評価・全体評価を切り替え、`INDEX.md` の整備、対象 oracle の列挙、各ファイルの評価実行、問題点リストの改善、`.cmoc/reports/review_oracles` への保存までを扱います。
- 評価プロンプトの組み立て、Structured Output の検証、評価結果の集計、成功時とエラー時の Markdown レポート生成を支える補助関数も含みます。

## Read this when

- `cmoc review oracles` の実装・修正・レビューをするとき。
- `--full` の有無とブランチ種別から、部分評価か全体評価かを決めるロジックを確認したいとき。
- Codex CLI に渡す評価プロンプト、Structured Output の schema、入力値検証、評価レポート生成の流れを確認したいとき。

## Do not read this when

- `cmoc review oracles` のユーザー向け仕様や前提条件だけを確認したいとき。
- CLI のコマンド登録や `--help` の定義だけを確認したいとき。
- `cmoc session` や `cmoc apply` など、他サブコマンドの実装だけを確認したいとき。

## hash

- f721661e404efe04bd645b16dce4b5853135d1942b000b6561432c36fc87566c

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

- `src/sub_commands/session` は `cmoc session` 系サブコマンドのパッケージ入口で、`fork.py`、`join.py`、`abandon.py` に各コマンド本体を持ち、`__init__.py` はパッケージ宣言のみを担います。
- このディレクトリは session の開始・統合・破棄を扱う実装の入口であり、個別の処理詳細は各モジュールへ分かれています。

## Read this when

- `cmoc session` 系サブコマンドの実装入口と、`fork` / `join` / `abandon` の配置を把握したいとき。
- session パッケージ全体の役割や、どのモジュールがどのコマンドを担当しているかを確認したいとき。
- `src/sub_commands/session` 配下の実装・修正・レビュー・テストを始める前に、関連ファイルの入口を整理したいとき。

## Do not read this when

- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` のうち 1 つだけの詳細仕様を確認したいときは、この目次ではなく該当モジュールを直接読むべきです。
- `cmoc apply` 系の開始・終了や破棄の仕様だけを確認したいときは、このディレクトリではなく apply 側の仕様を読むべきです。
- `src/sub_commands/session` のパッケージ宣言だけを確認したいときは `__init__.py` を直接見れば足ります。

## hash

- 8b7bcc836b12b151fa9dce31aeb1da89425157c028bb734b90ee5e9814ce73a6

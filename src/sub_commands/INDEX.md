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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンドの実装パッケージで、`__init__.py`、`fork.py`、`join.py`、`abandon.py` をまとめる入口です。
- `fork.py` は apply の本体処理、`join.py` は apply branch の取り込み、`abandon.py` は未 join の apply run の破棄を担当します。
- `__init__.py` はパッケージ宣言だけを担う最小モジュールです。

## Read this when

- `src/sub_commands/apply` 配下の実装モジュールへの入口を探したいとき。
- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` の責務分担や処理の流れを把握したいとき。
- `cmoc apply` の実装・修正・レビュー・テストで、どのモジュールを読むべきか判断したいとき。

## Do not read this when

- `cmoc apply` の利用手順や正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/apply_*.md` を直接読むべきです。
- `cmoc session` 系や `eval-oracles` など、`apply` 以外のサブコマンドを確認したいときは、このディレクトリではなく該当の入口へ進むべきです。
- `apply` 系の共通ルールや設計方針だけを確認したいときは、`oracles/app_specs/` や `oracles/dev_rules/` 側を先に読むべきです。

## hash

- 64a92ef2ddb68ff48e68957087efa6fbd77bba8c70dc94a45ad0ed118740cc04

# `eval_oracles.py`

## Summary

- `cmoc eval-oracles` の本体実装で、`oracles` 配下の仕様断片を Codex CLI で評価し、結果をレポート化する処理をまとめたモジュールです。
- 現在ブランチと `--full` から部分評価 / 全体評価を切り替え、`INDEX.md` の整備、対象 oracle の列挙、各ファイルの評価実行、`.cmoc/reports/eval-oracles` への保存までを扱います。
- 評価プロンプトの組み立て、Structured Output の検証、評価結果の集計、成功時とエラー時の Markdown レポート生成を支える補助関数も含みます。

## Read this when

- `cmoc eval-oracles` の実装・修正・レビューをするときに読むべきです。
- `--full` の有無とブランチ種別から、部分評価か全体評価かを決めるロジックを確認したいときに読むべきです。
- Codex CLI へ渡す評価プロンプト、Structured Output の schema、入力値検証、評価レポート生成の流れを確認したいときに読むべきです。

## Do not read this when

- `cmoc eval-oracles` のユーザー向け仕様や前提条件だけを確認したいときは、`oracles/app_specs/sub_commands/eval_oracles.md` を読むべきです。
- CLI のコマンド登録や `--help` の定義だけを確認したいときは、`src/main.py` を読むべきです。
- `cmoc session` や `cmoc apply` など他サブコマンドの実装だけを確認したいときは、このファイルではなく該当モジュールを読むべきです。

## hash

- 06f103b6f9e05053e16a0c0dd5f1985278eb3489d95a1aca9df5421c86fe7d3d

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

- `src/sub_commands/session` は `cmoc session` 系サブコマンドのパッケージで、`fork.py`、`join.py`、`abandon.py` に各コマンド本体を持ち、`__init__.py` はパッケージ宣言のみを担います。
- このディレクトリは session の開始・統合・破棄を扱う実装の入口であり、個別の処理詳細は各モジュールへ分かれています。

## Read this when

- `cmoc session` 系サブコマンドの実装入口と、`fork` / `join` / `abandon` の配置を把握したいとき。
- session パッケージ全体の役割や、どのモジュールがどのコマンドを担当しているかを確認したいとき。
- `src/sub_commands/session` 配下の実装・修正・レビュー・テストを始める前に、関連ファイルの入口を整理したいとき。

## Do not read this when

- `cmoc apply` 系の開始・終了や、apply branch / worktree の仕様だけを確認したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` のうち 1 つだけの詳細を確認したいときは、該当するモジュールを直接読むべきです。
- `src/sub_commands/session` 配下の Python パッケージ構造ではなく、`oracles/app_specs/sub_commands/` 側の利用手順だけを見たいとき。

## hash

- c613accffa48c967beddcd2fca1e0c073cb56376461bc4e6c68355596831c161

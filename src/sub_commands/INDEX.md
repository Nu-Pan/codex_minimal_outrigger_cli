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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンドの実装をまとめるパッケージで、`fork.py`、`join.py`、`abandon.py`、`__init__.py` への入口になります。
- この配下の `INDEX.md` は、`cmoc apply` の個別実装へたどるための目次として使います。
- `fork` は調査・修正ループ、`join` は完了済み apply の取り込み、`abandon` は未 join の apply の破棄を担当します。

## Read this when

- `src/sub_commands/apply` 配下にある `cmoc apply` 系モジュールの役割分担を確認したいとき。
- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` のどの実装ファイルへ進むべきかを判断したいとき。
- このディレクトリが Python パッケージとしてどう構成されているか、入口を整理したいとき。

## Do not read this when

- `cmoc apply fork`、`join`、`abandon` の個別の実装フローだけを確認したいときは、それぞれのモジュールを直接読むべきです。
- `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/apply_*.md` 側を参照すべきです。
- `cmoc apply` 以外のサブコマンドや共通仕様を確認したいときは、このディレクトリではなく該当する `INDEX.md` を読むべきです。

## hash

- f4fbe1dd85709e4ef6e165f0a6f1b9361df08da663112f5dcb619b435b79bfcb

# `eval_oracles.py`

## Summary

- `cmoc eval-oracles` の本体処理を案内する目次で、oracle ファイルを評価して人間向けレポートを生成する流れをまとめます。
- ブランチが session branch かどうかと `--full` の有無に応じて、部分評価と全体評価を切り替える仕様へたどれます。
- 評価前の `.cmoc` ignore 保証、`INDEX.md` の保守、Structured Output 検証、issue 集約、通常時と失敗時のレポート生成を確認できます。

## Read this when

- `cmoc eval-oracles` の実装・修正・テスト・レビューを行うとき。
- `--full` の有無とブランチ種別による部分評価・全体評価の切り替え条件を確認したいとき。
- `.cmoc` の ignore 保証、`INDEX.md` の保守、oracle ファイルの列挙と選定の流れを確認したいとき。
- Structured Output の検証、fatal / inconclusive / warning の集約、レポート生成とエラー時の出力を確認したいとき。

## Do not read this when

- `cmoc eval-oracles` 以外のサブコマンドの実装や手順だけを確認したいとき。
- oracle 断片そのものの仕様だけを読みたいときで、評価・集約・レポート生成の流れが不要なとき。
- `INDEX.md` の生成・更新ルールだけを確認したいときで、評価ロジック自体は不要なとき。
- レポート本文の細かな文言だけを確認したいときで、ファイル選定や Structured Output の検証は不要なとき。

## hash

- b2cf301036a8bc6a91ee72ebc1e88f8a7c710394a7f0d4c312a3562cc56cb7c9

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

- `src/sub_commands/session` の入口で、`__init__.py` と `fork.py`、`join.py`、`abandon.py` をまとめるディレクトリです。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の実装本体へのルーティング情報を提供します。
- session の開始・完了・破棄の役割分担を整理して、目的の実装へ直接進めるようにします。

## Read this when

- `cmoc session` 系サブコマンドの実装・修正・レビュー・テストを進めたいとき。
- このディレクトリ内の `__init__.py`、`fork.py`、`join.py`、`abandon.py` がそれぞれ何を担当するか確認したいとき。
- session の開始、統合、破棄の処理フローを実装順にたどりたいとき。

## Do not read this when

- `cmoc apply` 系や `eval-oracles` など、session 以外のサブコマンドだけを確認したいとき。
- `cmoc session` の利用手順や正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。
- `src/sub_commands/session` の実装詳細ではなく、CLI 入口や共通処理だけを追いたいときは別のモジュールを読むべきです。

## hash

- 369b57b77ab468cb15d6e0a2a9241e7de1e021092dbbf1bd91f6198d03fbe340

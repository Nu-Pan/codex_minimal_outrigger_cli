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

- `src/sub_commands/apply` 配下の `cmoc apply` 系実装モジュールの入口です。`__init__.py`、`abandon.py`、`fork.py`、`join.py` の役割分担をまとめます。
- `abandon.py` は未 join の apply run の破棄、`fork.py` は調査・修正ループと成果物生成、`join.py` は session branch への取り込みを担います。
- この INDEX から個別モジュールへたどれば、apply 系の処理順、状態遷移、cleanup の責務を素早く確認できます。

## Read this when

- `cmoc apply` 系実装の入口をまとめて把握したいとき。
- `abandon` / `fork` / `join` のどのモジュールを読むべきか整理したいとき。
- apply run の破棄、調査・修正ループ、session branch への取り込みの責務境界を確認したいとき。
- `src/sub_commands/apply` 配下の実装ファイル一覧を、処理の役割と対応づけてたどりたいとき。

## Do not read this when

- 個別の `cmoc apply abandon`、`cmoc apply fork`、`cmoc apply join` の実装だけを確認したいときは、この INDEX ではなく該当モジュールを直接読むべきです。
- `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。
- `src/sub_commands/apply` が Python パッケージとして存在するかだけを確認したいときは、`__init__.py` のみを見れば足ります。

## hash

- d30e3e2c66e0ce0d1bf987b6b34c179794e6e24d945dc5b9f86ac4923aec7857

# `eval_oracles.py`

## Summary

- `cmoc eval-oracles` の本体処理で、oracle ファイル群を選定して Codex CLI で評価し、人間向けレポートを作成します。
- セッションブランチ上では `--full` の有無で部分評価・全体評価を切り替え、それ以外では全体評価として動作します。
- 評価前に `.cmoc` の ignore を保証し、`INDEX.md` を保守したうえで、対象 oracle ごとに Structured Output を検証しながら評価します。
- 評価結果は fatal / inconclusive / warning ごとに集約され、通常レポートと失敗時レポートの両方を生成できるようになっています。

## Read this when

- `cmoc eval-oracles` の実装・修正・テスト・レビューを行うとき。
- 部分評価と全体評価の切り替え条件、`--full` の扱い、対象 oracle ファイルの選び方を確認したいとき。
- `.cmoc` の ignore 保証、`INDEX.md` の保守、`codex exec` による 1 ファイル単位の評価実行を確認したいとき。
- Structured Output の検証、評価結果の集約、レポート生成、エラー時のレポート出力を確認したいとき。

## Do not read this when

- `cmoc eval-oracles` 以外のサブコマンドの実装や挙動だけを確認したいとき。
- oracle 断片そのものの仕様だけを確認したいときで、この処理本体の流れは不要なとき。
- `INDEX.md` の生成・更新ルールだけを確認したいときで、評価処理の実装は不要なとき。
- レポート本文の細かな文言だけを確認したいときで、ファイル選択・評価実行・検証ロジックは不要なとき。

## hash

- 148ae2a414da66167dd7a8ba14a4005643d7a80bc80543f5a50522af5ffc2589

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

- `src/sub_commands/session` 配下の `cmoc session` 系実装モジュールの入口です。
- `__init__.py` はパッケージ宣言のみ、`fork.py` は session 開始、`join.py` は session 完了、`abandon.py` は session 破棄を担います。
- この目次から、各モジュールへ進んで session 系処理の順序、前提条件、状態遷移、cleanup の責務を確認できます。

## Read this when

- `cmoc session` 系実装の入口をまとめて把握したいとき。
- `fork` / `join` / `abandon` のどのモジュールを読むべきか整理したいとき。
- session の開始、完了、破棄の責務境界を確認したいとき。
- `src/sub_commands/session` 配下の実装ファイル一覧を、処理の役割と対応づけてたどりたいとき。

## Do not read this when

- 個別の `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の実装だけを確認したいときは、この INDEX ではなく該当モジュールを直接読むべきです。
- `cmoc session` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。
- `src/sub_commands/session` が Python パッケージとして存在するかだけを確認したいときは、`__init__.py` のみを見れば足ります。
- session 以外のサブコマンドや `cmoc` 全体の入口だけを確認したいときは、このディレクトリの INDEX は適しません。

## hash

- e8c222e289be56f51494770067a5ad86ef85004503e095e4596660a650e6aa7f

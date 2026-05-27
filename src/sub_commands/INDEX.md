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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンドのパッケージ宣言と、個別実装モジュールへの入口をまとめたディレクトリです。
- `__init__.py` は `cmoc apply` 系サブコマンドのパッケージ宣言だけを担います。
- `abandon.py` は `cmoc apply abandon` の本体処理を実装します。
- `fork.py` は `cmoc apply fork` の本体処理を実装します。
- `join.py` は `cmoc apply join` の本体処理を実装します。

## Read this when

- `src/sub_commands/apply` が Python パッケージとしてどう構成されているか確認したいとき。
- `cmoc apply abandon`、`cmoc apply fork`、`cmoc apply join` のどの実装モジュールへ進むべきかを判断したいとき。
- `cmoc apply` 系サブコマンドの入口として、`__init__.py` を含めた構成を整理したいとき。
- `cmoc apply` 配下の個別モジュールの役割分担をひと目で把握したいとき。

## Do not read this when

- `cmoc apply` 以外のサブコマンドの仕様や実装だけを確認したいときは、このディレクトリではなく該当する別ディレクトリを読むべきです。
- `cmoc apply` の仕様断片だけを確認したいときは、`oracles/app_specs/sub_commands/` 側の文書を直接読むべきです。
- `cmoc apply` の共通ルールや利用方法だけを知りたいときは、このディレクトリではなく上位の目次や共通仕様を参照すべきです。

## hash

- 99d43e941458540eae1b699a5db8a0eb3920bbc82f6e0b196cd1a9f9f31c937c

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

- `src/sub_commands/session` は `cmoc session` 系サブコマンドの実装をまとめたパッケージです。
- `__init__.py` はパッケージ宣言を担い、`fork.py`、`join.py`、`abandon.py` がそれぞれ session の開始・統合・破棄処理の本体を実装します。
- このディレクトリを起点に、session の各操作に対応する実装モジュールへ直接たどれます。

## Read this when

- `cmoc session` 系サブコマンドの実装構成をまとめて把握したいとき。
- `session fork`、`session join`、`session abandon` のどの実装モジュールへ進むべきかを判断したいとき。
- このディレクトリが `cmoc session` 系サブコマンドの Python パッケージとしてどう構成されているか確認したいとき。
- session 系の開始・統合・破棄に対応する入口を、`__init__.py` を含めて整理したいとき。

## Do not read this when

- `session fork`、`session join`、`session abandon` のうち 1 つだけの実装や挙動を確認したいときは、このディレクトリ全体ではなく該当する `fork.py`、`join.py`、`abandon.py` を直接読むべきです。
- `cmoc session` 系の仕様断片だけを確認したいときは、`oracles/app_specs/sub_commands/` 側の該当文書を読むべきです。
- パッケージ宣言の有無だけを確認したいときは、`__init__.py` だけを読むだけで足ります。
- `cmoc apply` 系サブコマンドや、`init`、`eval-oracles` など session 以外の実装を確認したいときは、このディレクトリではなく対応する別ディレクトリを読むべきです。

## hash

- 1d2275727371db17e67840652dafc3bd5d257922e8484d2d1211517708131088

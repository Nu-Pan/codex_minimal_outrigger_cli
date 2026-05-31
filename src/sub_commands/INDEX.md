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
- `apply`、`session`、`review`、`init` などの各モジュールの仕様を追いたいとき。
- `src.sub_commands` のパッケージ宣言ではなく、実際の業務ロジックや CLI 入口を見たいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply`

## Summary

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンド実装の入口で、`__init__.py`、`fork.py`、`join.py`、`abandon.py` をまとめています。
- `fork.py` は apply の開始と調査・修正ループ、`join.py` は完了済み apply の session への取り込み、`abandon.py` は未 join の apply 破棄を担当します。
- このディレクトリは、apply 系の実装を読む前に開始・統合・破棄のどれへ進むべきかを切り分けるための目次です。

## Read this when

- `src/sub_commands/apply` 配下の実装ファイルの役割分担を把握したいとき。
- `cmoc apply fork`、`cmoc apply join`、`cmoc apply abandon` のどの実装へ進むべきか整理したいとき。
- apply 系サブコマンドの開始・統合・破棄の流れを、実装ベースで素早く確認したいとき。
- このディレクトリを起点に、必要なモジュールだけを最短で読み分けたいとき。

## Do not read this when

- `src/sub_commands/apply/__init__.py` のパッケージ宣言だけを確認したいとき。
- `cmoc apply fork` の実行ループや調査・修正対象の列挙だけを確認したいとき。
- `cmoc apply join` のマージ条件や `--force-resolve` の扱いだけを確認したいとき。
- `cmoc apply abandon` の破棄条件や cleanup 手順だけを確認したいとき。
- `cmoc session` や `cmoc review oracles` など、apply 以外のサブコマンド仕様を探しているとき。
- `oracles` 側の正本仕様や `INDEX.md` 生成ルールだけを確認したいとき。

## hash

- 7a050d35910cf93eb1e7245948202ee451fe0eb7f614dbb1f4f0068ece0b3221

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

# `review`

## Summary

- `src/sub_commands/review` は `cmoc review` 系サブコマンド実装の入口です。
- `__init__.py` はパッケージ宣言のみを担い、実行ロジックは持ちません。
- `oracles.py` は `cmoc review oracles` の本体実装で、oracle スナップショット評価の入口です。

## Read this when

- `src/sub_commands/review` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc review` 系サブコマンドの入口となるパッケージ構造を把握したいとき。
- `cmoc review oracles` の実行フローや評価ロジックを確認したいときは、この目次から `oracles.py` に進みたいとき。

## Do not read this when

- `cmoc apply`、`cmoc session`、`cmoc init` など別サブコマンドの実装や仕様を追いたいとき。
- `cmoc review oracles` ではなく、`oracles` 配下の個別仕様断片そのものを直接確認したいとき。
- `src/sub_commands/review` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接読むべきです。

## hash

- 1f6e4bb667025e8e35cdaa458b6674cb5018bc33043fdff73836dad1e5102560

# `session`

## Summary

- `src/sub_commands/session` は `cmoc session` 系サブコマンドの実装入口です。
- `__init__.py` はパッケージ宣言のみで、実行ロジックは `fork.py`、`join.py`、`abandon.py` に分かれています。
- この目次は session の開始・統合・破棄のどの実装へ進むべきかを素早く振り分けるためのものです。

## Read this when

- `cmoc session` 系サブコマンドの入口と各モジュールの担当範囲を把握したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` のどれを読むべきか整理したいとき。
- `src/sub_commands/session` 配下の実装・修正・レビュー・テストを始める前に、関連ファイルの入口を整理したいとき。

## Do not read this when

- 個別の `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の詳細仕様、状態遷移、例外条件だけを確認したいとき。
- `cmoc apply` 系の開始・統合・破棄の流れだけを確認したいとき。
- `src/sub_commands/session` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接読むべきです。

## hash

- 81fb0f4d687be7393e1c8257c8036f5d9c57f4ac1de1348d4dee6ecae64e3048

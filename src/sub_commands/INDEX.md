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

- `src/sub_commands/apply` は `cmoc apply` 系サブコマンド実装のまとまりで、`__init__.py` はパッケージ宣言のみ、`fork.py`・`join.py`・`abandon.py` が各サブコマンドの本体です。
- `fork.py` は apply branch と worktree の作成、要修正点の抽出と修正、`apply.state` の更新、レポート生成、`INDEX.md` の維持までを担当します。
- `join.py` は完了済みの apply branch を session branch に取り込み、想定外差分の扱い、`INDEX.md` conflict の自動解消、後始末を担当します。
- `abandon.py` は未 join の apply run を破棄し、必要なら実行中プロセスを停止して、apply branch と worktree を整理したうえで state を ready に戻します。

## Read this when

- `cmoc apply fork`・`cmoc apply join`・`cmoc apply abandon` の実装、修正、テスト、レビューを始める前に入口を確認したいとき。
- apply state の遷移、apply branch と worktree の生成・削除、merge 時の `--force-resolve` や conflict 解消の扱いを把握したいとき。
- `src/sub_commands/apply` がどのファイルで何を担当しているか、パッケージ全体の役割分担を素早く確認したいとき。

## Do not read this when

- `cmoc apply` の利用手順や仕様断片だけを確認したいときは、この実装ディレクトリではなく `oracles/docs/app_specs/sub_commands/` 側を読むべきです。
- `session` 側の開始・終了・統合だけを確認したいときは、このディレクトリではなく `src/sub_commands/session` 側を確認すべきです。
- `__init__.py` のようなパッケージ宣言だけを知りたいときは、この目次ではなく対象ファイルを直接読むだけで足ります。

## hash

- 29ea48e5c6d9e0cac12c5b1425989ab98da649a47fd2f34f84cc72ebda7ac835

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

- `cmoc apply`、`cmoc session`、`cmoc init` など別サブコマンドの実装や仕様を確認したいとき。
- `cmoc review oracles` ではなく、`oracles` 配下の個別仕様断片そのものを直接確認したいとき。
- `src/sub_commands/review` のパッケージ宣言だけを確認したいときは、`__init__.py` を直接読むべきです。

## hash

- a45c36bf2ed636fda5bc637ebba35a00a096ac07679f5d9a8714e5e25a2e05e7

# `session`

## Summary

- `src/sub_commands/session` は `cmoc session` 系サブコマンド実装の入口で、`__init__.py`、`fork.py`、`join.py`、`abandon.py` をまとめるディレクトリです。
- この配下では `fork` が session 開始、`join` が merge による完了、`abandon` が merge せず破棄を担当します。
- 個別実装に進む前に、session 系の責務分担と入口構造を俯瞰するための目次です。

## Read this when

- `cmoc session` 系サブコマンドの入口と、`fork`・`join`・`abandon` の役割分担を把握したいとき。
- `src/sub_commands/session` 配下のどの実装ファイルを読むべきか整理したいとき。
- `cmoc session fork`、`cmoc session join`、`cmoc session abandon` の実装・修正・レビュー・テストを始める前に、関連ファイルの位置関係を確認したいとき。

## Do not read this when

- `cmoc session` ではなく `cmoc apply` や `cmoc init` の実装・仕様を確認したいとき。
- `fork`、`join`、`abandon` のいずれか個別の詳細手順、状態遷移、例外条件だけを確認したいとき。
- このディレクトリのパッケージ宣言だけで足りるときは、`__init__.py` を直接読むべきです。

## hash

- 4501721235ccdb9decb85ed3abb2724d6240184ff98925d0accc91d1633f9963

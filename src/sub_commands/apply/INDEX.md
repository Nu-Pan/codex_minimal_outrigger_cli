# `__init__.py`

## Summary

- `src/sub_commands/apply/__init__.py` は `cmoc apply` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src/sub_commands/apply` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc apply` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- 個別の `cmoc apply fork/join/abandon` の実行フローや状態遷移を確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。

## hash

- 5646cb02b7ca8e507d8725e2d5f87e9580881d66ce1a67505595830d53c239d6

# `abandon.py`

## Summary

- `src/sub_commands/apply/abandon.py` は `cmoc apply abandon` の本体処理を実装するモジュールです。
- 現在の session に紐づく未 join の apply run を破棄し、`running` なら子プロセスを停止したうえで、apply branch と worktree を強制削除して `apply.state` を `ready` に戻します。
- 破棄前後の状態表示と warning 出力を行い、次回の apply 実行に支障が出ないよう session state の補助情報を初期化します。

## Read this when

- `src/sub_commands/apply/abandon.py` の役割と責務を素早く把握したいとき。
- `cmoc apply abandon` の実装・修正・レビュー・テストを始める前に入口を確認したいとき。
- 未 join の apply run を破棄する前提条件や、`session.state` / `apply.state` の検証条件を追いたいとき。
- `running` 中の apply を停止する挙動や、apply branch / worktree の cleanup 方針を確認したいとき。
- 破棄結果として標準出力に何を出し、warning をどう扱うかを確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点整理だけを確認したいとき。
- `cmoc apply join` や `cmoc session abandon` など、別サブコマンドの終了・統合・破棄手順だけを確認したいとき。
- `cmoc apply abandon` の仕様断片や利用手順だけを確認したいときは、実装ではなく正本仕様を直接読むべきとき。
- `src/sub_commands/apply` パッケージ全体の入口だけを確認したいとき。

## hash

- 62f15798e9638f295e46c5cc870085cfdc0a751b855334cabacac6cdc98b9ed0

# `fork.py`

## Summary

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体で、session branch 上で専用 apply branch と worktree を作成し、要修正点の調査・適用・レポート生成までをまとめて担当するモジュールです。
- 起動前の session/apply state 検証、`--repeat-investigate-and-fix` / `--repeat-improove-fixing-list` / `--scope` の検証、`apply.state` の `running` / `completed` / `error` 遷移、排他ロックと worktree 作成リトライを含みます。
- Structured Output による不整合調査、要修正点の整理、修正適用、commit、編集禁止領域の検査、YAML Front Matter 付き report 出力と変更要約生成まで扱います。

## Read this when

- `cmoc apply fork` の処理順と責務の境界を確認したいとき。
- `session.state` / `apply.state` の検証条件、apply branch/worktree の作成条件、scope ごとの調査対象選定を確認したいとき。
- Structured Output の要修正点生成、修正反映、commit、report 生成の流れを実装・修正・レビュー・テストしたいとき。
- 編集禁止領域の検査や report の検証条件を確認したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` の実装・終了処理だけを確認したいとき。
- `cmoc apply fork` の利用手順や正本仕様だけを確認したいときは、`oracles/app_specs/sub_commands/apply_fork.md` を直接読むべきとき。
- `src/sub_commands/apply` パッケージ全体の入口だけを確認したいときや、`INDEX.md` の生成ルールだけを確認したいとき。

## hash

- 899b27c632c0f057a1887962c8e6cf3cfb6f6fc68e8504222bc361053ac8bca4
<!-- cmoc-index-kind: file -->

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体実装で、完了済みの apply branch を session branch に取り込む処理を担当します。
- session/apply state の妥当性確認、現在 branch と local branch の存在確認、未コミット差分と想定外差分の検出・必要時の強制修復をまとめています。
- merge 後の `apply.state` を `ready` に戻す処理、`INDEX.md` conflict の自動解消、report/result の保存状況を踏まえた apply branch / worktree の cleanup まで扱います。

## Read this when

- `cmoc apply join` の実装・修正・レビュー・テストで、処理順や責務の境界を確認したいとき。
- apply branch を session branch に取り込む前提条件や、`--force-resolve` による想定外差分の扱いを確認したいとき。
- `INDEX.md` の conflict を自動解消する条件、merge 後の `apply.state` 更新、不要になった apply branch / worktree の削除条件を確認したいとき。
- report/result の保存状況に応じた cleanup の warning 条件を把握したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点リスト作成だけを確認したいとき。
- `cmoc apply abandon` の破棄手順や running 中の停止処理だけを確認したいとき。
- `cmoc apply join` の仕様断片や利用手順だけを確認したいときは、実装ではなく正本仕様を直接参照したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。

## hash

- 5aefd2f80aec3dd2d61d4a8b6c886f932f6c88239e5cb7746964f2f90510b85b
<!-- cmoc-index-kind: file -->

# `__init__.py`

## Summary

- `src/sub_commands/apply/__init__.py` は `cmoc apply` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- `src/sub_commands/apply` が Python パッケージとして宣言されていることを確認したいとき。
- `cmoc apply` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- 個別の `cmoc apply fork/join/abandon` の実行フローや状態遷移を確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/docs/app_specs/sub_commands/` 側を読むべきです。

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

- `cmoc apply fork` の本体実装で、session branch 上で専用の apply branch と worktree を作成し、`session.state` / `apply.state` の検証・更新、排他ロック、作業開始・終了の制御をまとめている。
- oracle ファイルと実装ファイルを対象に、Structured Output で不整合を調査し、要修正点の整理・改善・適用を並列実行しながら、`--repeat-investigate-and-fix`、`--repeat-improove-fixing-list`、`--scope` を扱う。
- 禁止領域の変更検査、`INDEX.md` の維持、コミット生成、Markdown + YAML Front Matter の apply report / error report 生成、および各種 prompt・validation helper をまとめている。

## Read this when

- `cmoc apply fork` の開始から report 出力までの全体フローを追いたいとき。
- `session.state` / `apply.state` の前提条件、`--repeat-investigate-and-fix`、`--repeat-improove-fixing-list`、`--scope` の挙動、または apply branch / worktree の作成リトライを確認したいとき。
- 不整合調査の Structured Output、要修正点リストの整理、修正の適用、禁止領域チェック、commit / report 生成の実装やテストを確認したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon`、`cmoc session fork/join/abandon` など、別サブコマンドの手順だけを確認したいとき。
- `cmoc apply fork` の CLI 登録や入口だけを確認したいときは、このファイルではなく `src/main.py` や `src/sub_commands/apply/INDEX.md` を先に読むべきです。
- `oracles` 配下の正本仕様そのものや、`INDEX.md` の生成ルールだけを確認したいときは、この実装ファイルを読む必要はありません。

## hash

- 97d354fa21c33b42457c37a4a5bdf7c8f21c69ac53f3e21dc89c3b504673d6d8

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体で、完了済みの apply branch を session branch に取り込む処理を実装するモジュールです。
- session/apply state の検証、現在ブランチと local ブランチの存在確認、未コミット差分の検出、想定外差分の `--force-resolve` 処理をまとめています。
- merge 後の `apply.state=ready` への更新、`INDEX.md` conflict の自動解消、保存済み report/result を踏まえた apply branch / worktree の cleanup まで担います。

## Read this when

- `cmoc apply join` の処理順、前提条件、終了後の後始末を実装・修正・レビュー・テストしたいとき。
- `--force-resolve` を付けたときに、想定外差分をどう扱うか確認したいとき。
- `INDEX.md` conflict の自動解消条件や、merge 後に `apply.state` を `ready` に戻す流れを確認したいとき。
- apply report と result の保存状況に応じて、`<cmoc-apply-branch>` と `<cmoc-apply-worktree>` を削除してよい条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや、要修正点リストの生成仕様だけを確認したいとき。
- `cmoc apply abandon` の破棄手順や、実行中プロセスの停止処理だけを確認したいとき。
- `cmoc session join` や `cmoc session abandon` など、session 側の終了・統合・破棄だけを確認したいとき。
- `cmoc apply join` の利用手順ではなく、仕様断片だけを読みたいときは正本仕様を直接参照したいとき。

## hash

- d165b399c718de13cda6d0ca8c1f844d3691b876734153ee3258eecf4ce649ec

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

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体で、session branch 上に専用 apply branch と worktree を作り、調査・修正・commit・report 生成までを一括で担う。
- session/apply state の検証、repeat 系オプションと `scope` の解釈、apply 開始時の排他制御と worktree 作成リトライを扱う。
- oracle / 実装ファイルを対象に Structured Output で不整合を調査し、要修正点の整理、追従修正、禁止領域検査、commit を反復する。
- Markdown + YAML Front Matter の apply report、変更要約の Structured Output、各種 validation と prompt 生成の補助関数をまとめている。

## Read this when

- `cmoc apply fork` の処理順や、開始から report 出力までの全体フローを追いたいとき。
- session.state / apply.state の前提条件、`--repeat-investigate-and-fix`、`--repeat-improove-fixing-list`、`--scope` の扱いを確認したいとき。
- 不整合調査の Structured Output、要修正点の整理、実装修正ループ、commit の境界を確認したいとき。
- apply report の YAML Front Matter、Markdown セクション検証、変更要約の生成条件を確認したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` の終了・破棄処理だけを追いたいとき。
- `cmoc apply` の入口定義だけで十分で、実装の細部や helper 群まで要らないとき。
- 個別の oracle 仕様や `oracles` 配下の正本断片そのものを確認したいとき。
- `cmoc session`、`cmoc init`、`cmoc review` など別サブコマンドの実装を見たいとき。

## hash

- c04bc891f48a043350b16e690cc6a8380c87327fb45b06374a026a1fc8b3f85d

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体で、完了済みの apply branch を session branch に取り込む処理を実装するモジュールです。
- session/apply state の検証、現在ブランチと local ブランチの存在確認、未コミット差分の検出、想定外差分の `--force-resolve` 処理をまとめています。
- merge 後の `apply.state=ready` への更新、`INDEX.md` conflict の自動解消、保存済み report/result を踏まえた apply branch / worktree の cleanup まで担います。

## Read this when

- `cmoc apply join` の処理順、前提条件、終了後の後始末を実装・修正・レビュー・テストしたいとき。
- `--force-resolve` を付けたときに、想定外差分をどう扱うか確認したいとき。
- `INDEX.md` conflict の自動解消条件や、merge 後に `apply.state` を `ready` に戻す流れを確認したいとき。
- apply report と result の保存状況に応じて、`<cmoc-apply-branch>` と `<cmoc-apply-worktree>` を削除してよい条件を確認したいとき.

## Do not read this when

- `cmoc apply fork` の調査・修正ループや、要修正点リストの生成仕様だけを確認したいとき。
- `cmoc apply abandon` の破棄手順や、実行中プロセスの停止処理だけを確認したいとき。
- `cmoc session join` や `cmoc session abandon` など、session 側の終了・統合・破棄だけを確認したいとき。
- `cmoc apply join` の利用手順ではなく、仕様断片だけを読みたいときは正本仕様を直接参照したいとき。

## hash

- 1b62ae4cdcbd532f3c9840511e60015d67e92c740825fd6be270262485b5824b

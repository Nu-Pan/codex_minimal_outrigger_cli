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

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体で、session branch 上に専用の apply branch と worktree を作り、要修正点の調査・整理・適用までをまとめて担当するモジュールです。
- 起動前の state 検証、repeat オプションと scope の検証、`apply.state` の遷移、排他ロック、worktree 作成リトライ、Structured Output による不整合調査を扱います。
- 修正反映、禁止領域チェック、commit、YAML Front Matter 付き report 生成、失敗時の error report 生成とフォールバック要約まで含めて、apply run 全体の流れを持ちます。

## Read this when

- `cmoc apply fork` の処理順、状態検証、worktree 作成、修正点調査の流れを確認したいとき。
- `session.state` / `apply.state` の検証条件や、repeat オプションと scope の扱いを実装・修正・レビューしたいとき。
- 要修正点の Structured Output、修正適用、commit、report 生成、error report 生成までの流れを追いたいとき。
- 編集禁止領域の検査や、apply run の終了条件・失敗時の扱いを確認したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` の終了処理だけを確認したいとき。
- `src/sub_commands/apply` パッケージ全体の入口だけを確認したいとき。
- `INDEX.md` の生成ルールや `oracles` 全体のルーティング方針だけを確認したいとき。
- `cmoc apply fork` の利用手順や仕様断片だけを確認したいとき。

## hash

- 7f4473873b68002944224b142b74c08ac1851906861f6b3ebae8895f2162fd20

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体で、完了済みの apply branch を session branch に取り込む処理を実装する。
- session/apply state の検証、現在ブランチと local ブランチの存在確認、未コミット差分の検出、想定外差分の `--force-resolve` 処理をまとめている。
- merge 後の `apply.state=ready` への更新、`INDEX.md` conflict の自動解消、保存済み report/result を踏まえた apply branch / worktree の cleanup まで担う。

## Read this when

- `cmoc apply join` の処理順、前提条件、終了後の後始末を実装・修正・レビュー・テストしたいとき。
- `--force-resolve` を付けたときに、想定外差分をどのように revert してから merge するか確認したいとき。
- `INDEX.md` conflict の自動解消条件や、merge 後に `apply.state` を `ready` に戻す流れを確認したいとき。
- apply report と result の保存状況に応じて、`<cmoc-apply-branch>` と `<cmoc-apply-worktree>` を削除してよい条件を確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点リストの仕様だけを確認したいとき。
- `cmoc apply abandon` の破棄手順や running 中の停止処理だけを確認したいとき。
- `cmoc session join` や `cmoc session abandon` など、session 側の終了・統合・破棄だけを確認したいとき。
- `cmoc apply join` の利用手順や仕様断片だけを読みたいときは、実装ではなく正本仕様を直接参照したいとき。
- このディレクトリの `INDEX.md` 全体方針や、`oracles` のルーティング方針だけを確認したいとき。

## hash

- a9689461069946ed57458c52d977a474be944350d00edb0d177965d4a8945a1b

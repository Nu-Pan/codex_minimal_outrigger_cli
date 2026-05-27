# `__init__.py`

## Summary

- - `src/sub_commands/apply/__init__.py` は `cmoc apply` 系サブコマンドのパッケージ宣言だけを担う最小モジュールです。
- - 公開 API、定数、実行ロジック、再エクスポートは持ちません。

## Read this when

- - `src/sub_commands/apply` が Python パッケージとして宣言されていることを確認したいとき。
- - `cmoc apply` 系サブコマンドの入口となるパッケージ構造を把握したいとき。

## Do not read this when

- - 個別の `cmoc apply fork/join/abandon` の実行フローや状態遷移を確認したいときは、このファイルではなく各実装モジュールを読むべきです。
- - `cmoc apply` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/` 側を読むべきです。

## hash

- 5646cb02b7ca8e507d8725e2d5f87e9580881d66ce1a67505595830d53c239d6

# `abandon.py`

## Summary

- `src/sub_commands/apply/abandon.py` は `cmoc apply abandon` の本体処理を実装するモジュールです。
- 現在の session に紐づく未 join の apply run を破棄し、running 中なら停止したうえで apply worktree と apply branch を強制削除し、`apply.state` を `ready` に戻します。
- 破棄前後の状態表示と warning 出力を行い、次回の apply 実行に支障がないよう session state の補助情報を初期化します。

## Read this when

- `cmoc apply abandon` の実装・修正・レビュー・テストを行いたいとき。
- 未 join の apply run を破棄する前提条件、`apply.state` の検証、running apply の停止、worktree / branch の cleanup を確認したいとき。
- 破棄結果として標準出力に何を出し、warning をどう扱うかを確認したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループや要修正点一覧の生成だけを確認したいときは、このファイルではなく `fork.py` を読むべきです。
- `cmoc apply join` や `cmoc session abandon` など、別サブコマンドの終了・統合・破棄手順だけを確認したいときは、このファイルではなく該当モジュールを読むべきです。
- `cmoc apply abandon` の仕様断片や利用手順だけを確認したいときは、`oracles/app_specs/sub_commands/apply_abandon.md` を直接読むべきです。

## hash

- 496c8839373d9dc0dac817039b3a6e2874d4f414c2046ed8b9afe7ea887955b7

# `fork.py`

## Summary

- `src/sub_commands/apply/fork.py` は `cmoc apply fork` の本体処理を実装するモジュールで、session branch の前提確認から apply branch / worktree の作成、調査・修正ループ、レポート出力までをまとめて扱います。
- 要修正点の Structured Output 検証、部分適用・全体適用の切り替え、対象 oracle / 実装ファイルの列挙、改善ループ、禁止領域チェック、コミット生成と state 更新を担います。
- このディレクトリの入口として、`cmoc apply fork` の処理順や責務境界を追うための案内です。

## Read this when

- `cmoc apply fork` の実装・修正・レビュー・テストで、全体の処理順を確認したいとき。
- session state の検証、apply branch / worktree の生成、調査・修正ループ、要修正点の整理、レポート保存までの流れを追いたいとき。
- 部分適用モードと全体適用モードの違い、調査対象ファイルの選定規則、要修正点リストの改善ループを確認したいとき。
- Structured Output の schema 検証、禁止領域の変更検査、コミット生成、`apply.state` の `running` / `completed` / `error` 遷移を確認したいとき。

## Do not read this when

- `cmoc apply join` や `cmoc apply abandon` の挙動だけを確認したいとき。
- `cmoc session fork/join/abandon` など、session 側の処理だけを確認したいとき。
- `cmoc apply fork` の仕様断片そのものを確認したいときは、`oracles/app_specs/sub_commands/apply_fork.md` を読むべきで、この実装ファイルを読む必要はありません。
- Codex CLI 呼び出しの共通基盤や `INDEX.md` メンテナンスの一般ルールだけを確認したいとき。

## hash

- 869eeac4b502dffea0d00200c6afd25f0eba70faa4972eef8cd542778704611d

# `join.py`

## Summary

- `src/sub_commands/apply/join.py` は `cmoc apply join` の本体処理を実装するモジュールです。
- 完了済みの apply branch を session branch に `git merge --no-ff` で取り込み、session/apply state を更新します。
- 想定外差分の検出と `--force-resolve` による revert、merge conflict の報告、終了後の apply branch / worktree の削除判定を扱います。

## Read this when

- `cmoc apply join` の引数、実行順序、前提条件、エラー条件を確認したいとき。
- 想定外差分の検出方法と `--force-resolve` の分岐を確認したいとき。
- マージ後の `apply.state` 更新や、apply branch / worktree の削除条件を確認したいとき。
- `src/sub_commands/apply/join.py` の責務境界や処理順を把握したいとき。

## Do not read this when

- `cmoc apply fork` の調査・修正ループだけを確認したいときは、このモジュールではなく `fork.py` を読むべきです。
- `cmoc apply abandon` の破棄処理や cleanup 方針だけを確認したいときは、このモジュールではなく `abandon.py` を読むべきです。
- `cmoc session` 系や他のサブコマンドの実装だけを確認したいときは、このモジュールではなく該当モジュールを読むべきです。
- `cmoc apply join` の仕様断片だけを確認したいときは、`oracles/app_specs/sub_commands/apply_join.md` を直接読むべきです。

## hash

- 4376b574bd041df6f81cfb2c5789f6c383ff82e009be59e05645d3872f7ea37f

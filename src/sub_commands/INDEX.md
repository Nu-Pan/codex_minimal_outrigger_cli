# `__init__.py`

## Summary

- cmoc のサブコマンド実装パッケージであることを示すパッケージ初期化ファイル。
- 実行ロジックや公開 API の定義は含まず、パッケージ用途を docstring で説明するだけのファイル。

## Read this when

- src/sub_commands 配下が何のためのパッケージかを最小限確認したいとき。
- サブコマンド実装モジュール群のパッケージ境界や概要を確認したいとき。

## Do not read this when

- 個別サブコマンドの処理内容、引数、実行フローを調べたいとき。
- cmoc のコマンドルーティング、CLI エントリポイント、サブコマンド登録方法を調べたいとき。
- 実装上の詳細な仕様やテスト対象の振る舞いを確認したいとき。

## hash

- ea4df02b820eba1ca77dfb1b2227c81dbff61cd7c4c2bf4d26d891369b57fa77

# `apply.py`

## Summary

- `src/sub_commands/apply.py` は `cmoc apply` の本体実装モジュールで、`oracles` と実装の不整合調査、修正適用、コミット、レポート出力までをまとめて扱います。
- 作業ブランチ上での実行確認、`.cmoc` の追跡除外保証、`oracles` 以外の未コミット差分拒否、`INDEX.md` の維持といった前処理を含みます。
- 不整合調査の Structured Output schema、要修正点リストの整理、修正作業ループ、commit message 生成、apply レポート生成と終了コード返却の実装を含みます。

## Read this when

- `cmoc apply` の実行フロー、前提条件、反復回数、終了条件を確認したいとき。
- 部分適用と全体適用の切り替え条件や、調査対象の oracle ファイル・実装ファイルの絞り込みを追いたいとき。
- Codex CLI に渡す調査・整理・適用・commit message 生成のプロンプトや、要修正点 JSON の schema を確認したいとき。
- `INDEX.md` の維持、変更の自動 commit、編集禁止領域の検査、apply レポートの生成・検証を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの実装だけを確認したいとき。
- Codex CLI の共通呼び出し規約、ログ、エラーハンドリング、`INDEX.md` 自動生成の共通仕様だけを確認したいとき。
- `oracles` 側の正本仕様そのものを読みたいときや、テスト観点だけを先に確認したいとき。
- 共通ユーティリティや git 操作ヘルパーだけを追いたいとき。

## hash

- 50738d5c63393972ca7a6e75e71bc9d1a1c27f552e7b5eb2e93bd155550f4bc8

# `branch.py`

## Summary

- `cmoc branch` の本体処理をまとめたルーティング用ファイルです。
- `git checkout -b` による作業用ブランチ作成、`cmoc_<time-stamp>` 形式のブランチ名生成、衝突時の最大 10 回リトライを扱います。
- 作成元の `HEAD` を base commit として記録し、`.cmoc/branch/<branch>.txt` へ保存します。
- 作成後に `.cmoc` が git 追跡対象外であることを保証し、`StepTimer` で 3 段階の進捗表示と経過時間報告を行います。

## Read this when

- `cmoc branch` の実装フローや処理順を確認したいとき。
- 作業用ブランチ名の生成規則や、名前衝突時のリトライ挙動を確認したいとき。
- base commit の取得タイミングと、その保存先を確認したいとき。
- `.cmoc` の追跡除外保証や、進捗表示・経過時間レポートの扱いを確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの実装を調べたいとき。
- repo root 探索、git 実行、timestamp 生成、`StepTimer` など共通ユーティリティそのものを調べたいとき。
- CLI エントリーポイントでのサブコマンド登録や引数定義だけを確認したいとき。
- `src/sub_commands` 配下の他ファイルや、ルーティング目次全体を確認したいとき。

## hash

- d5849b98d41d0a4141bfd20cc13fb2f98ac5a781a9f4f21f2fe5f30c445eebd0

# `eval_oracles.py`

## Summary

- `cmoc eval-oracles` の本体実装で、oracle 断片の評価からレポート保存までをまとめて扱う。
- `.cmoc` が git 追跡対象外であることを事前に保証し、既存の `INDEX.md` をメンテナンスしたうえで評価を進める。
- `--full` の有無と現在のブランチ状態から、部分評価か全体評価かを切り替える。
- 対象 oracle ごとに `codex exec` を呼び出し、Structured Output の JSON を検証して評価結果を集約する。
- 評価結果は `.cmoc/reports/eval-oracles` 配下の Markdown レポートとして保存し、モード、ブランチ、コミット、問題件数を記録する。

## Read this when

- `cmoc eval-oracles` の処理順序、前処理、出力レポートの構成を確認したいとき。
- `--full` の有無や cmoc ブランチ上かどうかで、どの oracle を評価するか知りたいとき。
- 評価時に参照してよい `oracles` 配下のファイル範囲や、`INDEX.md` の扱いを確認したいとき。
- `codex exec` に渡す評価プロンプト、Structured Output の期待値、JSON 検証の流れを確認したいとき。
- レポート保存先、frontmatter の項目、問題件数の集計方法を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など他サブコマンドの仕様だけを知りたいとき。
- Codex CLI の低レベルな実装や、共通 runner、repo 操作、タイムスタンプ生成だけを調べたいとき。
- `INDEX.md` 自動生成や更新ロジックそのものを調べたいとき。
- oracle ファイルの列挙条件や、変更検出の個別実装だけを確認したいとき。
- 開発規約、コーディング規約、テスト規約などの開発者向けルールだけを確認したいとき。

## hash

- ace18f9932a352ec8e2610650b375d53dc66dea41ed44c7b20571c4de7a0c449

# `init.py`

## Summary

- `cmoc init` サブコマンドの本体処理を定義する実装ファイル。
- 直接呼び出し時は共通 runner に処理を委譲し、`repo_root` の解決と共通エラー整形を受ける。
- `.cmoc` が git 追跡対象外になるよう、`.gitignore` ルールの追加と既存 tracked file の追跡解除を保証する。
- 初期化で発生した変更のみを必要に応じてコミットし、`StepTimer` で 2 段階の進捗表示と完了時の経過時間報告を行う。

## Read this when

- `cmoc init` の実装本体と処理の流れを確認したいとき。
- `.cmoc` を git 追跡対象外にする処理の呼び出し順序を確認したいとき。
- `cmoc init` がどの条件で `.gitignore` や git index の変更をコミットするか調べたいとき。
- `cmoc init` の stdout 進捗表示、ステップ名、完了時の時間レポートを確認したいとき。
- テストから `cmoc_init_impl` を直接呼び出す際の `repo_root` 引数の扱いを確認したいとき。

## Do not read this when

- CLI エントリーポイントで `init` サブコマンドがどう登録されるかだけを調べたいとき。
- `.cmoc` ignore ルールの具体的な `.gitignore` 編集や git 操作の詳細実装を調べたいとき。
- 共通 runner の `repo_root` 解決、例外処理、終了ステータス整形の詳細を調べたいとき。
- タイマーや経過時間表示の内部実装だけを調べたいとき。
- `cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの挙動を調べたいとき。

## hash

- 766eb4ef5567a176766be2bb55dbc8f955c55af92c1ddc3f64043c1be4bda4ee

# `merge.py`

## Summary

- `cmoc merge` の本体実装が書かれている Python モジュールです。
- `cmoc_merge_impl` を中心に、未コミット差分の検証、`<cmoc-branch>` の自動解決、`git merge` 実行、コンフリクト時の解消依頼、マージ後のブランチ削除判定を扱います。
- Codex CLI へ渡すコンフリクト解消用プロンプト、conflict marker 検査、`git add` と `git commit` の実行順も含みます。

## Read this when

- `cmoc merge` の実装や挙動を修正・確認したいとき。
- マージ元ブランチの自動解決条件や、候補が複数・未確定だった場合のエラー処理を確認したいとき。
- `git merge` 失敗後にどこまでを cmoc が処理し、どこからを手動解決に切り替えるか確認したいとき。
- マージ完了後に source branch を削除してよい条件や、削除失敗時の warning 挙動を確認したいとき。
- Codex CLI に conflict 解消を依頼する際の入力内容や制約を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles` など他のサブコマンドの実装だけを調べたいとき。
- cmoc 全体の開発規約、コーディング規約、テスト規約だけを確認したいとき。
- `git` の一般的な merge 操作や conflict 解消の一般論だけを知りたいとき。
- `README.md`、`AGENTS.md`、`oracles` の運用ルールや編集可否だけを確認したいとき。

## hash

- c92c70c3d856e00f115f6f8df81d01956fd3beaa8fdb869008074fbaa268f3c9

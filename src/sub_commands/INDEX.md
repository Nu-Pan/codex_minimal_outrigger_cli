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

- `src/sub_commands/apply.py` は `cmoc apply` の本体実装で、oracle と実装の不整合調査から修正適用、コミット、レポート出力までを一括して扱うファイルです。
- `cmoc` 作業ブランチの確認、`.cmoc` の追跡除外保証、`INDEX.md` の維持、未コミット差分の検査、反復回数の検証など、実行前後の制御も含みます。
- 不整合調査用の Structured Output schema 検証、要修正点リストの整理、個別修正の実行、apply レポートの保存と終了コード決定の流れを含みます。

## Read this when

- `cmoc apply` の実行フロー、前提条件、部分適用と全体適用の切り替え、反復回数、終了コードを確認したいとき。
- oracle と実装の不整合調査に使う Codex CLI の prompt、Structured Output schema、要修正点リストの改善ロジックを追いたいとき。
- 変更の自動コミット、編集禁止領域の検査、`INDEX.md` の維持、apply レポートの生成と検証を確認したいとき。
- このファイル内の補助関数の役割や、各処理がどの順番で呼ばれるかを把握したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの実装だけを調べたいとき。
- Codex CLI の共通呼び出し規約、ログ、エラーハンドリング、`INDEX.md` 自動生成の共通仕様だけを確認したいとき。
- `oracles` 側の正本仕様そのものを読みたいとき。
- 共通ユーティリティや git 操作ヘルパーだけを追いたいとき。

## hash

- cd452d5c5735e8bc0ce304a5d96b0085de68092058c946947617ebfd4b239f91

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

- `src/sub_commands/eval_oracles.py` は `cmoc eval-oracles` の本体実装で、oracle 断片の評価、検証、レポート保存までをまとめて扱うモジュールです。
- 実行前に `.cmoc` の ignore 保証と `INDEX.md` メンテナンスを行い、`--full` と `cmoc` ブランチ状態に応じて部分評価か全体評価かを切り替えます。
- 各 oracle ファイルごとに `codex exec` を呼び出し、Structured Output の JSON schema を検証したうえで、評価結果を 1 つの Markdown レポートに集約します。
- 評価レポートには severity 別の issue 集計、評価順を保った問題一覧、参照した oracle / `INDEX.md` の一覧、エラー時の代替レポート出力も含まれます。

## Read this when

- `cmoc eval-oracles` の処理順序、前処理、評価実行、レポート保存までの流れを確認したいとき。
- `--full` の有無や `cmoc` ブランチ上かどうかで、どの oracle ファイルを評価するか知りたいとき。
- 評価用 prompt の内容、許可される参照範囲、Structured Output schema、JSON 検証ロジックを確認したいとき。
- 評価結果の集計方法、severity ごとの並び順、レポートの Markdown 体裁とエラー時の出力を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など他サブコマンドの実装だけを調べたいとき。
- Codex CLI の共通呼び出し規約、ログ、エラーハンドリング、`INDEX.md` 自動生成の共通仕様だけを確認したいとき。
- `oracles` 配下の正本仕様そのものを読みたいとき。
- 開発規約、コーディング規約、テスト規約など、開発者向けルールだけを確認したいとき。

## hash

- 27594a3633c164a64be706f0c05e01074cb7617096fe9fabdcba90e9356a6b22

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

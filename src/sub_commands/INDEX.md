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

- `cmoc apply` の本体実装をまとめるモジュールです。
- 不整合調査、要修正点の整理、個別適用、修正後の commit、作業レポート保存までの流れを扱います。
- 部分適用・全体適用の切り替え、対象ファイルの選別、反復回数制御、Structured Output 検証、編集禁止領域チェック、各種 prompt 生成とレポート検証の補助関数も含みます。

## Read this when

- `cmoc apply` の処理順序や全体フローを確認したいとき。
- 不整合調査用の Structured Output schema、要修正点の整理ロジック、実装への追従ループを確認したいとき。
- 部分適用と全体適用の切り替え条件、調査対象の絞り込み、修正後の commit やレポート保存の流れを確認したいとき。
- このモジュール内の prompt 生成関数、JSON 検証関数、レポート検証関数の役割を把握したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの実装だけを調べたいとき。
- `commons` 側の共通基盤、たとえば `run_codex_exec` や git ユーティリティの詳細だけを確認したいとき。
- `oracles/app_specs/sub_commands/apply.md` にある正本仕様そのものを読みたいとき。
- `cmoc` 全体の開発ルール、コーディング規約、テスト方針だけを確認したいとき。

## hash

- cf40519616b1d190d6e1c4a9e139e31fa2bc70528ca36709d6e658df406ecfde

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

# `eval-oracles.py`

## Summary

- `src/sub_commands/eval-oracles.py` は `cmoc eval-oracles` の本体実装で、oracle 断片の評価実行、Structured Output の検証、Markdown レポート生成をまとめて担当するモジュールです。
- 実行前に `.cmoc` の ignore 保証と `INDEX.md` のメンテナンスを行い、`--full` と現在のブランチ状態に応じて部分評価モードと全体評価モードを切り替えます。
- 各 oracle ファイルに対して `codex exec` を読み取り専用で呼び出し、参照可能な `oracles` / `INDEX.md` の範囲だけを見せて評価結果を収集します。
- 評価結果は severity ごとに集約され、通常レポートまたは error レポートとして `.cmoc/reports/eval-oracles/<timestamp>.md` に保存されます。

## Read this when

- `cmoc eval-oracles` の処理順序、前処理、評価実行、レポート保存までの流れを確認したいとき。
- `--full` の有無や `<cmoc-branch>` 上かどうかで、どの oracle ファイルを評価するか知りたいとき。
- 評価用 prompt、Structured Output schema、JSON 検証ロジック、issue の severity 順序や番号付けを確認したいとき。
- 評価レポートの YAML frontmatter、本文構成、参照ファイル一覧、エラー時の代替出力を確認したいとき。
- このファイル内の補助関数の役割や、各処理がどの順番で呼ばれるかを把握したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など他のサブコマンドの実装だけを調べたいとき。
- `codex exec` の共通呼び出し規約、ログ、共通エラーハンドリングだけを確認したいとき。
- `oracles` 側の正本仕様そのものを読みたいとき。
- 開発規約、コーディング規約、テスト規約など、`cmoc` 自体の開発者向けルールだけを確認したいとき。

## hash

- 8dbd4e4386d66f709cb2524ea2100c941f9589fc671a717f70adb1be1447879c

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

- `src/sub_commands/merge.py` は `cmoc merge` の本体実装をまとめたモジュールです。
- 未コミット差分の確認、`<cmoc-branch>` の自動解決、`git merge` の実行、コンフリクト解消の依頼、マージ後のブランチ削除判定までを扱います。
- 共通 runner 経由で `repo_root` を解決する直接呼び出しパスと、`StepTimer` による進捗表示・経過時間報告を含みます。
- コンフリクト時の Codex CLI への依頼文、conflict marker 検査、`git add`、`git commit` の順序もこのモジュールの担当範囲です。

## Read this when

- `cmoc merge` の実装や挙動を修正・確認したいとき。
- マージ元 `<cmoc-branch>` の引数仕様や、自動解決条件を確認したいとき。
- マージ前の前提条件、未コミット差分チェック、`.cmoc` の ignore 保証を確認したいとき。
- git merge のコンフリクト発生後に、cmoc がどこまで解決し、どこから手動対応へ切り替えるかを確認したいとき。
- マージ完了後の source branch 削除条件や、削除失敗時の warning 挙動を確認したいとき。

## Do not read this when

- `cmoc merge` 以外のサブコマンド仕様だけを調べたいとき。
- cmoc 全体の開発ルール、コーディング規約、テスト規約だけを確認したいとき。
- git の一般的な merge 操作や conflict 解消の一般論だけを知りたいとき。
- `README.md`、`AGENTS.md`、`oracles` の運用ルールや編集可否だけを確認したいとき。

## hash

- 7d9017bc3ccbf62d9c08be6ef19cbb8b3e44d2031c2479a2464dc3601a5b99a3

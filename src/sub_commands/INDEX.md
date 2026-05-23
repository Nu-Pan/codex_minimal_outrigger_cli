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

- `cmoc apply` の本体処理を実装したモジュールです。
- 不整合調査・整理・適用の反復ループ、対象ファイルの列挙、Codex CLI への依頼文生成を含みます。
- 不整合リスト用 Structured Output schema の検証、禁止領域チェック、変更の commit、作業レポート生成を担当します。

## Read this when

- `cmoc apply` の実行フロー、引数、反復回数、部分適用・全体適用の切り替えを実装・確認したいとき。
- `oracles` と実装の不整合を Codex CLI に調査させ、要修正点を整理して適用する処理を確認したいとき。
- 作業結果レポートの出力、`.cmoc/reports/apply` への保存、終了コードの扱いを確認したいとき。
- 不整合調査用の JSON schema 検証や、ファイル単位の Codex 呼び出し条件を確認したいとき。

## Do not read this when

- `cmoc branch`、`cmoc init`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの仕様だけを調べたいとき。
- `INDEX.md` の自動生成・更新ルールだけを確認したいとき。
- `cmoc` 自体のコーディング規約、設計規約、テスト規約など開発者向けルールだけを調べたいとき。
- 共通の repo 操作ユーティリティやログ・タイムスタンプ仕様だけを確認したいとき。

## hash

- 648f4dc0fa635548f5ce2c2124c4f241da6ac60d0ad645b6594436442053e02c

# `branch.py`

## Summary

- `cmoc branch` の本体処理を実装するファイルです。
- 共通 runner 経由で `<repo-root>` を解決し、作業用ブランチ `cmoc_<time-stamp>` を作成して、作成元 commit を `.cmoc/branch/<branch>.txt` に記録します。
- ブランチ名の衝突時は最大 10 回までリトライし、`StepTimer` で 3 段階の進捗表示と経過時間レポートを行います。

## Read this when

- `cmoc branch` の実装フローや処理順を確認したいとき。
- 作業用ブランチ名の生成規則、衝突時のリトライ挙動を確認したいとき。
- base commit の取得タイミング、`.cmoc` の追跡除外保証、stdout の進捗表示や計測を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの実装を調べたいとき。
- repo root 探索、git 実行、`timestamp` 生成、`StepTimer` など共通ユーティリティそのものを調べたいとき。
- `cmoc branch` の正本仕様や、`src/sub_commands` 以外のルーティング目次だけを確認したいとき。

## hash

- a2f0aaa3562304fd93b3e17fb51f579f2c1028009ef6ad0d22e262dfda477021

# `eval_oracles.py`

## Summary

- `src/sub_commands/eval_oracles.py` は `cmoc eval-oracles` の本体実装で、oracle 断片の評価からレポート保存までを担当します。
- 評価前の `.cmoc` の ignore 保証、`INDEX.md` メンテナンス、oracle ファイル列挙、部分評価・全体評価の切り替えをまとめて扱います。
- 各 oracle に対する `codex exec` 呼び出し用の評価 prompt 組み立てと、評価出力に必須見出しがあるかの検証を含みます。
- 評価結果は `.cmoc/reports/eval-oracles` に Markdown レポートとして保存され、モード・ブランチ・コミット情報も記録します。

## Read this when

- `cmoc eval-oracles` の実行フロー、ステップ順序、進捗表示を確認したいとき。
- `--full` の有無や cmoc ブランチ判定によって、部分評価と全体評価がどう切り替わるか調べたいとき。
- 評価対象 oracle の選定条件や、削除 oracle がある場合の扱いを確認したいとき。
- `codex exec` に渡す oracle 評価 prompt の内容、参照可能な `oracles` / `INDEX.md` の範囲、読み取り専用条件を確認したいとき。
- 評価出力の検証条件や、`.cmoc/reports/eval-oracles` に保存されるレポートの最低限の構成を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc merge` など他サブコマンドの実装を調べたいとき。
- Codex CLI の低レベル実装や、共通 runner・repo 操作・timestamp 生成などの共通処理だけを調べたいとき。
- `INDEX.md` 自動メンテナンスの生成規則や更新ロジックそのものを調べたいとき。
- oracle ファイルの列挙や変更検出など、評価対象選定の個別実装だけを確認したいとき。
- oracle 評価の正本仕様や、致命的問題の定義そのものを仕様断片として読みたいとき。

## hash

- 73c22f10cf34a91b0a882d027f6fe09813a5661ac0e5b560fa9b54fef127e998

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

- `src/sub_commands/merge.py` は `cmoc merge` の本体実装です。
- 未コミット差分の検証、`.cmoc` の追跡除外保証、マージ元ブランチの解決、`git merge` 実行、コンフリクト解消支援、作業ブランチ削除までを扱います。
- `StepTimer` による進捗表示と経過時間の計測もこのファイルの責務です。

## Read this when

- `cmoc merge` の実装、修正、テストを確認したいとき。
- マージ前の前提条件や、マージ元 `<cmoc-branch>` の自動解決条件を確認したいとき。
- コンフリクト発生時の Codex CLI への依頼内容、conflict marker 検査、`git add`、merge commit 作成の流れを確認したいとき。
- マージ完了後に `<cmoc-branch>` を削除してよい条件や、削除失敗時の warning 挙動を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles` など他サブコマンドの本体実装を調べたいとき。
- CLI エントリーポイントでのサブコマンド登録や引数定義だけを調べたいとき。
- `commons` 配下の共通処理、git ラッパー、Codex CLI ラッパー、時間計測の共通ユーティリティだけを調べたいとき。
- `oracles` 配下の正本仕様や、`tests` 配下の自動テスト全体構成を調べたいとき。

## hash

- 0aa910967824a53bfa15bfd859ae756c4047f9a1663e6484302f12d36b4a7577

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

- `cmoc apply` サブコマンドの本体処理を実装するファイル。
- cmoc 作業ブランチ上での実行確認、oracle 以外の未コミット差分拒否、`.cmoc` ignore 保証、oracle 差分のコミット、`INDEX.md` メンテナンスを行う。
- oracle ファイルごとに Codex CLI の read-only 実行で実装との不整合を Structured Output JSON として調査し、最大 5 回まで workspace-write 実行で追従修正を反復する。
- 不整合追従後は編集禁止領域の差分を検査し、Codex 生成の 1 行 commit message で全変更をコミットする。
- apply 実行レポートを `.cmoc/reports/apply/<timestamp>.md` に保存し、完了時は 0、未完了時は `APPLY_INCOMPLETE_EXIT_CODE` の 2 を返す。
- 不整合調査用 JSON schema、調査・実装修正・レポート・commit message 生成用プロンプト、Structured Output payload の厳密なバリデーション処理を含む。

## Read this when

- `cmoc apply` の実行フロー、ステップ表示、終了コード、反復回数を確認したいとき。
- oracle と実装の不整合をどのように Codex CLI へ調査・修正依頼しているか調べたいとき。
- 不整合調査の Structured Output schema や `discrepancies` payload の検証ルールを確認したいとき。
- apply 中に `.gitignore`、`.cmoc`、`oracles`、`INDEX.md`、実装差分がどの順番で処理・コミットされるか確認したいとき。
- apply が編集禁止領域として `oracles/`、`.agents/`、`memo` をどう扱うか調べたいとき。
- `.cmoc/reports/apply` に保存される apply レポートの生成タイミングやプロンプト内容を確認したいとき。
- `commons.codex`、`commons.repo`、`commons.indexing`、`commons.timing`、`commons.timestamps` との連携点を追いたいとき。

## Do not read this when

- `cmoc apply` 以外のサブコマンド実装だけを調べたいとき。
- Codex CLI 呼び出しの低レベル実装、JSON パース、git コマンド実行、タイマー、タイムスタンプ生成などの共通処理そのものを確認したいとき。
- oracle 仕様断片の内容やルーティング情報そのものを調べたいとき。
- `INDEX.md` メンテナンスの具体的な生成規則やファイル走査規則だけを調べたいとき。
- テストコードの構成や Fake Codex CLI の挙動だけを確認したいとき。
- ユーザー向け README、インストール手順、PATH 設定、全体ワークフローの説明だけが必要なとき。

## hash

- 1c8abc6455215e243b76f64c64108a1157faa67e0446144dc04c10c039a6c843

# `branch.py`

## Summary

- `cmoc branch` サブコマンドの本体処理を実装するファイルです。
- 作業用ブランチ作成前の HEAD commit を base commit として取得し、`cmoc_<timestamp>` 形式の一意なブランチを作成します。
- ブランチ作成後に `.cmoc` が git 追跡対象外であることを保証し、ブランチ名に対応する `.cmoc/branch` 配下のファイルへ base commit を記録します。
- ブランチ名衝突時は timestamp を作り直しながら短い sleep を挟んで最大 10 回 `git checkout -b` をリトライします。
- 進捗表示と処理時間計測には `StepTimer` を使い、`branch (1/3)` から `branch (3/3)` までの段階的な stdout 出力を行います。

## Read this when

- `cmoc branch` の実行本体、進捗表示、処理順序を確認したいとき。
- 作業用ブランチ名 `cmoc_<timestamp>` の生成や、衝突時のリトライ挙動を実装・修正したいとき。
- ブランチ作成元の HEAD commit をどのタイミングで取得し、どこへ記録するか調べたいとき。
- `.cmoc` を git 追跡対象外にする処理が `cmoc branch` 内でいつ呼ばれるか確認したいとき。
- `branch_base_commit_path`、`head_commit`、`run_git`、`ensure_cmoc_ignored` などの共通 repo ヘルパーとの接続箇所を追いたいとき。
- `run_command(cmoc_branch_impl)` による CLI 実行時の呼び出し分岐を確認したいとき。

## Do not read this when

- `cmoc branch` の正本仕様やユーザー向け仕様だけを確認したいとき。
- `cmoc init`、`cmoc apply`、`cmoc merge`、`cmoc eval-oracles` など他サブコマンドの実装を調べたいとき。
- git コマンド実行ヘルパー、リポジトリ探索、`.cmoc` パス生成などの共通処理そのものの詳細を調べたいとき。
- timestamp のフォーマットや生成規則そのものを確認したいとき。
- テスト実装、Fake Codex CLI、pytest 規約など、テスト側のルールを調べたいとき。
- `INDEX.md` 自動生成や oracle 評価など、ルーティング文書関連の仕様を調べたいとき。

## hash

- a2a1dc8602bb135cd22e9049dc55722f354c25a0dcd84d247f87cbb3480c34cc

# `eval-oracles.py`

## Summary

- `cmoc eval-oracles` サブコマンドの本体処理を実装するファイルです。
- `.cmoc` の ignore 保証、`INDEX.md` メンテナンス、評価対象 oracle ファイルの選択、Codex CLI による評価実行、Markdown レポート保存までの一連の処理を扱います。
- cmoc 作業ブランチかつ `--full` 未指定で削除 oracle がない場合は変更 oracle のみを部分評価し、それ以外は全 oracle を全体評価します。
- oracle 評価用プロンプトでは、対象 oracle だけでなく関連仕様、`INDEX.md`、必要な実装・テスト・設定を読むこと、`memo` 読み書き禁止、ファイル編集禁止を Codex CLI に指示します。
- 評価結果レポートは `.cmoc/reports/eval-oracles/<timestamp>.md` に frontmatter と oracle ごとの評価本文をまとめて保存します。

## Read this when

- `cmoc eval-oracles` の実行フロー、進捗表示、評価ステップ数、レポート保存処理を確認したいとき。
- `--full` の有無、cmoc ブランチ判定、base commit、削除 oracle の有無から部分評価と全体評価がどう切り替わるか調べたいとき。
- Codex CLI に oracle 評価を依頼する際のプロンプト内容、read-only 指定、JSON 期待有無を確認したいとき。
- 評価前に `.cmoc` ignore 保証や `INDEX.md` メンテナンスが実行される順序を確認したいとき。
- eval-oracles の Markdown レポートに含まれる frontmatter 項目や出力先パスを確認したいとき。

## Do not read this when

- `cmoc eval-oracles` の CLI 引数定義や argparse との接続だけを確認したいとき。
- oracle ファイル列挙、変更検出、ブランチ判定、base commit 読み取りなどの個別 git・repo ユーティリティ実装を詳しく調べたいとき。
- Codex CLI 実行共通処理、Structured Output、サンドボックス指定などの共通呼び出し実装そのものを確認したいとき。
- `INDEX.md` 自動メンテナンスの対象、除外規則、目次生成ロジックの詳細を調べたいとき。
- タイムスタンプ生成、ステップ時間計測、共通コマンド実行ラッパーの内部仕様だけを調べたいとき。

## hash

- e8b0fd770d124972b0a927af7556df069beb856150aa344720b484a8d7d69715

# `eval_oracles.py`

## Summary

- `cmoc eval-oracles` の実装本体 `eval-oracles.py` を Python の import 互換名から読み込む薄いラッパーモジュールです。
- `importlib.util.spec_from_file_location` で同階層の hyphen 名ファイルを `sub_commands._eval_oracles_body` として動的ロードします。
- 本体モジュールの `run_codex_exec` と `maintain_indexes` を再公開し、`cmoc_eval_oracles_impl` 呼び出し直前に monkeypatch 済みの参照を本体へ同期します。

## Read this when

- `src/sub_commands/eval-oracles.py` と `src/sub_commands/eval_oracles.py` の関係を確認したいとき。
- 既存テストや呼び出し側が `eval_oracles` を import する理由、または hyphen を含むファイル名との互換レイヤーを調べたいとき。
- `run_codex_exec` や `maintain_indexes` の monkeypatch が `cmoc_eval_oracles_impl` 実行時に本体へ反映される仕組みを確認したいとき。

## Do not read this when

- `cmoc eval-oracles` の実際の評価処理、Codex 実行、oracle 走査、INDEX 更新などの本体ロジックを調べたいとき。
- CLI 引数解析やサブコマンド登録の入口を調べたいとき。
- oracle 仕様、Structured Output の内容、または `<repo-root>` 側の `INDEX.md` 生成仕様を確認したいとき。

## hash

- 6aff74c72f4708d0a5bbe925651e3859bf2e7c22dd87f1ed86c1c4c8d4a89f7d

# `init.py`

## Summary

- `cmoc init` サブコマンドの本体処理を実装するファイル。
- `repo_root` が未指定の場合は `run_command` に自身を渡し、CLI 実行時の共通ラッパー経由で処理を再実行する。
- `repo_root` が指定された場合は、`.cmoc` が git 追跡対象外になるよう `.gitignore` 設定と tracked file 解除を保証する。
- 初期化前に `.gitignore` と `.cmoc` の作業ツリー状態が clean であることを確認する。
- 初期化によって発生した `.gitignore` や `.cmoc` 関連の変更だけを `Initialize cmoc` メッセージでコミットし、変更がなければその旨を表示する。
- `StepTimer` を使って `init` の各ステップ開始と完了時の時間レポートを出力する。

## Read this when

- `cmoc init` 実行時に `.cmoc` を git 追跡対象外へ初期化する処理の流れを確認したいとき。
- `cmoc init` がどのパスを clean 判定し、どのパスだけをコミット対象にするか調べたいとき。
- `.gitignore` 更新、`.cmoc` の tracked file 解除、初期化コミットの呼び出し元を確認したいとき。
- `cmoc init` の進捗表示や `StepTimer` によるステップ計測の実装箇所を探しているとき。
- `run_command` を使ったサブコマンド本体関数の呼び出しパターンを確認したいとき。

## Do not read this when

- `ensure_cmoc_ignored`、`assert_paths_clean`、`commit_if_changed` の詳細実装を確認したいとき。
- `run_command` の共通 CLI ラッパー、例外処理、repo root 解決の詳細を調べたいとき。
- `StepTimer` の時間計測や表示形式そのものを変更したいとき。
- `cmoc init` 以外の `branch`、`apply`、`eval-oracles`、`merge` サブコマンドの処理を調べたいとき。
- `cmoc init` の正本仕様断片やユーザー向け仕様を確認したいだけのとき。
- テストコードや Fake Codex CLI など、init 実装に対する自動テスト側の構成を調べたいとき。

## hash

- 487d59db1138a4f9667f62ec81112e2f9b657a7fd93664c6f0115a4fe7245644

# `merge.py`

## Summary

- `cmoc merge` サブコマンドの本体処理を実装するファイル。
- 対象リポジトリの検出後、作業ツリーの未コミット変更確認、`.cmoc` の ignore 確認、マージ元 cmoc ブランチの解決、`git merge --no-ff` 実行、必要時の conflict 解消、マージ後のブランチ削除までを担う。
- 明示された cmoc ブランチがない場合は、未マージブランチ一覧から cmoc 命名規則に一致する候補を 1 件だけ自動選択する。
- 通常の git merge が失敗した場合、unmerged path を固定して Codex CLI に conflict marker 解消を依頼し、marker 残存確認、`git add`、`git commit --no-edit` を行う。
- Codex に conflict 解消を依頼するプロンプトでは、`oracles`、`.agents`、`memo` の編集・アクセス禁止範囲や、`git add` / `git commit` 禁止を明示する。
- merge 開始後に例外が発生した場合は、cmoc が merge state をロールバックしないことと手動解決が必要なことを stderr に表示する。

## Read this when

- `cmoc merge` の実行フロー、進捗表示、StepTimer による計測対象を確認したいとき。
- マージ元 cmoc ブランチの自動解決条件や、候補が 0 件または複数件だった場合のエラー内容を調べたいとき。
- `git merge --no-ff` 失敗時に、Codex CLI に conflict marker 解消を依頼する条件や、その後の検証・commit 手順を確認したいとき。
- conflict marker 残存検査、unmerged path 検出、merge commit 作成、マージ元ブランチ削除の実装を変更・テストしたいとき。
- merge conflict 解消用 Codex プロンプトに含める禁止事項、対象ファイル一覧、INDEX メンテナンス例外指定を確認したいとき。
- merge 開始後の例外時に表示される手動解決案内メッセージや、cmoc がロールバックしない方針を確認したいとき。

## Do not read this when

- `cmoc merge` の CLI 引数定義や argparse への登録だけを確認したいとき。
- Codex CLI 呼び出しの共通実装、サンドボックス指定、Structured Output 処理など `run_codex_exec` 側の詳細を調べたいとき。
- `run_git`、`assert_no_uncommitted_changes`、`ensure_cmoc_ignored`、`is_cmoc_branch` など git・リポジトリ共通処理の内部実装だけを確認したいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles` など merge 以外のサブコマンド挙動を調べたいとき。
- `oracles` 配下の正本仕様そのものや、merge 仕様の設計意図を確認したいだけで、Python 実装の制御フローが不要なとき。
- 対象リポジトリ側の個別 conflict 内容や、実際のマージ結果を調査したいとき。

## hash

- e679357fc26f4c6d06e0536d8082ddd0e167b8b486183d97502699e599be74bc

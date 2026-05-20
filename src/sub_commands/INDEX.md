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

- `cmoc apply` サブコマンドの本体処理を実装するファイルです。
- cmoc 作業ブランチ上でのみ実行できることを検査し、oracle 外の未コミット差分を拒否しつつ、`.gitignore`、`.cmoc`、`oracles` の必要な commit を先に整理します。
- `INDEX.md` のメンテナンス、不整合調査、不整合追従、禁止パス検査、変更 commit、作業レポート生成までの apply 全体フローを 4 ステップで制御します。
- oracle ファイルごとに Codex CLI を read-only Structured Output で呼び出し、`discrepancies` 配列として oracle と実装の明確な不整合を収集します。
- 不整合がある場合は Codex CLI を workspace-write で呼び出して実装修正を依頼し、`oracles/` と `.agents/` の変更を禁止したうえで全差分を commit します。
- apply レポートを `.cmoc/reports/apply/<timestamp>.md` に保存し、収束時は終了コード 0、指定回数内に収束しない場合は終了コード 2 を返します。
- 不整合調査用 Structured Output schema、Codex への調査・実装・commit message・レポート生成プロンプト、レポート内容と不整合 JSON の機械的検証処理を含みます。

## Read this when

- `cmoc apply` の実行順序、ブランチ制約、未コミット差分の扱い、INDEX メンテナンス、実装修正ループ、レポート生成までの全体フローを確認したいとき。
- apply がどの条件で `CmocError` を出すか、特に cmoc ブランチ以外での実行、負の `--repeat`、禁止パス変更、レポート不備、Structured Output 不備の扱いを調べたいとき。
- oracle と実装の不整合を Codex CLI に調査させる prompt、Structured Output schema、JSON 検証ロジックを修正または確認したいとき。
- 不整合追従のために Codex CLI を workspace-write で呼ぶ箇所や、`oracles`、`.agents`、`memo` の禁止事項を prompt にどう渡しているか確認したいとき。
- apply 中の commit 方針、`commit_if_changed` と `_commit_all_changes` の使い分け、Codex 生成 commit message の fallback を確認したいとき。
- apply レポートの保存先、必須見出し、収束・未収束ラベル、不整合件数推移の検証条件を確認したいとき。
- `commons.codex`、`commons.indexing`、`commons.repo`、`commons.timing`、`commons.timestamps` との連携点を追いたいとき。

## Do not read this when

- `cmoc apply` 以外のサブコマンド、例えば `init`、`branch`、`merge`、`eval-oracles` の詳細挙動だけを調べたいとき。
- Codex CLI 呼び出しの低レベル実装、JSON パース処理、git コマンド実行、repo root 探索、タイマー、タイムスタンプ生成そのものを調べたいとき。
- oracle の正本仕様本文やルーティング情報を調べたいだけで、apply 実装コードの制御フローが不要なとき。
- `INDEX.md` 自動生成の対象ディレクトリ、除外規則、ハッシュ判定など、目次メンテナンス機能そのものの詳細だけを確認したいとき。
- cmoc のユーザー向け README、インストール方法、PATH 設定、全体ワークフローの説明だけが必要なとき。
- テストコードの配置や pytest の具体的なテスト実装を調べたいとき。

## hash

- 5aef470203fee231156cf378a74b90fe06671233faaeecc1a7e93c6c6f4244c0

# `branch.py`

## Summary

- `cmoc branch` サブコマンドの本体処理を実装するファイル。
- 共通 runner 経由の repo root 解決、作業用ブランチ作成、`.cmoc` の git ignore 保証、作成元 commit の `.cmoc/branch` への記録を行う。
- ブランチ名は `cmoc_<timestamp>` 形式で生成し、衝突時は最大 10 回リトライする。
- 実行中の進捗表示は `branch (1/3)` から `branch (3/3)` までの段階表示と、各ブランチ作成試行の表示で構成される。
- 処理時間の計測と完了時レポートには `StepTimer` を使用する。

## Read this when

- `cmoc branch` の実装フローを確認したいとき。
- 作業用ブランチ名の生成規則や、timestamp 衝突時のリトライ挙動を調べたいとき。
- `cmoc branch` が base commit をどのタイミングで取得し、どこへ保存するか確認したいとき。
- `.cmoc` を git 追跡対象外にする処理が `cmoc branch` 内でいつ呼ばれるか調べたいとき。
- `cmoc branch` の stdout 進捗表示や `StepTimer` による計測箇所を確認したいとき。

## Do not read this when

- `cmoc init`、`cmoc apply`、`cmoc merge`、`cmoc eval-oracles` など他サブコマンドの本体処理を調べたいとき。
- repo root 探索、git 実行、`.cmoc` パス生成、timestamp 生成、時間計測などの共通ユーティリティ実装そのものを調べたいとき。
- `cmoc branch` の正本仕様やユーザー向け仕様だけを確認したいとき。
- 自動テストの構成、Fake Codex CLI、pytest 規約を調べたいとき。
- cmoc を用いて開発する `<repo-root>` 側の oracle や `INDEX.md` 生成仕様を調べたいとき。

## hash

- 3f0f49fc6b3453d7c26dea4e5cb47b8bd0b23b7378f6d77da6eeb182a334eee7

# `eval-oracles.py`

## Summary

- `cmoc eval-oracles` サブコマンドの本体処理を定義する実装ファイル。
- `.cmoc` の ignore 保証、`INDEX.md` メンテナンス、評価対象 oracle ファイルの選択、Codex CLI による評価実行、Markdown レポート保存までの 5 ステップを担う。
- `--full` 指定、cmoc ブランチ判定、削除済み oracle の有無、ブランチ基点コミットに基づいて、部分評価と全体評価を切り替える。
- oracle 評価用プロンプトでは、関連仕様と `INDEX.md` ルーティングを根拠にすること、実装・テスト・設定ファイル参照禁止、`memo` 読み書き禁止、編集禁止を Codex CLI に指示する。
- 評価結果は `.cmoc/reports/eval-oracles/<timestamp>.md` に frontmatter 付き Markdown として保存される。

## Read this when

- `cmoc eval-oracles` の実行フロー、進捗表示、評価対象選択、レポート生成処理を確認したいとき。
- 部分評価と全体評価の切り替え条件を調べたいとき。
- Codex CLI に oracle 評価を依頼するプロンプト内容や `read_only` 実行設定を確認したいとき。
- 評価レポートの保存先、ファイル名、frontmatter、oracle ごとの出力結合形式を確認したいとき。
- `ensure_cmoc_ignored`、`maintain_indexes`、oracle ファイル列挙、ブランチ情報取得、タイマー表示の呼び出し順を追いたいとき。

## Do not read this when

- `cmoc eval-oracles` の CLI 引数定義や argparse 側の登録処理だけを確認したいとき。
- oracle ファイル列挙、cmoc ブランチ判定、`.cmoc` ignore 保証などの共通 repo 操作の詳細実装を調べたいとき。
- `INDEX.md` メンテナンス処理そのものの詳細を調べたいとき。
- Codex CLI 実行ラッパー、ログ保存、リトライ、サンドボックス指定などの共通処理を調べたいとき。
- タイムスタンプ生成や StepTimer の実装詳細を調べたいとき。

## hash

- 29e6ed0b739fd8b701484bda5222be421949287d5cb8662504d58fb846216340

# `eval_oracles.py`

## Summary

- `src/sub_commands/eval_oracles.py` は、ハイフン付きの本命実装ファイル `eval-oracles.py` を通常の Python import から扱いやすくする互換モジュールです。
- `importlib.util.spec_from_file_location` を使って同じディレクトリの `eval-oracles.py` を `sub_commands.eval-oracles` として動的に読み込みます。
- 読み込んだ本命実装モジュールから `cmoc_eval_oracles_impl` と `_evaluation_prompt` を再公開し、テストや他モジュールがアンダースコア区切りの `eval_oracles.py` 経由で参照できるようにします。
- 動的ロードに失敗した場合は `ImportError` を送出します。

## Read this when

- `eval-oracles.py` の実装を Python の通常 import で参照するための互換レイヤーを確認したいとき。
- `cmoc_eval_oracles_impl` や `_evaluation_prompt` が `src/sub_commands/eval_oracles.py` からどのように公開されているか調べたいとき。
- ハイフンを含むファイル名の本命実装を `importlib` で読み込む仕組みを確認したいとき。
- `eval-oracles` サブコマンド関連のテストが `eval_oracles.py` を import している理由を理解したいとき。

## Do not read this when

- `cmoc eval-oracles` の本体処理、CLI 挙動、oracle 評価ロジック、プロンプト生成の詳細を調べたいとき。その場合は本命実装の `src/sub_commands/eval-oracles.py` を読むべきです。
- `cmoc eval-oracles` の正本仕様を確認したいとき。その場合は `oracles/INDEX.md` から該当する仕様断片へルーティングしてください。
- 他のサブコマンドや共通 CLI 処理の実装を調べたいとき。
- ファイル名互換や再公開の仕組みではなく、実際の評価結果生成、ログ保存、Codex CLI 呼び出しなどの処理内容を確認したいとき。

## hash

- f7b3b8fed670ac7d3b700362e0de934019a514fb8f5c3b2f06b762b6eabf01c7

# `init.py`

## Summary

- `cmoc init` サブコマンドの本体処理を定義する実装ファイル。
- `cmoc_init_impl` は、直接呼び出し時に共通 runner へ処理を委譲し、`repo_root` 解決と共通エラー整形を受ける。
- 初期化処理として、対象リポジトリで `.cmoc` が git 追跡対象外になるよう `.gitignore` ルールや tracked file 解除を保証する。
- 初期化で発生した `.gitignore` や git index の変更だけをコミットし、変更がない場合はその旨を表示する。
- `StepTimer` により `init` の各ステップ開始と最終的な経過時間レポートを行い、stdout に 2 段階の進捗を表示する。

## Read this when

- `cmoc init` の実装本体を確認したいとき。
- `.cmoc` を git 追跡対象外にする処理の呼び出し順序を確認したいとき。
- `cmoc init` が `.gitignore` や git index の変更をどの条件でコミットするか調べたいとき。
- `cmoc init` の stdout 進捗表示、ステップ名、完了時の時間レポートを確認したいとき。
- `cmoc_init_impl` をテストから直接呼び出す際の `repo_root` 引数の扱いを確認したいとき。

## Do not read this when

- CLI エントリーポイントで `init` サブコマンドがどう登録されるかだけを調べたいとき。
- `.cmoc` ignore ルールの具体的な `.gitignore` 編集や git 操作の詳細実装を調べたいとき。
- 共通 runner の repo root 解決、例外処理、終了ステータス整形の詳細を調べたいとき。
- タイマーや経過時間表示の内部実装だけを調べたいとき。
- `cmoc branch`、`cmoc apply`、`cmoc eval-oracles`、`cmoc merge` など他サブコマンドの挙動を調べたいとき。

## hash

- 253e20a5cd3777cd63492c0bac7fb6ed2c0dc7fdefeb5135264b7912c81b9a7a

# `merge.py`

## Summary

- `cmoc merge` の本体処理を実装するモジュール。
- 作業ツリーの未コミット変更確認、`.cmoc` の ignore 保証、merge 元 cmoc ブランチの解決、`git merge --no-ff`、安全なブランチ削除、ステップ時間レポートまでを担当する。
- merge conflict が発生した場合は、unmerged path を取得して Codex CLI に conflict marker 解消を依頼し、marker 残存確認、`git add`、`git commit --no-edit` までを行う。
- 自動解決できる cmoc ブランチ候補が 1 件でない場合、または conflict 解消後も marker や unmerged path が残る場合は `CmocError` で手動対応を促す。
- conflict marker 検出は git 管理対象ファイル全体を走査し、`<<<<<<<`、`=======`、`>>>>>>>` の残存を確認する。

## Read this when

- `cmoc merge` サブコマンドの実行フロー、進捗表示、前提条件チェック、merge 元ブランチ解決の実装を確認したいとき。
- 未マージの cmoc ブランチを `git branch --no-merged` から自動解決する条件や、明示指定が必要になるケースを調べたいとき。
- `git merge --no-ff` 失敗時に Codex CLI を使って conflict marker を解消する処理を確認したいとき。
- conflict 解消後の marker 残存検出、unmerged path 確認、`git add`、`git commit --no-edit` の責務分担を調べたいとき。
- merge 後に source branch を `git branch -d` で削除し、削除できない場合は warning に留める挙動を確認したいとき。
- merge state が残る可能性がある例外時の stderr メッセージや、手動解決案内の扱いを確認したいとき。

## Do not read this when

- `cmoc merge` の CLI 引数定義や argparse へのサブコマンド登録だけを調べたいとき。
- `cmoc init`、`cmoc branch`、`cmoc apply`、`cmoc eval-oracles` など、merge 以外のサブコマンド仕様や実装を調べたいとき。
- Codex CLI 呼び出し共通処理、ログ保存、Structured Output、リトライ方針など `run_codex_exec` の内部実装を調べたいとき。
- git コマンド実行ラッパー、repo root 解決、共通エラー整形、StepTimer の内部仕様だけを調べたいとき。
- merge conflict 解消プロンプトの文言ではなく、oracles 側の正本仕様やユーザー向けワークフロー説明だけを確認したいとき。
- INDEX.md 自動生成全体の対象ディレクトリ、除外規則、ハッシュ管理、処理順序を調べたいとき。

## hash

- 512711fc123c5f5655dc4f656b008c8daae9a85ab4f5a0f85b38ed15891cbd21

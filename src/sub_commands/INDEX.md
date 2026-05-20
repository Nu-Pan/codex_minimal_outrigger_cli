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
- cmoc 作業ブランチ上であることを確認し、oracle 外の未コミット差分を拒否したうえで、`.cmoc` ignore 保証差分と oracle 差分を必要に応じて commit します。
- `INDEX.md` メンテナンス、不整合調査、不整合追従、禁止パス検査、変更 commit、作業レポート生成までの apply 全体フローを 4 ステップで制御します。
- oracle ファイルごとに Codex CLI を read-only Structured Output モードで呼び出し、`discrepancies` JSON schema と追加の Python バリデーションで不整合調査結果を検証します。
- 検出された不整合は workspace-write の Codex CLI に修正させ、`oracles/` と `.agents/` への差分を禁止し、変更があれば Codex 生成の 1 行 commit message で commit します。
- apply レポートを `.cmoc/reports/apply/<timestamp>.md` に保存し、必須見出し・収束区分・不整合件数推移・全変更内容カテゴリ要約を検証してから、収束時は終了コード 0、指定回数内に収束しない場合は終了コード 2 を返します。

## Read this when

- `cmoc apply` の実行順序、ブランチ制約、未コミット差分の扱い、INDEX メンテナンス、実装修正ループ、レポート生成までの全体フローを確認したいとき。
- `--repeat` の反復上限、負の値の拒否、収束時と未収束時の終了コードを調べたいとき。
- apply がどの条件で `CmocError` を出すか、特に cmoc ブランチ以外での実行、負の `--repeat`、禁止パス変更、レポート不備、Structured Output 不備の扱いを調べたいとき。
- 不整合調査で Codex CLI に渡す prompt、read-only 実行、Structured Output schema、`discrepancies` payload の検証ロジックを確認したいとき。
- 不整合追従作業で Codex CLI に渡す prompt、workspace-write 実行、`oracles`・`.agents`・`memo` の禁止指定を確認したいとき。
- apply 中の commit 方針、`commit_if_changed` と `_commit_all_changes` の使い分け、Codex 生成 commit message の fallback を確認したいとき。
- apply レポートの保存先、必須見出し、収束・未収束ラベル、不整合件数推移の検証条件を確認したいとき。

## Do not read this when

- `cmoc apply` 以外のサブコマンド、例えば `init`、`branch`、`merge`、`eval-oracles` の詳細挙動だけを調べたいとき。
- CLI の引数定義や Typer のコマンド登録だけを確認したいとき。
- Codex CLI 呼び出しの共通実装、JSON パース、ログ保存、リトライなど、`commons.codex` 側の詳細だけを調べたいとき。
- git 操作、cmoc ブランチ判定、oracle ファイル列挙、`.cmoc` ignore 保証など、`commons.repo` 側の共通関数の内部実装だけを調べたいとき。
- `INDEX.md` 自動生成・ハッシュ管理・除外規則の共通仕様や実装だけを調べたいとき。
- oracle の正本仕様本文やルーティング情報を調べたいだけで、apply 実装コードの制御フローが不要なとき。
- apply のテストケースや monkeypatch 方針だけを調べたいとき。

## hash

- 91277899ac4cb4c3b4ac4070006439b9d7c5de2bedcfd85ffcdc87d37fb02748

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

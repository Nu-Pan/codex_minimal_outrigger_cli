
# Doctor Preprocess

## 概要

- doctor preprocess では `<repo-root>` が cmoc を正常に実行可能な状態か検証し、可能な限り修復を試みる
- doctor preprocess は各サブコマンドの本命処理の開始前に必ず実行される
- 各サブコマンドに共通して必要な検証・修復は、個別サブコマンドではなく doctor preprocess の責務とする
- 各サブコマンド固有の事前条件は、doctor preprocess が正常終了した後に検証する
- 修復困難な場合はその場で cmoc をエラー終了する

## 実行手順

1. `<work-root>/.cmoc/local` が git 追跡対象外であることを保証する
2. `<work-root>/.agents` が git 追跡対象であることを保証する
3. cmoc managed ollama が利用可能であることを保証する
4. external model provider が利用可能であることを保証する
5. ここまでの作業で発生した差分を git commit する

## 「`<repo-root>/.cmoc/local` が git 追跡対象外であることを保証する」の詳細

### 検証

- 必要な操作
    - `/.cmoc/local/` を `<work-root>/.gitignore` に追加する
    - 既に tracked な `<work-root>/.cmoc/local` ツリー内ファイルは追跡を解除する (e.g. `git rm --cached`)
    - `<work-root>/.cmoc` ツリー内ファイルは追跡を解除する (e.g. `git rm --cached`)
- `<repo-root>/.cmoc/local` 追跡対象外保証の完了判定は、以下の両方を満たすこととする
    - `git ls-files -- <repo-root>/.cmoc/local` の出力が空である
    - `git check-ignore -q <repo-root>/.cmoc/local/.__cmoc_ignore_probe__` が成功する
        - これは `<work-root>/.cmoc/local` 配下に将来作成されるファイルが git ignore 対象になることを確認するための probe path である
    - よって、実ファイルを作成する必要はない

### 修復

- `<work-root>/.gitignore` が存在しなければ作成する
- `<work-root>/.gitignore` に `/.cmoc/local/` が無ければ追加する
- `<work-root>/.cmoc/local` ツリー内に tracked file があれば、working tree 上の実ファイルを残したまま git index から除外する
- 修復後も完了判定を満たさない場合はエラー終了する

## 「`<work-root>/.agents` が git 追跡対象であることを保証する」の詳細

### 検証

- 必要な操作
    - `<work-root>/.agents` が存在しなければ作成する
    - `<work-root>/.agents` が空ディレクトリならば `<work-root>/.agents/.gitkeep` を作成する
    - `<work-root>/.agents` ツリー内 git 追跡対象外ならば `<work-root>/.agents/.gitkeep` を git 追跡対象に追加する
- 必要な理由
    - `<work-root>/.agents` は agent 操作禁止領域なので、差分が出る余地をなくしたい
    - なので、最初から作っておく

### 修復

- `<work-root>/.agents` が存在しなければ作成する
- `<work-root>/.agents` が空ディレクトリならば `<work-root>/.agents/.gitkeep` を作成する
- `<work-root>/.agents` ツリー内に tracked file が無い場合は `<work-root>/.agents/.gitkeep` を git index に追加する
- 修復後も `<work-root>/.agents` ツリー内に tracked file が無い場合はエラー終了する

## 「cmoc managed ollama が利用可能であることを保証する」の詳細

- `ensure_cmoc_managed_ollama` の呼び出しを、検証・修復とする

## 「external model provider が利用可能であることを保証する」の詳細

### 検証

- `CodexModelSpec.model_provider` の設定が external model provider である場合、`CodexModelSpec.model` が cmoc から接続可能である事を確認する

### 修復

- cmoc の外側の話なので諦める

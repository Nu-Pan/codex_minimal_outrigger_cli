
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
3. ollama が SLM をサーブ可能であることを保証する
4. ここまでの作業で発生した差分を git commit する

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


## 「ollama が SLM をサーブ可能であることを保証する」の詳細

### 検証

- SLM backend を利用する可能性があるサブコマンドの共通前提として、ollama が cmoc から接続可能であることを確認する
- cmoc が利用する SLM モデル名が定義されている場合、そのモデルを ollama が serve 可能であることを確認する
- SLM モデル名が未定義の場合の扱いは `<cmoc-root>/oracle/doc/app_spec/ollama_slm_server.md` を正本とする

### 修復

- ollama が未起動で、cmoc が起動可能な場合は起動する
- 必要な SLM モデルが未取得で、cmoc が取得可能な場合は取得する
- 修復後も cmoc から SLM を利用できない場合はエラー終了する

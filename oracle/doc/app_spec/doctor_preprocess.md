
# Doctor Preprocess

## 概要

- doctor preprocess では `{{repo-root}}` が cmoc を正常に実行可能な状態か検証し、可能な限り修復を試みる
- doctor preprocess は各サブコマンドの本命処理の開始前に必ず実行される
- 各サブコマンドに共通して必要な検証・修復は、個別サブコマンドではなく doctor preprocess の責務とする
- 各サブコマンド固有の事前条件は、doctor preprocess が正常終了した後に検証する
- 修復困難な場合はその場で cmoc をエラー終了する

## 実行手順

1. `{{work-root}}/.cmoc/gu` が git 追跡対象外であることを保証する
2. `{{work-root}}/.agents` が git 追跡対象であることを保証する
3. `{{work-root}}/.cmoc/gt/ar/config.json` が git 追跡対象である事を保証する
4. `{{work-root}}/.cmoc/gt/ar/realization/refactor/state.json` が git 追跡対象であり、schema と entry 集合が同期済みであることを保証する
5. `CmocConfig.cmoc_managed_ollama_service_launch_behavior` に従って、cmoc managed ollama service の起動保証処理を扱う
6. ここまでの作業で発生した差分を git commit する

## 「`{{repo-root}}/.cmoc/gu` が git 追跡対象外であることを保証する」の詳細

### 検証

- 必要な操作
    - `/.cmoc/gu/` を `{{work-root}}/.gitignore` に追加する
    - 既に tracked な `{{work-root}}/.cmoc/gu` ツリー内ファイルは追跡を解除する (e.g. `git rm --cached`)
- `{{repo-root}}/.cmoc/gu` 追跡対象外保証の完了判定は、以下の両方を満たすこととする
    - `git ls-files -- {{repo-root}}/.cmoc/gu` の出力が空である
    - `git check-ignore -q {{repo-root}}/.cmoc/gu/.__cmoc_ignore_probe__` が成功する
        - これは `{{work-root}}/.cmoc/gu` 配下に将来作成されるファイルが git ignore 対象になることを確認するための probe path である
    - よって、実ファイルを作成する必要はない

### 修復

- `{{work-root}}/.gitignore` が存在しなければ作成する
- `{{work-root}}/.gitignore` に `/.cmoc/gu/` が無ければ追加する
- `{{work-root}}/.cmoc/gu` ツリー内に tracked file があれば、working tree 上の実ファイルを残したまま git index から除外する
- 修復後も完了判定を満たさない場合はエラー終了する

## 「`{{work-root}}/.agents` が git 追跡対象であることを保証する」の詳細

### 検証

- 必要な操作
    - `{{work-root}}/.agents` が存在しなければ作成する
    - `{{work-root}}/.agents` が空ディレクトリならば `{{work-root}}/.agents/.gitkeep` を作成する
    - `{{work-root}}/.agents` ツリー内 git 追跡対象外ならば `{{work-root}}/.agents/.gitkeep` を git 追跡対象に追加する
- 必要な理由
    - `{{work-root}}/.agents` は agent 操作禁止領域なので、差分が出る余地をなくしたい
    - なので、最初から作っておく

### 修復

- `{{work-root}}/.agents` が存在しなければ作成する
- `{{work-root}}/.agents` が空ディレクトリならば `{{work-root}}/.agents/.gitkeep` を作成する
- `{{work-root}}/.agents` ツリー内に tracked file が無い場合は `{{work-root}}/.agents/.gitkeep` を git index に追加する
- 修復後も `{{work-root}}/.agents` ツリー内に tracked file が無い場合はエラー終了する

## 「`{{work-root}}/.cmoc/gt/ar/config.json` が git 追跡対象である事を保証する」の詳細

### 検証

- `{{work-root}}/.cmoc/gt/ar/config.json` が存在していること
- `{{work-root}}/.cmoc/gt/ar/config.json` が git 追跡対象であること

### 修復

- `{{work-root}}/.cmoc/gt/ar/config.json` が存在しなければ作成する
- `{{work-root}}/.cmoc/gt/ar/config.json` を git 追跡対象に追加する

## 「refactor state が git 追跡対象であり、schema と entry 集合が同期済みであることを保証する」の詳細

### 検証

- `{{work-root}}/.cmoc/gt/ar/realization/refactor/state.json` が存在していること
- 同 file が git 追跡対象であること
- JSON のトップレベルが object であり、各 key と value が `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の refactor state 仕様を満たすこと
- 同期完了時点で、entry が全 oracle file と全 realization file の和集合に過不足なく対応すること
- 現在の file の SHA256 が最後に調査した hash と異なる entry で `investigation_required=true` であること

### 修復

- file が存在しなければ、空の object `{}` を保存する
- file を git 追跡対象に追加する
- 新規 file の entry 作成、削除 file の entry 削除、および hash 変更時の調査要求設定により entry 集合を同期する
- file が存在するものの schema を満たさない場合は、既存の調査履歴を破棄せずエラー終了する

### `cmoc run join` での同期時点

- active run の kind が `realization_refactor` の場合、merge 前の doctor preprocess では追跡状態と schema だけを検証し、entry 集合の同期を merge 後まで遅延する。
- これは session branch と run branch が同じ refactor state を独立に更新して merge conflict を起こすことを避けるためである。
- merge 後は kind にかかわらず、最終的な session tree に対して entry 集合を同期する。

## 「cmoc managed ollama service の起動保証処理を扱う」の詳細

- 起動保証処理を実行するかバイパスするかの条件は、`CmocConfig.cmoc_managed_ollama_service_launch_behavior` のコメントを正本とする
- 起動保証処理で保証するサービスとモデルの状態は、`{{cmoc-root}}/oracle/doc/app_spec/cmoc_managed_ollama.md` を正本とする

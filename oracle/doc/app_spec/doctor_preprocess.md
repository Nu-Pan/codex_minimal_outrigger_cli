# Doctor Preprocess

## 概要

- doctor preprocess は、`{{repo-root}}` で cmoc を正常に実行できるか検証し、可能な限り修復を試みる
- doctor preprocess は各サブコマンドの本命処理の開始前に必ず実行される
- 各サブコマンドに共通して必要な検証・修復は、個別サブコマンドではなく doctor preprocess の責務とする
- 各サブコマンド固有の事前条件は、doctor preprocess が正常終了した後に検証する
- git working tree または staging area の clean 状態は、doctor preprocess では検査しない。clean 状態を必要とするサブコマンドが、doctor preprocess の正常終了後に個別仕様に従って検査する
- 修復困難な場合はその場で cmoc をエラー終了する
- feedback MCP reporter/client の利用不能だけは本命 workload を妨げないため、本書の reporter 固有規則を優先して degraded warning とする

## 実行手順

1. `{{repo-root}}/.cmoc/gu` が git 追跡対象外であることを保証する
2. `{{work-root}}/.agents` が git 追跡対象であることを保証する
3. `{{work-root}}/.cmoc/gt/config.json` が git 追跡対象であることを保証する
4. `{{work-root}}/.cmoc/gt/realization/refactor/state.json` が git 追跡対象であり、schema と entry 集合が同期済みであることを保証する
5. cmoc が管理する local stdio MCP reporter/client の利用可能性と collector との protocol compatibility を事前検証する
6. ここまでの作業で発生した tracked 差分を git commit する

## 「`{{repo-root}}/.cmoc/gu` が git 追跡対象外であることを保証する」の詳細

### 検証

- 非追跡保証は `.cmoc/gu` の一部用途だけではなく、feedback の pending observation、active state、report cut、checkpoint、および Markdown report を含むツリー全体と、将来作成される全 descendant に適用する
- `{{repo-root}}/.cmoc/gu` 追跡対象外保証の完了判定は、以下の両方を満たすこととする
    - `git ls-files -- {{repo-root}}/.cmoc/gu` の出力が空である
    - `git check-ignore -q {{repo-root}}/.cmoc/gu/.__cmoc_ignore_probe__` が成功する
        - これは `{{repo-root}}/.cmoc/gu` 配下に将来作成されるファイルが git ignore 対象になることを確認するための probe path である
        - この probe のために実ファイルを作成する必要はない

### 修復

- `{{repo-root}}/.gitignore` が存在しなければ作成する
- `{{repo-root}}/.gitignore` に `/.cmoc/gu/` が無ければ追加する
- `{{repo-root}}/.cmoc/gu` ツリー内に tracked file があれば、working tree 上の実ファイルを残したまま git index から除外する
- 修復後も完了判定を満たさない場合はエラー終了する

## 「`{{work-root}}/.agents` が git 追跡対象であることを保証する」の詳細

agent が書き込めない `.agents` は、doctor preprocess があらかじめ用意する。

### 検証

- `{{work-root}}/.agents` が存在すること
- `{{work-root}}/.agents` ツリー内に git 追跡対象 file が 1 件以上あること

### 修復

- `{{work-root}}/.agents` が存在しなければ作成する
- `{{work-root}}/.agents` ツリー内に tracked file がない場合は `{{work-root}}/.agents/.gitkeep` を用意し、git index に追加する
- 修復後も `{{work-root}}/.agents` ツリー内に tracked file がない場合はエラー終了する

## 「`{{work-root}}/.cmoc/gt/config.json` が git 追跡対象であることを保証する」の詳細

### 検証

- `{{work-root}}/.cmoc/gt/config.json` が存在していること
- `{{work-root}}/.cmoc/gt/config.json` が git 追跡対象であること

### 修復

- `{{work-root}}/.cmoc/gt/config.json` が存在しなければ作成する
- `{{work-root}}/.cmoc/gt/config.json` を git 追跡対象に追加する

## 「refactor state が git 追跡対象であり、schema と entry 集合が同期済みであることを保証する」の詳細

### 検証

- `{{work-root}}/.cmoc/gt/realization/refactor/state.json` が存在していること
- 同 file が git 追跡対象であること
- 同 file が `{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「保存先と JSON schema」を満たすこと
- entry 集合と調査要求が、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/realization_refactor.md` の「entry 集合の同期」が定める同期完了時点の条件を満たすこと

### 修復

- file が存在しなければ、空の object `{}` を保存する
- file を git 追跡対象に追加する
- 同文書の「entry 集合の同期」に従って entry 集合と調査要求を同期する
- file が存在するものの schema を満たさない場合は、既存の調査履歴を破棄せずエラー終了する

### editing run の join での同期時点

- active run の kind が `realization_refactor` または `feedback_report` の場合、merge 前の doctor preprocess では追跡状態と schema だけを検証し、entry 集合の同期を merge 後まで遅延する。
- これは session branch と run branch が同じ refactor state を独立に更新して merge conflict を起こすことを避けるためである。
- merge 後は kind にかかわらず、最終的な session tree に対して entry 集合を同期する。

## feedback MCP reporter/client の事前検証

- reporter の agent-facing interface と期待する protocol は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「MCP interface」と「collector と transport」を正本とする。
- doctor preprocess の検査は、次の事前判定に必要な範囲に限る。
    - cmoc が管理する local stdio MCP reporter/client を call 開始時に起動できること
    - 同 reporter/client と collector の protocol に互換性があること
- doctor preprocess は repo-local reporter executable を作成、copy、配置、修復、または version command で検証してはならない。
- reporter の利用不能または protocol 不一致を検出した場合は、`feedback.reporter_unavailable` の構造化 event と warning を記録する。その invocation の agent 自己申告を degraded として、本命処理を続ける。
- reporter の利用不能を理由に sandbox、file access mode、Structured Output schema、個別 agent call の完了条件、または Codex workload の retry 判定を変更してはならない。

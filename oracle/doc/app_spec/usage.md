# cmoc 使用方法

## 呼び出し方法

- `{{cmoc-root}}/bin` を環境変数 `PATH` に追加し、`cmoc` コマンドで呼び出す。

## 最初に 1 回だけ行うこと

1. 人間が `cmoc doctor` を呼び出す。

## 想定 workflow

1. 人間が作業対象の `{{local-branch}}` へ移動する。
2. 人間が `cmoc session fork` を呼び出す。
    - cmoc は現在の branch を `{{cmoc-session-home-branch}}` として記録する。
    - cmoc は `{{cmoc-session-branch}}` を作成して checkout する。
3. 短い仕様変更・実装変更 loop を繰り返す。
    1. 必要に応じて `cmoc oracle investigation` で read-only の調査を行う。
    2. 人間が oracle file を直接編集するか、`cmoc oracle edit fork` で編集 run を開始する。
        - fork を使用した場合は結果を確認し、`cmoc run join` で取り込むか `cmoc run abandon` で破棄する。
    3. 人間が `cmoc oracle review` を呼び出し、必要なら oracle file を修正する。
    4. 人間が oracle file の変更を commit する。
    5. 人間が `cmoc realization apply fork` を呼び出す。
        - cmoc は前回 join 済み apply から現在までの oracle commit 差分を注入し、run worktree 上の `codex exec` 1 回でリポジトリ全体の realization を追従させる。
    6. 人間が `cmoc run join` で apply run を取り込むか、`cmoc run abandon` で破棄する。
    7. 人間が現状の実装で問題ないと判断するまで繰り返す。
4. 必要に応じて、ファイル単位の網羅的な追従を行う。
    1. 人間が `cmoc realization refactor fork` を呼び出す。
        - cmoc は refactor state の調査要求に従い、差分情報を渡さずに 1 file ずつ調査する。
        - 自然完了または `Ctrl+C` による整合した中断まで処理する。
    2. 人間が `cmoc run join` で確定済み成果物を取り込むか、`cmoc run abandon` で破棄する。
    3. 調査要求が残っている場合は、join 後に新しい `cmoc realization refactor fork` を開始する。
5. 人間が `{{cmoc-session-branch}}` 上で `cmoc session join` を呼び出す。
    - cmoc は `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge する。

## workload の使い分け

- realization apply は、直近の oracle 変更を短い loop で素早く realization へ反映するときに使う。
- realization refactor は、変更差分に引っ張られず、全 oracle file と realization file の調査要求を収束させるときに使う。
- oracle edit、realization apply、realization refactor の編集 run は共通の明示的 fork/join lifecycle を使う。

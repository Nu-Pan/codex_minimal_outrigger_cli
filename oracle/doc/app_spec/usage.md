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
    2. 人間が oracle file を直接編集するか、clean な `{{cmoc-session-branch}}` 上で `cmoc oracle edit` の TUI を起動する。
        - TUI の変更は未コミットで残る。人間が差分を確認し、必要なら追加修正する。
    3. 人間が `cmoc oracle review` を呼び出し、必要なら oracle file を修正する。
    4. 人間が oracle file の変更を commit または破棄する。破棄した場合は必要に応じて loop の先頭へ戻る。
    5. 人間が `cmoc realization apply fork` を呼び出す。
        - cmoc は前回 join 済み apply から現在までの oracle commit 差分を注入し、run worktree 上の `codex exec` 1 回でリポジトリ全体の realization を追従させる。
    6. 人間が `cmoc run join` で apply run を取り込むか、`cmoc run abandon` で破棄する。
    7. 人間が現状の実装で問題ないと判断するまで繰り返す。
4. 必要に応じて、ファイル単位の網羅的な追従を行う。
    1. 人間が `cmoc realization refactor fork` を呼び出す。
        - cmoc は refactor state の調査要求に従い、差分情報を渡さずに 1 file ずつ調査する。
        - unresolved target は current fork 内で保留し、それ以外の調査要求がなくなるまで処理する。
        - `natural_completion` による完全な自然完了、`completed_with_unresolved` による unresolved 付き完了、または `Ctrl+C` による整合した中断まで処理する。
    2. 人間が `cmoc run join` で確定済み成果物を取り込むか、`cmoc run abandon` で破棄する。
    3. 調査要求が残っている場合は、join 後に新しい `cmoc realization refactor fork` を開始する。
5. 人間が `{{cmoc-session-branch}}` 上で `cmoc session join` を呼び出す。
    - cmoc は `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge する。

## workload の使い分け

- realization apply は、直近の oracle 変更を短い loop で素早く realization へ反映するときに使う。
- realization refactor は、変更差分に引っ張られず、全 oracle file と realization file の調査要求を収束させるときに使う。
- oracle edit は main worktree 上で oracle file を直接編集する対話型 TUI であり、run lifecycle を使わない。
- realization apply と realization refactor の編集 run は共通の明示的 fork/join lifecycle を使う。

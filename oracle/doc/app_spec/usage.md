# cmoc 使用方法

## エンドユーザーが cmoc を呼び出す方法

- `{{cmoc-root}}/bin` を環境変数 `PATH` に追加し、`cmoc` コマンドで呼び出す。

## 最初に 1 回だけ行うこと

1. 人間が `cmoc doctor` を呼び出す。

## 想定 workflow

1. 人間が `{{local-branch}}` に移動する。
    - e.g. `issue/123-fix-login`
    - `main` / `master` である必要はない。
2. 人間が `cmoc session fork` を呼び出す。
    - cmoc は現在の branch を `{{cmoc-session-home-branch}}` として記録する。
    - cmoc は `{{cmoc-session-branch}}` を作成して checkout する。
3. 短い仕様変更・実装変更ループを繰り返す。
    1. 人間が、やってほしいことを `{{repo-root}}/oracle` に反映する。
        - 必要に応じて `cmoc oracle investigation`, `cmoc oracle edit` を使う。
    2. 人間が `cmoc oracle review` を呼び出し、必要なら oracle file を修正する。
    3. 人間が oracle file の変更を commit する。
    4. 人間が `cmoc realization apply fork` を呼び出す。
        - cmoc は前回 join 済み apply から現在までの commit 差分を注入し、TUI 1 セッションでリポジトリ全体の realization を追従させる。
        - 作業結果は `{{cmoc-realization-apply-branch}}` に commit される。
    5. 人間が `cmoc realization apply join` を呼び出す。
        - cmoc は apply branch を `{{cmoc-session-branch}}` へ merge する。
    6. 人間が現状の実装で問題ないと判断するまで繰り返す。
4. 必要に応じて、ファイル単位の網羅的な追従を行う。
    1. 人間が `cmoc realization refactor fork` を呼び出す。
        - cmoc は refactor state にある全候補 file を、差分情報を渡さずに 1 file ずつ調査する。
        - `Ctrl+C` で中断しても、次回の同じ fork で既存 branch から再開できる。
    2. refactor state が空になるまで fork を続行または再開する。
    3. 人間が `cmoc realization refactor join` を呼び出す。
        - cmoc は refactor branch と空になった refactor state を `{{cmoc-session-branch}}` へ merge する。
5. 人間が `{{cmoc-session-branch}}` 上で `cmoc session join` を呼び出す。
    - cmoc は `{{cmoc-session-branch}}` を `{{cmoc-session-home-branch}}` へ merge する。

## workload の使い分け

- `cmoc realization apply` は、直近の oracle 変更を短い loop で素早く realization へ反映するときに使う。
- `cmoc realization refactor` は、変更差分に引っ張られず、全候補 file の追従状況を収束させるときに使う。
- `cmoc apply ...` は廃止済みであり、使用しない。

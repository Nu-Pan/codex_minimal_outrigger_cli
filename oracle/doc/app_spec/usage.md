# cmoc 使用方法

## エンドユーザーが cmoc を呼び出す方法

- `<cmoc-root>/bin` を環境変数 `PATH` に追加し `cmoc` コマンドで呼び出すものとする

## 最初に 1 回だけのおまじない

1. 人間が `cmoc init` を呼び出す

## 想定ワークフロー

1. 人間が `<local-branch>` に移動する
   - 例: `issue/123-fix-login`
   - `main` / `master` である必要はない
2. 人間が `cmoc session fork` を呼び出す
   - cmoc は現在のブランチを `<cmoc-session-home-branch>` として記録する
   - cmoc は `<cmoc-session-branch>` を作成して checkout する
3. 記述・実装ループ
   1. 人間がやってほしいと思っている事を `<repo-root>/oracle` に反映する
   2. 人間が `cmoc review oracle` を呼び出して、レビューレポートを読む
   3. 人間が必要に応じて `<repo-root>/oracle` を修正する
   4. 人間が `<repo-root>/oracle` の変更を commit する
   5. 人間が `cmoc apply fork` を呼び出す
      - cmoc は、呼び出された時点の `<oracle-snapshot-commit>` 上の `<run-root>/oracle` を正本として、実装を追従させる作業を行う
      - 実装追従作業は apply worktree 上で長時間作業かけて行われる
      - 通常系においては、 `cmoc apply fork` が完了した時点で、作業結果が `<cmoc-apply-branch>` にコミットされている
      - `cmoc apply fork` 実行中も、人間は `<cmoc-session-branch>` 側で `<repo-root>/oracle` の改訂を進めてよいが、その内容は既に実行を開始した `cmoc apply fork` には反映されない（よって、普通はもう１周必要）
   6. 人間が `cmoc apply join` を呼び出す
      - cmoc は `<cmoc-apply-branch>` を `<cmoc-session-branch>` へマージする
   5. 人間が現状の実装で問題なしと判断したら、ループ終了
4. 人間が `<cmoc-session-branch>` 上で `cmoc session join` を呼び出す
   - cmoc は `<cmoc-session-branch>` を `<cmoc-session-home-branch>` へマージする

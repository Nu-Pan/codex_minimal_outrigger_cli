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
   1. 人間がやってほしいと思っている事を `/oracles` に反映する
   2. 人間が `cmoc eval-oracles` を呼び出して、評価レポートを読む
   3. 人間が必要に応じて `/oracles` を修正する
   4. 人間が `/oracles` の変更を commit する
   5. 人間が `cmoc apply fork` を呼び出す
      - `cmoc apply fork` は専用 apply worktree 上で長時間作業を行う
      - apply 実行中も、人間は `<cmoc-session-branch>` 側で `/oracles` の改訂を進めてよい
      - 実行中の apply は開始時点の oracle snapshot に対する作業である
   6. `<cmoc-apply-branch>` を `<cmoc-session-branch>` に取り込む
      - この取り込み方法は別仕様または通常の git merge に従う
   7. 人間が現状の実装で問題なしと判断したら、ループ終了
4. 人間が `<cmoc-session-branch>` 上で `cmoc session join` を呼び出す
   - cmoc は session metadata に記録された `<cmoc-session-home-branch>` へ session を merge する

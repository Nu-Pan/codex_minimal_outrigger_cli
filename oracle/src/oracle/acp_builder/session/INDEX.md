# `join`

## Summary
- session join で競合が起きた際に使う agent call の prompt と起動条件を組み立てる入口。session と home の merge 前 HEAD、home 側の進行中 worktree、編集範囲を共通の競合解消 prompt に渡す。
- 共通の競合解消方針を定義する場所ではなく、session join 固有の commit、作業場所、書き込み範囲、preflight の選択を担う。

## Read this when
- session branch を home branch に統合する競合解消 call の prompt、アクセス範囲、作業場所、起動設定を確認・変更するとき。
- oracle と realization の両方を扱う書き込み範囲や、merge 進行中に indexing preflight を省略する設定を確認するとき。

## Do not read this when
- run の成果を session に統合する競合解消 call を調べるとき。run join 固有の書き込み範囲や追加入力は、その call の構築箇所を確認する。
- 両 join に共通する競合解消 prompt や policy、競合時の判断基準を調べるとき。共通 prompt の構築箇所や正本仕様を直接確認する。

## hash
- 80369de4088bc3f5bb5de1ff7d969437a64a6a12c3b3bc7c7bb36cd1d60d9381

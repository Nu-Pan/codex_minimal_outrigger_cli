# `conflict_resolution.py`

## Summary
- run の変更を session へ統合する競合解消 agent call の構築を担い、merge 対象 worktree、commit、閲覧範囲、realization の編集境界を共通 prompt に渡す。
- 自動 join では封印済み report cut の参照と採用結果を維持するための指示を追加し、必要なマージ調整と検証を call に組み込む。

## Read this when
- 進行中の run から session への merge について、競合解消 call の入力や編集境界を確認するとき。
- 自動 join が封印済み結果をどう参照し、統合時に維持するかを確認するとき。

## Do not read this when
- session から home への統合用 call を調べるときは、その専用 builder を読む。
- run join と session join に共通する競合取得・統合 prompt の方針を調べるときは、共通 prompt builder を読む。

## hash
- cbd1d81583ce534863b96232eb068052c7c91d792115a3066609d48fccec89da

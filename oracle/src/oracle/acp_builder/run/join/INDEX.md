# `conflict_resolution.py`

## Summary
- run join の競合解消 agent call を組み立てる定義で、merge 先 worktree、編集範囲、起動設定を選びます。sealed feedback report が渡された場合は、採用結果を保つための追加指示も組み込みます。
- 共通の競合解消方針ではなく、run join 用の call 構成を調べる入口です。

## Read this when
- run の変更を session に統合する際の競合解消 call の入力、編集範囲、起動設定を追跡または変更するとき。
- feedback report の自動 join で、sealed report を競合解消 agent に渡す方法を確認するとき。

## Do not read this when
- session を home に統合する競合解消 call の構成を調べるときは、session join 用の call 定義を参照してください。
- run と session に共通する競合解消の指示や判断基準を調べるときは、共通 prompt の構築定義または正本仕様を参照してください。
- run join の事前条件、失敗時の復旧、または自動 join 後の publication を調べるときは、それぞれの lifecycle 仕様を参照してください。

## hash
- 4c9d7c42bb7430e25c163acbb12693c2bf418658c27047bcec493a6ea77f3070

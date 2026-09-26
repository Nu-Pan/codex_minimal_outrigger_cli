# `edit`

## Summary
- `cmoc oracle edit` の編集 agent call に共用する prompt と起動パラメータを構築する。編集指示、判断材料、oracle file の編集条件をまとめ、呼び出し側が決めた文書検索範囲を適用する。

## Read this when
- 編集 agent に渡す共通指示、oracle file の編集境界、未コミット差分の扱い、文書検索範囲の適用を確認・変更するとき。
- 編集本体と handoff 用 prompt skeleton に共通する構築処理を追うとき。

## Do not read this when
- 入力確定、実行前提、agent call の回数や順序、終了処理など、サブコマンド全体の挙動を確認・変更するときは、oracle edit の意味仕様へ進む。
- agent call の model provider、model、reasoning effort の設定を確認・変更するときは、設定定義へ進む。

## hash
- bba1b90a1a0e49f473a50d08ebca518fdda1deec97a878600a4a321c555707e4

# `investigation`

## Summary
- Oracle file の調査指示と呼び出し側が決めた閲覧範囲から、調査 agent 用の完全 prompt を組み立てる。
- 読み取り専用の oracle 調査とエディタ入力の引継ぎを含む、Codex CLI TUI 用の起動パラメータを作る。

## Read this when
- oracle investigation の TUI 呼び出しで、調査 prompt の目的や根拠範囲、読み取り専用指定、ポリシーの適用、エディタ入力の引継ぎ、起動パラメータを変更・追跡するとき。

## Do not read this when
- 調査コマンドの入力受付や実効閲覧範囲の決定、または完全 prompt の共通構築ルールが対象で、この呼び出し固有の内容が関係しないとき。それぞれの処理を担う箇所から確認する。

## hash
- 4b46490f23b3fd5dd5c6b66c029e900046191cb1c4e7449a7adfc76854f14da4

# `review`

## Summary
- 所見レビュー用のエージェント呼び出し定義をまとめる。新規所見の列挙、所見を支持・反証する理由の調査、提示可否の判定、所見リストの統合を扱う入口。

## Read this when
- oracle 所見レビューのエージェント呼び出しで、作業指示や各段階の組み立てを調べる・変更する場合。とくに新規所見の探索、特定所見の賛否理由、提示判断、所見間の重複や矛盾を整理する操作が対象になる時。

## Do not read this when
- 所見の正本仕様や保存規則そのものを調べる場合は、その仕様を定義する対象を直接読む。ここはレビュー用エージェント呼び出しの構築を扱う。
- oracle file の編集や調査など、レビュー以外のエージェント呼び出しを扱う場合は、その作業を担当する対象を読む。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

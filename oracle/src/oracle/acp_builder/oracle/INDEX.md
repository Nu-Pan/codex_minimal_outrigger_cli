# `edit`

## Summary
- `cmoc oracle edit` の編集 agent 向け指示と、呼び出しに使う固定パラメータを構築する。両方の編集 call で共用する編集目標・対象範囲・完了条件と、oracle file の編集境界を扱う。
- コマンド全体の実行制御ではなく、編集 workload 固有の prompt と起動条件を変更するときの入口。共通の prompt 構築処理を利用する。

## Read this when
- oracle edit agent が何を目標とし、どの情報を判断材料にして、どの範囲を編集できるかを変更するとき。
- 編集 agent の prompt や、Codex exec 起動用の固定パラメータを変更するとき。

## Do not read this when
- 入力確定、事前条件、indexing、二回の実行順序、結果報告などコマンド全体の流れを確認するときは、サブコマンドの仕様と呼び出し側の実装を読む。
- oracle file の調査だけを行う TUI 起動条件や指示を確認するときは、調査用 builder を読む。
- 複数の agent call に共通する prompt 構築規則を変更するときは、共通 prompt builder とその関連定義を読む。

## hash
- 5fd9c45a203ac50811632c5ec6e89806353ef57d841dc8bf123a51b7aa7ba2e4

# `investigation`

## Summary
- `cmoc oracle investigation` 用に、ユーザーの調査指示を含む完全 prompt と、oracle 読み取り専用の Codex TUI 起動設定を組み立てる。
- 共通の prompt 構築機能を使いながら、この調査経路で選ぶ指示内容と TUI 固有の設定を担う。

## Read this when
- 調査用 agent に渡す prompt の内容や、oracle 読み取り制限、handoff、indexing preflight など、この TUI 呼び出し固有の設定を変更・確認するとき。

## Do not read this when
- サブコマンド全体の実行順、調査の責務、変更境界を確認するときは、その意味仕様を直接読む。
- 共通 prompt 構築の挙動や agent 呼び出しパラメータ型の定義を確認するときは、共通 builder や型定義を直接読む。

## hash
- 179a429a524ca7ce54b47924b20858759faf740f69bf282b21d81bfc41fc09d8

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

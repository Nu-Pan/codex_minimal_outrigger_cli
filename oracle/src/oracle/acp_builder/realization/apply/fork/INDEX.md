# `launch_exec.py`

## Summary
- `cmoc realization apply fork` で agent に渡す完全 prompt と起動パラメータを組み立て、差分追従の指示と実行コンテキストを結び付ける。
- 指定された commit 範囲、run worktree、呼び出し元が決めた文書検索範囲を使い、oracle の変更を realization に反映する call 固有の指示と共通方針を構成する。

## Read this when
- `realization apply fork` の agent 向け指示、完了条件、差分の取得・扱いを確認または変更するとき。
- agent call のアクセス権限、作業ディレクトリ、文書検索範囲の受け渡しを確認または変更するとき。

## Do not read this when
- 追従対象の選定や run worktree の作成・管理など、agent call 起動前後の処理を確認または変更するときは、呼び出し側の apply orchestration を読む。
- 共通 prompt 方針や起動パラメータ型の定義だけを確認または変更するときは、それぞれの共通定義を読む。

## hash
- 4cbd2089f4a4d3b267f5c074c7d6115a7e397258d486befb5dd9bd201b90b392

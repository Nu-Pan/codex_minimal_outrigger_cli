# `oracle`

## Summary
- `cmoc review oracle` で oracle file レビュー所見を列挙・検証・採否判定・整理する agent call parameter と Structured Output schema をまとめた領域。
- レビュー対象から新規所見を抽出し、所見の妥当理由と反証理由を集め、人間へ提示するか判定し、重複や矛盾を整理する一連の出力契約と prompt 正本を確認する入口になる。

## Read this when
- `cmoc review oracle` の所見生成、所見検証、採否判定、所見リスト整理に関する agent call parameter や Structured Output schema を確認したいとき。
- oracle file レビューで、既知所見や既知理由との重複を避けて新規の所見・理由だけを返す契約を確認したいとき。
- レビュー所見について、妥当理由、反証理由、採否理由、重大度、見出し、根拠となる oracle file、整理理由をどの意味で扱うか確認したいとき。
- 複数のレビュー所見から、削除・置換・統合・変更不要のいずれとして整理するかの出力境界を確認したいとき。

## Do not read this when
- oracle file 全般の品質基準や、仕様断片として何を問題扱いするかの標準を確認したいとき。
- `cmoc review oracle` の CLI 実装、所見保存処理、表示整形、対象ファイル探索など、agent call parameter と応答 schema 以外の実装を確認したいとき。
- oracle review ではなく realization review や INDEX.md エントリー生成の prompt 正本を確認したいとき。
- prompt 部品の共通組み立て、path placeholder 解決、markdown rendering などの共通実装詳細を確認したいとき。

## hash
- b6e44967c4b4429485af5337e5f9e101a73ba2e569eb9068cf3bbda8292e886b

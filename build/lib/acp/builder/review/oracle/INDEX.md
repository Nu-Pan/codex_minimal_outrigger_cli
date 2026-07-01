# `__init__.py`

## Summary
- oracle.acp_builder.review.oracle 互換の package 入口であり、実体的な処理や仕様ではなく import path 互換性のために置かれている。

## Read this when
- oracle.acp_builder.review.oracle 系の互換 import path が必要か、package として存在する理由を確認したいとき。
- build 配下に生成された互換 package の最小的な責務を確認したいとき。

## Do not read this when
- review oracle の具体的な処理、判定ロジック、データ構造を調べたいとき。
- 正本仕様断片としての oracle file を確認したいとき。

## hash
- af0101216671fb90a1b9f95b81758a8f49779d3a1830bc39993735590f29a60d

# `enumerate_finding.py`

## Summary
- review finding 列挙処理の旧 import 経路を、正本側の canonical 実装へ接続する互換モジュール。呼び出し元の移行が終わるまで残すための薄い再 export であり、列挙処理そのものは持たない。

## Read this when
- review finding 列挙処理について、旧 import 経路がまだ使われている理由や移行完了後の削除条件を確認したいとき。
- 互換 import 経路から canonical 実装へどのように接続しているかを確認したいとき。

## Do not read this when
- review finding 列挙処理の実装内容や仕様上の意味を確認したいとき。この対象ではなく canonical 実装を読む。
- 新しい列挙ロジック、抽出条件、出力内容を変更したいとき。この対象は互換再 export だけを担う。

## hash
- 0469200f883330879457152116ebf6fce239124db5e820f3bc7d0122adf3707b

# `judge_finding.py`

## Summary
- レビュー指摘の判定ロジックについて、旧来の import 経路を維持するための互換 shim。実体は正本側の canonical implementation にあり、この対象自体は挙動を定義せず再エクスポートだけを担う。

## Read this when
- 旧来の import 経路からレビュー指摘判定を参照している呼び出し元を調査する。
- 互換 shim を削除できるか判断するため、旧経路への依存が残っているか確認する。
- レビュー指摘判定の import 経路移行に伴う影響範囲を確認する。

## Do not read this when
- レビュー指摘判定の仕様や実装内容を確認したい場合は、canonical implementation を直接読む。
- 新しいレビュー指摘判定ロジックを追加・変更したい場合は、この互換 shim ではなく実体側を読む。
- 通常の利用側コードで canonical path を既に使っている場合は、この対象を読む必要はない。

## hash
- 1af803594cd6409cf869f8b42cff07b9196e96439b57002bc1b935c328c1e069

# `merge_finding.py`

## Summary
- oracle merge finding review 用の agent call parameter を組み立てる既存の oracle 側 builder を呼び出し、その戻り値の構造を保ったまま prompt 内の oracle root placeholder 表記だけを補正する薄い実装です。
- known findings を入力として受け取り、model・reasoning effort・file access mode・structured output schema path は元の builder の値を維持し、prompt だけを最小限に修正します。

## Read this when
- oracle merge finding review の agent call parameter がどこで作られるかを確認したいとき。
- prompt 内の oracle root placeholder 表記補正が必要な理由、補正範囲、削除条件を確認したいとき。
- oracle 側 builder の出力を利用しつつ、realization 側で一時的に prompt を補正している経路を変更・削除したいとき。

## Do not read this when
- merge finding の正本仕様や元の prompt 内容そのものを確認したいとき。
- agent call parameter の基本データ構造や共通 builder の定義を確認したいとき。
- oracle merge finding review 以外の review 種別や、placeholder 補正と関係しない builder 実装を調べたいとき。

## hash
- 30f34cf41e060b2567a79f4e46fafe181afdd10fd79a1a7be75807ec8320b973

# `validate_finding_advocate.py`

## Summary
- レビュー用の oracle finding advocate パラメータ生成を、oracle 側の生成結果を元にしつつ静的プロンプト内の `<oracle_root>` 表記だけを `<oracle-root>` に補正する実装。動的入力である finding や既知理由は保持し、oracle src の typo が直るまでの互換補正を担う。

## Read this when
- oracle finding advocate レビューの agent call parameter 生成経路を確認・変更する場合。
- レビュー用プロンプトに含まれる `<oracle_root>` から `<oracle-root>` への最小補正がどこで行われているか確認する場合。
- oracle src 由来の静的 typo 補正と、finding・known reasons など動的入力を変更しない制約を確認する場合。

## Do not read this when
- oracle finding challenger など advocate 以外のレビュー用パラメータ生成を扱う場合。
- プロンプト typo 補正ではなく、oracle 側の正本プロンプト定義そのものを確認・変更する場合。
- 生成済み build 配下ではなく実装本体やテスト本体の変更箇所を探している場合。

## hash
- 31b050587e1d463e96b41b466bf5c79a8f3e17f87aa8c35847045f73823e5d2a

# `validate_finding_challenger.py`

## Summary
- 旧来の呼び出し元が使う互換 import 経路を維持し、正本側の challenger finding validation 実装へ再エクスポートする薄い中継モジュール。
- 実体は canonical oracle path 側にあり、この対象は移行期間中の import 互換性だけを担う。

## Read this when
- 旧来の import 経路がまだ必要か確認するとき。
- challenger finding validation の import 解決や互換中継の削除条件を調べるとき。
- canonical oracle path へ呼び出し元を移行する作業で、残っている互換モジュールの役割を確認するとき。

## Do not read this when
- challenger finding validation の実装内容や検証ロジックを確認したいとき。canonical oracle path 側の実装を直接読む。
- 新しい validation 挙動を追加・変更したいとき。この対象は互換 import の中継であり、挙動の実装場所ではない。
- 旧来の import 経路を使う呼び出し元が存在しないことを確認済みで、削除作業以外の目的で読むとき。

## hash
- 65259bcd79ca803eef7fc76ba4bbabf8267bb9b725e86300e20be0da2181ff24

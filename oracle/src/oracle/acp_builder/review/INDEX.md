# `oracle`

## Summary
- `cmoc review oracle` のレビュー用 agent call parameter と Structured Output schema を集めた oracle src ディレクトリ。
- oracle file から新規所見を列挙し、所見を擁護・反証し、人間提示の採否を判定し、重複・矛盾する所見リストを整理する各フェーズの正本仕様への入口になる。
- 各ファイルは、レビュー対象・既知所見や既知理由・file access profile・モデル設定・出力 schema など、oracle file レビューの AI 呼び出し契約をフェーズ別に定義する。

## Read this when
- `cmoc review oracle` の所見列挙、所見検証、採否判定、所見マージに関する agent call parameter や出力 schema を確認したいとき。
- oracle file レビューで、既知所見や既知理由との重複を避けて新規の所見・擁護理由・反証理由を返す仕様を追いたいとき。
- レビュー用 agent に oracle と INDEX だけを読ませ、realization file を読ませないアクセス制御や placeholder の扱いを確認したいとき。
- レビュー所見の重大度、見出し、根拠、理由、採否理由、整理理由を Structured Output 上でどう扱うか確認したいとき。

## Do not read this when
- `cmoc review oracle` 以外のサブコマンドや、oracle file 以外を対象にした review 用 agent call parameter を確認したいとき。
- CLI の実行制御、結果表示、ファイル編集、テスト追加など、レビュー用 AI 呼び出し契約の外側にある realization 側の実装だけを確認したいとき。
- file access profile、path placeholder、complete prompt rendering、AgentCallParameter などの共通部品そのものの仕様を確認したいとき。
- oracle file 全般の品質基準や仕様断片として何を問題扱いするかの標準を確認したいとき。

## hash
- f17b777e0537e918f35232e12f9408e13b30a5288258265259ca8b2b83003cbf

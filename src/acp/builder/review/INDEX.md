# `oracle`

## Summary
- oracle file レビューに関する AI 呼び出しパラメータ構築と、それに対応する Structured Output schema をまとめる領域。
- 新規所見の列挙、所見を支持・否定する理由の追加調査、所見採否の判定、所見群の重複・矛盾整理という、review oracle の主要なエージェント呼び出し単位への入口になる。
- 各処理は、対象所見や既知理由・既知所見を prompt に渡し、oracle file を根拠にした結果だけを返させるための role、goal、標準 prompt、file access mode、model class、reasoning effort、出力契約の対応を担う。

## Read this when
- `cmoc review oracle` で、oracle file レビュー用の agent 呼び出し内容や prompt 構築を確認・変更したいとき。
- oracle file から新規所見を列挙する処理、既知所見との重複回避、所見なしの場合の扱いを確認したいとき。
- レビュー所見について、妥当である理由と妥当ではない理由を oracle file に基づいて追加調査する呼び出しを追いたいとき。
- 擁護理由・反対理由を踏まえて、単一所見を人間へ提示するかどうか判定する処理を確認したいとき。
- 複数の oracle review 所見について、重複・矛盾・過剰な細分化を削除・置換・統合で整理する処理を確認したいとき。
- review oracle 標準や oracle 標準を組み込んだ complete prompt、oracle 読み取り専用のアクセス条件、モデル種別、推論量、対応する Structured Output schema の選択関係を確認したいとき。

## Do not read this when
- oracle file そのものの正本仕様内容や、レビューで実際に調査すべき仕様断片を探しているだけのとき。
- oracle file と realization file の基本定義、編集責任、配置ルール、または oracle 標準そのものを確認したいとき。
- レビュー所見の保存、CLI 表示、通知、集計、実行フロー全体、サブコマンド入口処理を確認したいとき。
- oracle file 以外の実装レビューや、通常の realization file レビューの prompt 構築を調べたいとき。
- 汎用的な AgentCallParameter、path 解決、Markdown レンダリング、構造化ドキュメント描画などの共通 helper の詳細を調べたいとき。
- Structured Output schema の項目名・型・JSON 形式だけを機械的に確認したいとき。

## hash
- 185a64c41d2cd90d0360720f548178b70f83b13227135db9ca5ac2dec73d6d76

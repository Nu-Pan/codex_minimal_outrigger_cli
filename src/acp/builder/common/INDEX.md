# `__init__.py`

## Summary
- oracle.acp_builder.common に対応する互換 builder package の入口を示す。

## Read this when
- acp builder common 領域で oracle 側との互換 package の有無や入口を確認したいとき。
- builder common 配下の import 経路や package 初期化の扱いを確認したいとき。

## Do not read this when
- builder common の具体的な処理内容や個別機能を調べたいときは、下位 module を直接読む。
- oracle 側の正本仕様断片を確認したいときは、対応する oracle file を読む。

## hash
- 39723a6719db306a6db964d9bcc53626a73d1311f463c76d706234e142954b99

# `file_access_rule_vaolation_recovery.json`

## Summary
- ファイルアクセス規則違反からの復旧結果または復旧方針を表すデータを、固定された内部構造に縛らず受け渡すための JSON Schema。具体的な項目はこのスキーマ自身では制限せず、利用側の文脈に委ねる。

## Read this when
- ファイルアクセス規則違反の検出後に、復旧処理の入出力データをどの程度構造化して扱うか確認したいとき。
- 復旧結果を厳密な項目定義ではなく任意の JSON object として許容している箇所の根拠を確認したいとき。

## Do not read this when
- 復旧処理そのものの手順、判定条件、エラーメッセージを確認したいとき。
- ファイルアクセス規則の内容や、読み書き禁止範囲の仕様を確認したいとき。
- JSON Schema の各プロパティに具体的な意味や型制約が定義されていることを期待しているとき。

## hash
- 5a6db1802d7f3515060678f77906368420e16f002dc760d59e62c5a6d8aac23c

# `file_access_rule_vaolation_recovery.py`

## Summary
- ファイルアクセス規則違反からのリカバリー用 agent call parameter を組み立てる realization wrapper。oracle 側の正本 builder を呼び出し、realization 側の型へ適応したうえで、参照される structured output schema が存在しない場合だけ同階層の代替 schema に差し替える。

## Read this when
- ファイルアクセス規則違反時に起動するリカバリー agent call の parameter 構築経路を確認・変更したいとき。
- oracle 側 builder の戻り値を realization 側の AgentCallParameter として扱う適応処理を調べたいとき。
- structured output schema path が欠落している場合の fallback 挙動を確認したいとき。

## Do not read this when
- ファイルアクセス規則そのものの定義や違反判定ロジックを調べたいとき。
- oracle 側のリカバリー parameter 正本仕様や builder 本体を確認したいとき。
- 一般的な agent call parameter の型定義や file access mode の意味を調べたいとき。

## hash
- 7562e91bea8502a7832008cf268a59e8a62d51c64298190701a4026ccac40ef4

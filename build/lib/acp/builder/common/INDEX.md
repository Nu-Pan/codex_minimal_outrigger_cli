# `__init__.py`

## Summary
- 互換 builder package の入口であり、oracle.acp_builder.common への互換レイヤーであることだけを示す。

## Read this when
- builder common package の互換入口がどの正本側 package に対応するかを確認したいとき。
- acp.builder.common 配下を参照する既存コードの互換先を把握したいとき。

## Do not read this when
- builder common の具体的な実装内容や API の詳細を確認したいとき。
- oracle.acp_builder.common 側の仕様や実装そのものを確認したいとき。

## hash
- 39723a6719db306a6db964d9bcc53626a73d1311f463c76d706234e142954b99

# `file_access_rule_vaolation_recovery.json`

## Summary
- 任意のオブジェクト形状を許容する JSON Schema。固定されたプロパティや必須項目を持たず、追加プロパティを制限しない対象を扱う。

## Read this when
- 特定のキー構造を定めず、オブジェクトであれば内容を広く受け入れる schema の意味を確認したいとき。
- プロパティ追加を禁止しない JSON Schema が必要かどうかを判断するとき。

## Do not read this when
- 必須プロパティ、型付きプロパティ、値制約などの具体的な schema 定義を確認したいとき。
- オブジェクト以外の JSON 値、または追加プロパティを制限する schema を探しているとき。

## hash
- 5a6db1802d7f3515060678f77906368420e16f002dc760d59e62c5a6d8aac23c

# `file_access_rule_vaolation_recovery.py`

## Summary
- ファイルアクセス規則違反からのリカバリー用 AgentCallParameter を構築する wrapper。oracle 側の正本 builder を import 可能にしたうえで委譲し、返された parameter を realization 側の型へ適合させる。
- oracle 側から渡された structured output schema path が存在しない場合だけ、この wrapper 自身に対応する schema path へ差し替えた AgentCallParameter を返す。

## Read this when
- ファイルアクセス規則違反リカバリー時に使う AgentCallParameter の構築経路を確認したいとき。
- oracle 側 builder への委譲、repo root 解決、oracle src の import 準備、realization 側 parameter への適合処理を調べるとき。
- structured output schema path が存在しない場合の fallback 挙動を変更または確認したいとき。

## Do not read this when
- ファイルアクセス規則違反の検出条件や違反ファイル一覧の生成処理を調べたいとき。
- AgentCallParameter や FileAccessMode の基本定義そのものを確認したいとき。
- oracle 側の正本 builder が生成する prompt 内容や parameter の詳細仕様を確認したいとき。

## hash
- 7562e91bea8502a7832008cf268a59e8a62d51c64298190701a4026ccac40ef4

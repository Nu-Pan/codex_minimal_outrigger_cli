# `join`

## Summary
- `cmoc session join` の Git merge conflict 解消用 AgentCallParameter を構築する実装。conflict 対象パスを実体パスへ解決し、対象ファイルと編集方針を含む prompt、およびリポジトリ書き込み・最高品質モデル・最大推論・事前 indexing 無効の起動設定をまとめる。

## Read this when
- `cmoc session join` の merge conflict marker 解消処理を変更または調査するとき。
- conflict 対象パスの解決、解消用 prompt、または AgentCallParameter のモデル・推論・アクセス設定を確認するとき。

## Do not read this when
- 通常の `session join` 処理や、merge conflict 解消以外の prompt 構築を確認するとき。
- AgentCallParameter の共通定義や prompt の一般的な組み立て規則を確認するときは、共通実装を直接読む。

## hash
- 56f23cc4685a1a253100696155f608756ab7835cf571e02d2255f1b6158f57c3

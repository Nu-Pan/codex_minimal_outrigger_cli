# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消用 AgentCallParameter を構築する正本ソース。競合対象パスを実パスへ解決して prompt に列挙し、競合解消時の役割・目標・追加アクセス規則・モデルおよび推論設定を定義する。

## Read this when
- `cmoc session join` の conflict marker 解消 prompt の内容、対象ファイル指定、AgentCallParameter のモデル・推論・アクセス設定を変更または確認するとき。

## Do not read this when
- 通常の `session join` 実装や conflict 解消処理そのものを調べるときは、該当するサブコマンド実装・テストを直接読む。
- prompt 全体の共通構築規則を調べるときは、prompt builder や共通 prompt 定義を直接読む。

## hash
- e3d325a17e362bec618d1339a0a3f8f41b3b2a414313fc7ebf45c49b0beb5bac

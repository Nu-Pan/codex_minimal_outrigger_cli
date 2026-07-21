# `conflict_resolution.py`

## Summary
- `cmoc session join` における merge conflict marker 解消用の AgentCallParameter を構築する正本ソース。対象パスを実パスへ解決して prompt に列挙し、conflict 解消時の役割・目標・追加アクセス規則・最高品質のモデル設定を定義する。

## Read this when
- `cmoc session join` の conflict marker 解消 prompt の内容、対象ファイル指定、AgentCallParameter のモデル・推論設定を変更または確認するとき。

## Do not read this when
- 通常の `session join` 実装や conflict 解消処理そのものを調べるときは、該当するサブコマンド実装・テストを直接読む。
- prompt 全体の共通構築規則を調べるときは、prompt builder や共通 prompt 定義を直接読む。

## hash
- 0d683ed9bde30e17c0907a0fabb464ea213e0aa4d5214db62c6ab5a35ab373c7

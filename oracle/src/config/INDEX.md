# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の挙動設定を集約する dataclass 群の仕様断片。設定は人間が編集する永続設定として扱われ、init による生成・同期、Enum 値の JSON 保存時の value 化、Codex CLI 向けモデル名・reasoning effort 名の対応、apply fork と review oracle のループ上限を定める。

## Read this when
- リポジトリ単位で永続化される cmoc 設定の構造、既定値、保存時の扱いを確認したいとき。
- Codex CLI に渡すモデル名や reasoning effort 名と、cmoc 内部の分類値との対応を確認・実装するとき。
- apply fork の apply ループや所見改善ループ、review oracle の所見列挙・マージ・検証ループの既定回数を確認・変更するとき。
- init が生成・同期する設定ファイルに含める項目や、人間が編集する設定面の範囲を確認するとき。

## Do not read this when
- パスキーワードや root 概念そのものの定義を確認したいだけのとき。
- 設定の永続化先を超えて、実際のファイル読み書き処理、JSON 変換処理、init コマンドの制御フローを確認したいとき。
- apply fork や review oracle の各ループ内部で行われる具体的な処理内容や所見生成ロジックを調べたいとき。
- Codex CLI 呼び出し全体の実行手順、プロンプト、サブプロセス制御を調べたいとき。

## hash
- 57ddc5247eb6651db57eb95b3655ce29ea534ab9ec4c1ada81c8f4ddb505a90e

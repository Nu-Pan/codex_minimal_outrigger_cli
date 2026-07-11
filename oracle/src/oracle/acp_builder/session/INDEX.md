# `join`

## Summary
- `cmoc session join` の conflict marker 解消向けに、対象パスの正規化、プロンプト組み立て、実行パラメータ設定を確認する入口。merge conflict の解消に関わる処理全体を見たいときにここから読む。
- conflict 対象ファイルの列挙や、解消時に許される追加編集範囲を確認したいときに読む。共通の prompt 生成や markdown 化の詳細は、ここではなく別の prompt builder 側を優先する。

## Read this when
- `cmoc session join` の conflict resolution 用パラメータ生成を変更・確認したい。
- conflict 対象パスの扱い、実行モデル、推論強度、repo write 前提の設定を確認したい。
- merge conflict 解消時に AI に渡す制約や追加ファイルアクセス条件を確認したい。

## Do not read this when
- 通常の `session join` の接続処理やセッション管理だけを見たい。
- 共通の prompt 生成ロジックや markdown 化の実装だけを見たい。
- conflict 解消以外のサブコマンド向けエージェントパラメータを探している。

## hash
- e88816171ef5820e886fd4240d718fc2765dd1aec17db5c41f8a3f7108287d2d

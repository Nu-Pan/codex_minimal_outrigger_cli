# `file_access_rule_vaolation_recovery.py`

## Summary
- ファイルアクセス規則違反が発生した agent call を復旧するための、再実行用 agent call parameter を組み立てる実装。違反時のアクセス規則、違反ファイル一覧、発生ログをプロンプトへ埋め込み、違反解消と元の作業目的維持を依頼する呼び出し設定を返す。

## Read this when
- ファイルアクセス規則違反を検出した後、その違反を解消するための agent call parameter の内容や生成条件を確認したいとき。
- 違反したアクセス規則、違反ファイル一覧、発生ログ情報をどのように復旧プロンプトへ渡すかを確認したいとき。
- 復旧担当 agent の role、summary、goal、file access mode、model class、reasoning effort の組み立てを変更したいとき。

## Do not read this when
- 通常の agent call parameter 全般の型定義や列挙値を確認したいとき。
- ファイルアクセス規則そのものの文面生成や各 access mode の仕様を確認したいとき。
- 完全なプロンプトを組み立てる共通処理や markdown rendering の詳細を確認したいとき。
- path placeholder の一般的な解決規則を確認したいとき。

## hash
- e52ec609130b621b6bdeb665952a259de9beb9222abd4b662919f1ab7060c337

# `conflict_resolution.py`

## Summary
- `cmoc session join` で発生した git merge conflict の解消を担当するエージェント呼び出しパラメータを構築する。対象ファイルの実体パスを解決し、conflict marker 解消用 prompt、最高品質のモデル・推論設定、リポジトリ書き込み権限、作業ディレクトリなどをまとめて返す。
- conflict 対象ファイルの指定、session join 用の prompt 構成、または conflict 解消エージェントの起動設定を確認・変更するときの入口となる。

## Read this when
- `cmoc session join` の merge conflict 解消処理を変更するとき
- conflict 解消用エージェントの prompt、対象パスの扱い、モデル・推論設定、ファイルアクセス権限を確認するとき
- conflict 解消呼び出しで indexing preflight を実行しない理由や作業ディレクトリの設定を確認するとき

## Do not read this when
- 通常の session join のマージ処理や conflict の検出ロジックを確認するときは、該当する session join の実装へ直接進む
- 一般的なエージェント呼び出しパラメータの定義や prompt 共通処理を確認するときは、それぞれの基盤モジュールへ直接進む
- conflict 解消対象のファイル内容や仕様を確認するときは、この構築定義ではなく指定された対象ファイルを読む

## hash
- af08f8775b2258495724cc5f93469532930cf907795d4a722e17bcd4a82a0647

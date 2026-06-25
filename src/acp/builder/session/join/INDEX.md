# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker を解消するための AI エージェント呼び出しパラメータを組み立てる実装。
- 解消対象パスを実パスに解決し、対象一覧、作業範囲、編集禁止事項、oracle file 例外、commit 禁止、marker 残存禁止を含む完了プロンプトを生成する。
- 返却するパラメータでは mainstream model、medium reasoning、realization write のファイルアクセス方針を指定し、生成した markdown prompt を渡す。

## Read this when
- `cmoc session join` の conflict marker 解消用エージェント呼び出し内容を変更・確認したいとき。
- merge conflict 解消タスクで AI に渡す role、summary、goal、補助プロンプト、ファイルアクセス方針を調整したいとき。
- conflict 対象パスの解決方法や、解消対象ファイル一覧をプロンプトへ埋め込む流れを確認したいとき。
- 通常は編集禁止の oracle file に conflict marker がある場合だけ、必要最小限の編集を許可する扱いを確認したいとき。

## Do not read this when
- `cmoc session join` の通常の join 処理、git 操作、conflict 検出そのものを調べたいとき。
- 汎用的な prompt 部品の組み立て仕様、markdown rendering、構造化ドキュメント表現の詳細を調べたいとき。
- path model 全般、work root 解決、実パス解決の詳細仕様を調べたいとき。
- conflict marker を実際に解消するアルゴリズムや、解消後の検証処理を探しているとき。

## hash
- 178b29ee724b5e7ba01760409af66a822e2463ff42db68de5125061b5a4138ab

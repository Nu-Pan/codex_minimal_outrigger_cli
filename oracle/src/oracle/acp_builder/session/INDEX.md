# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消エージェント呼び出しパラメータに関する正本実装を扱う領域。
- 衝突対象パスの提示、complete prompt の構成、モデルクラス・reasoning effort・ファイルアクセス権限など、session join の conflict 解消 agent call 条件を確認する入口となる。

## Read this when
- `cmoc session join` で merge conflict marker 解消エージェントへ渡す prompt、目標、呼び出し条件を確認または変更したいとき。
- conflict 対象ファイル一覧がどのように実パスへ解決され、prompt 内に提示されるかを確認したいとき。
- oracle file の conflict 解消時だけ許可される追加編集規則を確認したいとき。
- `oracle_and_realization_basic`、`oracle_standard`、`realization_standard` を含む complete prompt 構成が必要な session join 用 agent call parameter を調べるとき。

## Do not read this when
- merge conflict marker の検出処理、git merge の実行、または `cmoc session join` 全体の制御フローを調べたいだけのとき。
- complete prompt builder、構造化 markdown rendering、path placeholder 解決、agent call parameter 型そのものの汎用仕様を調べたいとき。
- session join 以外のサブコマンドや、merge conflict marker 解消以外の agent call prompt を確認したいとき。

## hash
- a1e1f5ca18b8cebe3bc9332e4a91ac0c2ec835c075991ce38f0f101be2ad0ee0

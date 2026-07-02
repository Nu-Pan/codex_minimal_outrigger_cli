# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker を解消するための AI エージェント呼び出しパラメータを組み立てる正本実装。対象パス一覧を実パスへ解決し、衝突解消の役割・目標・追加アクセス規則を含む complete prompt を生成して、MAINSTREAM / MEDIUM / REPO_WRITE の呼び出し条件として返す。

## Read this when
- `cmoc session join` の conflict marker 解消エージェントに渡す prompt、目標、ファイルアクセス権限、モデルクラス、reasoning effort を確認または変更したいとき。
- conflict 対象ファイル一覧が prompt 内でどのように提示されるか、また oracle file の conflict 解消時だけ許可される追加編集規則を確認したいとき。
- `oracle_and_realization_basic`、`oracle_standard`、`realization_standard` を含めた complete prompt 構成が必要な session join 用 agent call parameter を調べるとき。

## Do not read this when
- merge conflict marker の検出処理、git merge の実行、または `cmoc session join` 全体の制御フローを調べたいだけのとき。
- complete prompt builder、構造化 markdown rendering、path placeholder 解決、agent call parameter 型そのものの汎用仕様を調べたいとき。
- session join 以外のサブコマンドや、merge conflict marker 解消以外の agent call prompt を確認したいとき。

## hash
- 6e41085dc88a41a3b09065d5d75629402b6dff3dbd8eeb4d44ce98f3f0f91777

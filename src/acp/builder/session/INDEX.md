# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消フェーズで、AI エージェント呼び出しパラメータを組み立てる領域。conflict 対象パスの実パス解決、解消作業だけに範囲を絞る prompt、realization 書き込み権限、oracle/realization 標準指示の付与を扱う。

## Read this when
- `cmoc session join` で検出済みの merge conflict marker を AI に解消させるための role、summary、goal、補助 prompt、モデル種別、推論努力、ファイルアクセス権限を確認または変更したいとき。
- conflict 対象ファイル一覧を AI prompt にどう渡すか、また対象パスをどの時点で実パスへ解決するかを確認したいとき。
- 通常は realization 書き込み権限で動く join 用 AI 呼び出しに対して、conflict 解消に限り oracle file の最小編集を許可する境界を確認したいとき。
- merge conflict 解消作業で git add や git commit を禁止し、conflict marker が残らない状態を goal とする prompt の内容を確認したいとき。

## Do not read this when
- `cmoc session join` 全体の制御、merge 実行、conflict marker の検出、join 後の状態更新を調べたいとき。
- AI 呼び出しパラメータの共通型、モデル種別、推論努力、ファイルアクセスモードそのものの定義を調べたいとき。
- prompt 部品の markdown レンダリング、共通 prompt 構築、oracle/realization 標準指示の中身を変更したいとき。
- conflict marker 解消以外の通常の session 処理や、対象外ファイルの編集方針を調べたいとき。

## hash
- f3ebc8b4e31d2f112ede8674c70afa589034013385cad2d636477271686f8c18

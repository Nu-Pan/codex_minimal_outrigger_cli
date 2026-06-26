# `conflict_resolution.py`

## Summary
- `cmoc session join` の merge conflict marker 解消を AI エージェントに依頼するための呼び出しパラメータを構築する実装。
- 解消対象パスを実パスへ正規化し、対象一覧と追加アクセス規則を含む完了プロンプトを組み立て、mainstream model・medium reasoning・realization write の実行条件で返す。

## Read this when
- `cmoc session join` が検出した merge conflict marker の解消作業を、どの role・goal・file access mode で AI に渡すかを確認または変更したいとき。
- conflict 対象ファイル一覧がプロンプト内へどう渡されるか、また oracle file に marker がある場合の最小編集許可がどう表現されるかを確認したいとき。
- session join 系のエージェント呼び出しで、merge conflict 解消に限定した禁止事項や完了条件を調整したいとき。

## Do not read this when
- 実際に merge conflict marker を解析・除去するアルゴリズムやファイル編集処理を探しているとき。
- `cmoc session join` 全体の制御フロー、conflict 対象パスの検出、git 操作、または join 成功後の処理を確認したいとき。
- 汎用的な prompt 部品の markdown 構築、構造化ドキュメントの描画、path model の実パス解決そのものを調べたいとき。

## hash
- caceb7b108026650c89706b5a14843849da1f7f4c861170455ee863feab7f786

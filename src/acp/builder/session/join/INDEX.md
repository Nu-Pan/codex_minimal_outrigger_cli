# `conflict_resolution.py`

## Summary
- `cmoc session join` で merge conflict marker 解消を担当する AI エージェント呼び出しパラメータを構築する実装。
- 衝突対象パスを作業ルート基準の実パスへ解決し、対象ファイル一覧、作業範囲、編集禁止事項、oracle file への限定的な例外許可を含む complete prompt を組み立てる。
- 返却する呼び出し条件は mainstream モデル、中程度の推論、リポジトリ書き込み権限で、生成した prompt markdown を AgentCallParameter に格納する。

## Read this when
- `cmoc session join` の merge conflict marker 解消用プロンプト、権限、モデル、推論量、または AgentCallParameter の構築内容を確認・変更したいとき。
- conflict marker 解消作業における編集範囲の制約、git add/git commit 禁止、対象外ファイル編集禁止、oracle file への必要最小限の編集許可を扱う箇所を探しているとき。
- 衝突対象ファイルのパス一覧がどのように resolve され、AI に渡す補助 prompt に埋め込まれるかを確認したいとき。

## Do not read this when
- 通常の `cmoc session join` 処理全体の制御フロー、git 操作、または merge 実行そのものを調べたいだけのとき。
- complete prompt の共通構築ロジック、StructDoc の markdown レンダリング、または AgentCallParameter 型そのものの仕様を確認したいとき。
- merge conflict marker の検出ロジックや、実際に conflict を解消するアルゴリズムの実装を探しているとき。

## hash
- 294d743be90256911378561e269dad646f2dc5930f5fe8e3dea6171cf579f30c

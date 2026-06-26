# `join`

## Summary
- session join 中に検出された merge conflict marker を解消するため、AI エージェント呼び出しのパラメータと完了プロンプトを組み立てる領域。
- conflict 対象の実パス解決、作業ルート解決、対象ファイル一覧の埋め込み、解消作業に限定した役割・目標・追加アクセス規則を扱う。

## Read this when
- session join が merge conflict marker 解消用にどのようなエージェント呼び出し内容を作るか確認・変更したいとき。
- conflict 対象ファイルの一覧がプロンプトへどのように渡されるか、また対象パスや作業ルートがどのように解決されるかを追いたいとき。
- merge conflict marker 解消時の許可範囲、禁止事項、oracle file への例外的編集許可、git add や git commit の禁止指示を確認したいとき。

## Do not read this when
- session join 全体の処理フロー、workspace 状態の統合、または conflict marker の検出処理を調べたいだけのとき。
- merge conflict の内容を実際にどう編集して解消するかという自動編集アルゴリズムを探しているとき。
- 汎用的なプロンプト部品、エージェント呼び出しパラメータの型定義、またはパスモデルの仕様そのものを確認したいとき。

## hash
- ed515ca206fe710cabb674682f420631db8fcba97058c5dfc68d14acef9149a6

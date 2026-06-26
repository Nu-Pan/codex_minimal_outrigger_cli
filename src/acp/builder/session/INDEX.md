# `join`

## Summary
- `cmoc session join` の merge conflict marker 解消を担当する AI 呼び出し条件を組み立てる領域。
- 衝突対象パスを作業ルート基準の実パスとして解決し、対象ファイル、作業範囲、編集禁止事項、oracle file への限定的な例外許可を含む complete prompt を構成する。
- 生成した prompt markdown を、mainstream モデル、中程度の推論、リポジトリ書き込み権限を持つ AgentCallParameter として返す処理への入口となる。

## Read this when
- `cmoc session join` で conflict marker 解消用エージェントに渡す prompt、権限、モデル、推論量、または AgentCallParameter の内容を確認・変更したいとき。
- conflict marker 解消作業で、対象ファイル以外の編集禁止、git add や git commit の禁止、作業範囲の制約、oracle file への必要最小限の編集許可がどのように指示されるかを確認したいとき。
- 衝突対象ファイルのパス一覧がどのように解決され、補助 prompt として AI に渡されるかを調べたいとき。

## Do not read this when
- `cmoc session join` 全体の制御フロー、git 操作、merge 実行、または join コマンドの通常処理を調べたいだけのとき。
- complete prompt の共通構築、StructDoc の markdown 化、AgentCallParameter 型そのものなど、呼び出しパラメータ構築の周辺共通部品を確認したいとき。
- merge conflict marker の検出方法や、実際に衝突内容を解決するアルゴリズムを探しているとき。

## hash
- f2ff755136c8ea1f506e298f02ee1d87d3392b54afc2f303dbab3bf5045c3817

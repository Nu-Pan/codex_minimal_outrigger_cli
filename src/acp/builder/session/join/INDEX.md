# `conflict_resolution.py`

## Summary
- `cmoc session join` で検出された merge conflict marker の解消を AI エージェントへ依頼するための呼び出しパラメータを構築する実装。
- 解消対象パスを作業ツリー基準の実パスへ解決し、対象ファイル一覧、作業範囲、禁止事項、oracle file への限定的な編集例外を含む complete prompt を生成して `AgentCallParameter` として返す。

## Read this when
- `cmoc session join` の conflict marker 解消用プロンプトの役割、制約、AI 呼び出し設定を確認または変更したいとき。
- merge conflict 解消対象ファイルのパス一覧がプロンプトへどう渡されるかを確認したいとき。
- conflict marker 解消作業に限って oracle file の編集を許可する例外ルールや、git add・git commit 禁止などの作業境界を調整したいとき。

## Do not read this when
- 通常の session join 処理全体、merge 実行、conflict 検出、または join 後の状態管理を調べたいだけのとき。
- complete prompt の共通構築処理、構造化 markdown レンダリング、path model、AgentCallParameter 型そのものの仕様を調べたいとき。
- conflict marker 解消後の検証、テスト、または CLI 入出力の外部仕様を確認したいとき。

## hash
- 3fa51a6697d3c884d6cf97774a8fc325c7e78d7d57e14c43709f786093cd3cb2

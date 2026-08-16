# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築する実装。ユーザーの調査指示を固定の完全プロンプトへ組み込み、oracle-only の読み取り制約、パスコンテキスト、モデル・推論設定、構造化出力設定、索引付け前処理を含む `AgentCallParameter` を返す。oracle 調査起動フローのパラメータ定義を確認・変更するときの入口。

## Read this when
- `cmoc oracle investigation` の TUI 起動時に、完全プロンプトやユーザー指示の組み込み方を確認するとき
- oracle 調査用 agent call のモデル、権限、作業ディレクトリ、起動前処理などの固定パラメータを確認・変更するとき
- oracle 調査プロンプトの構築元や、調査・ルーティング・エディタ引き渡しポリシーの適用箇所を追うとき

## Do not read this when
- oracle file の調査内容そのものや正本仕様を確認したいときは、対象の oracle file を直接読む
- 一般的な agent call パラメータの型・列挙値の定義を確認したいときは、`oracle.acp_builder.basic` の定義を読む
- 完全プロンプトの共通生成規則だけを確認したいときは、`oracle.prompt_builder.complete_prompt` の実装を直接読む

## hash
- 9ca8a56ecf5454860a872b762978ce09e29fb6b3fc13af3762d46129dcc17ead

# `launch_tui.py`

## Summary
- `cmoc tui` が使用する AgentCallParameter と、TUI に渡す完全プロンプトの構築を定義する。
- オリジナルプロンプトを参照として埋め込み、リポジトリ書き込み権限、リポジトリルートの作業コンテキスト、モデル・推論設定、起動前 indexing を含む固定の TUI 起動パラメータを組み立てる。

## Read this when
- `cmoc tui` の TUI 起動パラメータや起動用プロンプト skeleton の構築を確認・変更するとき。
- オリジナルプロンプトの埋め込み方、AgentCallPathContext、FileAccessMode、ModelClass、ReasoningEffort、indexing 実行設定を確認するとき。

## Do not read this when
- 完全プロンプトの共通レンダリング規則を確認したい場合は、`build_complete_prompt` の実装を直接読むとき。
- TUI 起動パラメータの呼び出し元や、別サブコマンドの設定を調べる場合。

## hash
- 9a603c5e0a3f6e154ea36ebd667ac04fc9dea841cafda3de11e0828c2cad57da

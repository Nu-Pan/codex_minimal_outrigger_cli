# `oracle`

## Summary
- cmoc の各 agent call に渡す AgentCallParameter と、用途別の prompt・Structured Output・モデル・推論設定・ファイルアクセス・cwd・indexing preflight を構築する領域。共通の論理モデル定義から、indexing、feedback、oracle、realization、session join、TUI、quota probe の起動定義へ進む入口となる。

## Read this when
- 複数の cmoc サブコマンドにまたがる agent call 起動パラメータの構成や共通責務を確認するとき。
- 特定用途の agent call builder を探し、用途別の下位領域へ進む前に全体の分類を把握するとき。
- agent call の prompt 構築結果と、Structured Output、モデル・推論設定、ファイルアクセス、cwd、indexing preflight の組み合わせを確認するとき。

## Do not read this when
- 共通の AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode の定義だけを確認したい場合は、共通定義を直接読むとき。
- indexing、feedback、oracle、realization、session join、TUI の特定用途だけを調査する場合は、対応する下位領域を直接読むとき。
- 完全 prompt の共通構築、Standard、file access rule、Structured Output schema の定義を確認する場合は、prompt_builder または各用途の schema を直接読むとき。
- oracle や realization の具体的な仕様、実装、テスト内容を確認する場合は、それぞれの正本・実装・テスト対象を直接読むとき。

## hash
- 8eb8dd3192e5af9f90953f41f58d7db691d3a0a2734ff5d3d72eceb2224227d9

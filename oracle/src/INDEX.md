# `oracle`

## Summary
- cmoc の oracle 関連定義を集約するディレクトリ。AgentCallParameter の共通モデルと、oracle・realization・feedback・indexing・session・tui などの agent call 構築、prompt、Structured Output schema の下位要素への入口を提供する。
- oracle 配下には、agent call builder の共通定義、oracle 調査・レビュー、realization 作業、feedback 処理、INDEX.md 生成、session conflict 解消、TUI・quota probe の起動定義が機能別に配置されている。

## Read this when
- cmoc の oracle 関連 agent call が、どの prompt、モデル・推論設定、ファイルアクセスモード、cwd、Structured Output schema を使うか調査または変更するとき。
- 共通の AgentCallParameter、論理モデル種別、推論強度、ファイルアクセスモードを確認するときは acp_builder/basic.py へ進むとき。
- 特定機能の agent call 構築を確認するときは acp_builder 配下の該当する oracle、realization、feedback、indexing、session、tui の下位要素へ進むとき。
- prompt の統合規則や policy の構築を確認するときは prompt_builder 配下へ進むとき。
- パス解決、設定、構造化文書レンダリングの補助定義を確認するときは other 配下へ進むとき。

## Do not read this when
- Codex CLI の実際の agent call 実行処理や、抽象モデル・推論設定を具体的な CLI 引数へ変換する処理を確認したいとき。
- oracle・realization・feedback の意味仕様や正本文書そのものを確認したいとき。
- 既存の INDEX.md のルーティング内容だけを確認したいとき。

## hash
- 4ceef60433360bcbff7e620370866bdd03116e7f258b3c3b431bcf7d2bb0c01f

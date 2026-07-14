# `__init__.py`

## Summary
- 既存の `acp.builder.tui.*` import を維持するためだけに残された、`oracle.acp_builder.tui` 互換 package の入口。
- realization 側と利用者向け公開面からこの参照が消えた後に削除できる互換層として位置づけられる。

## Read this when
- 既存 import 経路 `acp.builder.tui.*` の互換維持や削除可否を確認する。
- `oracle.acp_builder.tui` との互換 package がなぜ残っているかを確認する。

## Do not read this when
- TUI 実装本体の挙動や画面構成を確認したい場合。
- 新しい公開 API や新規 import 経路を設計したい場合。

## hash
- 9e5ae7e28c1e80b5ffa414ac5eea7dd08927b7977f87292b3afa9b714a894d0a

# `launch_tui.py`

## Summary
- `cmoc tui` の起動パラメータを組み立てる互換入口。実体の生成は oracle 側に委譲し、この層では実行時に必要な `tui` 保存先だけ先に用意する。

## Read this when
- TUI 起動時の `AgentCallParameter` の作り方と、実行前に必要な保存先の準備を確認したいとき。
- realization 側の入口が oracle 側の builder をどう包んでいるかを見たいとき。

## Do not read this when
- `cmoc tui` の引数解釈や出力内容そのものを知りたいときは、委譲先の oracle 側 builder を読む。
- TUI 以外のコマンドの起動パラメータを調べたいとき。

## hash
- 544414fb16a433336a20d2d8feb385b3b15697d08a23768a5aa47fafd3bcc734

# `resolve_parameter.py`

## Summary
- TUI の `resolve_parameter` 生成を、既存の TUI 呼び出し経路からたどるための互換入口。正本の実装へ移る前に、この薄い転送層と公開している選択肢だけ確認したいときに読む。

## Read this when
- `acp.builder.tui.resolve_parameter` を import している呼び出し元を直すか確認したいとき。
- TUI から resolve-parameter 用の builder を使う経路が、どの canonical 実装に委譲されているかを知りたいとき。
- TUI 側で公開している `FileAccessMode` の利用可能な選択肢が、どの制約で絞られているかを確認したいとき。

## Do not read this when
- TUI resolve-parameter の実際の生成ロジックを変更したいときは、canonical な oracle 側の builder を読む。
- ファイルアクセスモードの定義そのものを変えたいときは、この互換入口ではなく正本の定義を読む。
- 新しい TUI 機能を設計したいだけで、既存の互換 import 経路を維持する必要がないとき。

## hash
- 96fdbba75b80c4af522536f9bd1b5af9efaad1b5698c436de5ea5fce2e84b1f0

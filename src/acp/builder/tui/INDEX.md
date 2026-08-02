# `__init__.py`

## Summary
- TUI 起動 builder の既存 import 経路を維持する互換 package。realization 側および利用者向け公開面から同経路が不要になった場合の削除候補であり、TUI builder の実装詳細への入口ではない。

## Read this when
- TUI 起動 builder の既存 import 経路や互換性を確認するとき
- realization 側または利用者向け公開面から当該 import 経路を削除・変更できるか判断するとき

## Do not read this when
- TUI builder の実装や起動処理そのものを変更・調査するとき
- TUI 起動 builder の import 互換性に関係しない処理を扱うとき

## hash
- d9cfe056fb590ace7dace1732eced1ab73daab8f28e521f8d480dd52beb37a60

# `launch_tui.py`

## Summary
- TUI 起動 parameter builder を互換 import 経路として公開する薄いモジュール。実装本体は oracle 側の `build_tui_launch_tui_parameter` を再エクスポートし、TUI 起動 parameter 構築への入口を提供する。

## Read this when
- TUI 起動 parameter builder の互換 import 経路や公開名を確認するとき。
- `build_tui_launch_tui_parameter` をこの import 経路から利用するコードを調査するとき。

## Do not read this when
- parameter builder の実装詳細を確認したいときは、再エクスポート元の oracle 側実装を直接読む。
- TUI 起動以外の parameter 構築や、互換 import 経路に関係しない処理を調査するとき。

## hash
- ce5d479f7cdbb9db6b4500a3d3a3f7411a47e05200670c12c41672e3101c5b93

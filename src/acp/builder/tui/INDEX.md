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
- TUI 起動 parameter builder の互換 import 経路を提供するモジュール。実体の builder は oracle 側の TUI 起動定義から再公開されるため、TUI 起動 parameter の実装詳細ではなく、この import 経路の利用箇所から下位定義へ進む入口として扱う。

## Read this when
- TUI 起動 parameter builder を既存の import 経路から参照するコードや、互換 import の解決先を確認するとき。

## Do not read this when
- TUI 起動 parameter の生成ロジックや挙動を調査・変更するときは、再公開元の TUI 起動定義を直接読む。
- TUI 以外の ACP builder や、parameter builder の共通仕様を調査するとき。

## hash
- 1a8a4aaf0f802fad209b12e2f0fbf5a2632620119c7e31c49847c01a3da61a93

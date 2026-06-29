# `__init__.py`

## Summary
- oracle.acp_builder.review と互換の package であることだけを示す、review builder 領域の package 初期化用ファイル。実装ロジックや詳細な仕様ではなく、互換名前空間としての位置づけを確認する入口になる。

## Read this when
- review builder 領域で、oracle 側の同名 package と対応する realization package が存在するかを確認したいとき。
- package としての互換性や import 経路の成立だけを確認したいとき。

## Do not read this when
- review builder の具体的な処理、関数、クラス、出力、制御フローを調べたいとき。
- 正本仕様断片としての review builder の要求を調べたいとき。
- package 初期化以外の実装変更先を探しているとき。

## hash
- adf6124f1c3a49a136159186b6a58b39f4321e0113527b60e85d8b1e3205484e

# `oracle`

## Summary
- review oracle 向け builder の realization 側入口をまとめる package。finding の列挙・判定・統合・検証用パラメータ生成について、正本側実装の再公開または最小限の prompt 補正を行う薄い互換層を収める。
- 多くの対象は正本側実装への委譲境界であり、実際の判定ロジックや oracle 仕様断片ではなく、realization 側 import path から正本由来の review oracle 機能へ到達するための入口として位置づく。

## Read this when
- realization 側から review oracle の finding 列挙・判定・統合・検証機能がどの import 経路で参照され、どこまで正本側へ委譲されているかを確認したいとき。
- review oracle 用 AgentCallParameter の生成経路で、正本側 builder の返却値に対して realization 側が prompt の oracle root 表記 typo だけを補正している箇所を探したいとき。
- finding、known findings、advocate 理由、challenger 理由などの動的入力を改変せず、生成済みパラメータの一部だけを維持または差し替える互換層を確認したいとき。
- この階層のモジュールが独自の review 判定処理を持つのか、正本側実装を再公開するだけなのかを切り分けたいとき。

## Do not read this when
- review oracle の finding 列挙・判定・統合・検証ロジックそのもの、入力・出力・判定基準、prompt 本文、structured output schema の内容を理解したいとき。その場合は委譲先の正本側 oracle src や該当仕様断片を読む。
- AgentCallParameter 型、model class、reasoning effort、file access mode、アクセス設定などの一般仕様を調べたいとき。
- oracle file と realization file の基本概念、oracle root などのパスモデル全体、または INDEX.md 生成規則を確認したいだけのとき。
- review oracle 以外の builder、CLI 入出力、テスト観点、または finding 以外の review 処理を調べているとき。

## hash
- d1748dae1a3c9f0d53b25cdc3c98ae8e374cd17c27acccbb65f5fe366661b397

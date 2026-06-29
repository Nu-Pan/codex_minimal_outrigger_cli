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
- review oracle 用 builder 群のうち、旧来の実装側 import 経路を維持する互換層と、正本側 builder の生成結果に既知の prompt 表記補正をかける薄い wrapper を置く領域。
- finding の列挙・判定・challenger 検証は実装本体を持たず正本側へ再公開し、finding 統合と advocate 検証は正本側 builder へ委譲したうえで oracle root placeholder 表記の局所補正だけを担う。
- review oracle の実処理・仕様本体を読む入口ではなく、realization 側に残る互換 import path と一時的な prompt 補正経路を確認するための入口である。

## Read this when
- review oracle builder 周辺で、古い realization 側 import 経路がまだ残っている理由、削除条件、正本側実装への委譲関係を確認したいとき。
- finding 統合や advocate 検証の AgentCallParameter 生成で、正本側 builder の返す parameter を保ったまま prompt 内の oracle root placeholder 表記だけを補正する wrapper の存在を調べたいとき。
- 同名機能の実装がこの階層にあるように見えるが、実体が正本側にあるのか、この階層で補正しているのかを切り分けたいとき。
- 互換 module を削除できるか、または呼び出し元を canonical oracle path へ移行する必要があるかを判断したいとき。

## Do not read this when
- review finding の列挙・判定・検証ロジックそのものや、prompt の正本仕様を確認したいとき。この階層ではなく正本側 oracle 実装や対応する仕様断片を読む。
- review oracle 以外の builder、CLI 表示、テスト方針、AgentCallParameter 型の共通仕様を調べたいとき。より直接その責務を持つ対象へ進む。
- 新しい判定ロジックや検証処理を追加・変更したいとき。互換再公開 module は実装本体ではなく、補正 wrapper も正本側 builder への追従用の薄い処理に限られる。
- 単に生成済み parameter の利用側挙動を追うだけで、旧 import 経路や prompt 表記補正の有無が関係しないとき。

## hash
- 800f388a4635bfdb36722be843a4f34b79e7d170fcdd7b884629e83bcc21ad55

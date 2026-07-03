# `__init__.py`

## Summary
- 既存の review builder 系 import 互換性を保つためだけに残された package 初期化部分。現行実装や公開面から互換 import が消えた時点で削除候補になる境界を示す。

## Read this when
- review builder 周辺の import 互換性を確認する。
- 古い acp.builder.review 系参照を削除できるか判断する。
- 互換 package の残存理由や削除条件を確認する。

## Do not read this when
- review builder の実処理や変換ロジックを調べたい。
- 新しい公開 API や利用者向け機能の仕様を確認したい。
- 互換 import と無関係な builder 実装を変更する。

## hash
- 20e0879d03952a8b860e9d09a0f9c7e08c05699e96390ec504f3e0481a897ebb

# `oracle`

## Summary
- review oracle 向け agent call parameter builder 群を扱う領域。主に旧来 import 経路を canonical oracle 実装へ委譲する互換層と、正本側 builder 出力に残る placeholder 表記差を realization 側で最小補正する薄い wrapper を含む。
- 実際の review oracle 仕様や判定ロジック本体ではなく、既存 caller との import 互換性、正本側 builder の再利用、一時的な typo・placeholder 補正の責務境界を確認する入口になる。

## Read this when
- review oracle 周辺の agent call parameter 生成で、realization 側が正本側 builder をどう再利用・補正しているか確認したい。
- review finding enumeration、judgment、validation などの旧来 import 経路が canonical oracle 実装へ委譲されているか、また互換層を削除できる条件を調べたい。
- prompt 内の oracle root placeholder 表記差など、正本側で解消されるまで realization 側に残している一時補正の範囲と削除条件を確認したい。
- 同名機能の実装が realization 側にあるように見えるが、実体を持つ実装なのか互換 import 層なのかを切り分けたい。

## Do not read this when
- review oracle の正本仕様、prompt の本来の文面、判定仕様、検証ロジック本体を確認したい場合は、対応する oracle file または canonical oracle 実装を直接読む。
- AgentCallParameter の基礎データ構造、model、reasoning effort、file access mode などの共通仕様を調べたい場合は、基礎定義側を読む。
- 互換 import 経路や一時的な placeholder 補正と無関係な review 全体の構成、別種の builder、または他領域の処理を調べたい場合は、より上位または該当対象へ進む。

## hash
- 7085f936f3d433011992d08f54118e0e9fc1eb64cb173a71dbb53ff27f7b5a37

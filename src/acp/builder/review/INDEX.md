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
- review oracle 用 agent call parameter builder 群のうち、旧 import 経路を維持する互換入口と、oracle src 由来 builder の戻り値へ既知の静的 placeholder/typo 補正を加える薄い realization 実装を収める。
- 主な責務は canonical 実装への再 export、既存 caller 移行までの互換維持、正本側の既知表記不具合に対する最小補正であり、review finding の実処理本体や正本 prompt そのものは別対象にある。

## Read this when
- review oracle finding の列挙・判定・統合・検証に関して、旧 import 経路から canonical 実装へつながる互換層を確認する。
- 既存 caller を canonical path へ移行する作業で、互換モジュールの削除可否や削除条件を判断する。
- oracle src 由来の agent call parameter に対して、prompt 内の oracle root placeholder 表記や静的 typo の最小補正がどこで行われるか確認する。
- finding や既知理由などの動的入力を改変せず保持する境界を確認する。

## Do not read this when
- review finding enumeration、judgment、validation の実処理や parameter 構築ロジックを確認したい場合は、canonical oracle path 側を読む。
- レビュー一般の finding 統合仕様、prompt 本文、または oracle src 側の正本定義そのものを確認・変更したい場合。
- agent call parameter の基本構造、型責務、構造化出力 schema、path model、ファイルアクセスなど、互換 import 経路や既知表記補正と無関係な基礎仕様を調べる場合。
- 新規 caller が利用すべき import path だけを確認したい場合は、canonical oracle path 側を読む。

## hash
- 2069772fc99338daeb1c34226e17f35226659623c1c5d8443103c3e8749d1fd5

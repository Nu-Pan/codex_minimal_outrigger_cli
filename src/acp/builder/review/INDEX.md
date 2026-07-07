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
- review oracle 向け agent call parameter builder 群のうち、旧 import 経路を維持する互換入口と、正本 builder 由来 prompt の既知 typo を最小補正する薄い adapter を含む。
- 実処理の多くは canonical oracle path または oracle src 側へ委譲され、この階層は移行中 caller との互換性、削除条件、review finding merge / validate finding advocate の限定補正境界を確認する入口になる。

## Read this when
- review oracle の旧 import 経路から canonical oracle path への移行状況、互換 shim の再 export 対象、または削除可否を確認する。
- merge finding や validate finding advocate の agent call parameter が、正本 builder から取得された後にどの範囲だけ realization 側で補正されるかを確認する。
- 正本 prompt に残る oracle root 表記 typo への一時的な補正、補正の削除条件、動的入力を改変しない境界を確認する。

## Do not read this when
- review oracle の正本仕様や正本 prompt の内容そのものを確認したい場合は、oracle 側の該当本文を読む。
- review finding enumeration、judgment、challenger validation の実処理や parameter 構築ロジックを確認したい場合は、canonical oracle path 側を読む。
- review oracle 以外の builder、agent call parameter 全般、path model、INDEX.md エントリー生成、または一般的な oracle file 定義を調べたい場合。

## hash
- 6b45aca0d34cdb64421456268debbca8e84f943b865d71f94b81ab3d36d65030

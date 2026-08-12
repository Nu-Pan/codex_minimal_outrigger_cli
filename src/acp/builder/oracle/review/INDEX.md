# `__init__.py`

## Summary
- `cmoc oracle review` builder の realization adapter package。oracle review ビルド処理に関する実装への入口。

## Read this when
- `cmoc oracle review` builder の realization adapter package の責務や関連実装を確認するとき。

## Do not read this when
- oracle review の正本仕様や、builder 以外の CLI 実装を確認するとき。

## hash
- 84497f0a0d2660a41158b931a250159397e20e8d81643dd88eac4315ffeb3813

# `enumerate_finding.py`

## Summary
- oracle review finding enumeration の canonical 実装を再公開する互換 import 経路。既存の acp.builder.oracle.review.enumerate_finding 呼び出し元から利用するための薄い委譲対象であり、実装内容を確認・変更するときは参照先の canonical 実装へ進む。

## Read this when
- 既存の acp.builder.oracle.review.enumerate_finding からの import 互換性や再公開対象を確認するとき。

## Do not read this when
- oracle review finding enumeration の実装仕様や処理内容を確認するときは、この互換経路ではなく canonical 実装を直接読む場合。

## hash
- 2da575386b541b2d2404f8d4213b85ea85c7b8204d8c961bec03d8198f646c36

# `judge_finding.py`

## Summary
- 対象は、oracle review の finding judgment 用パラメータ生成関数を canonical 実装へ転送する互換 import 経路である。canonical 実装の移行中に旧 import 経路を確認する入口として扱う。

## Read this when
- oracle review の finding judgment パラメータ生成関数について、旧 `acp.builder.oracle.review.judge_finding` import 経路との互換性や移行状況を確認するとき。

## Do not read this when
- canonical な oracle review の finding judgment 実装そのものを変更・確認するとき。
- oracle review と無関係な builder 実装や、旧 import 経路を利用しない処理を調べるとき。

## hash
- 3e915545cbcdbb4483339b271d5de1d82fee999a4a493f88bcee5ad101729c23

# `merge_finding.py`

## Summary
- oracle review finding merge の互換 import 経路を提供し、対応する oracle 実装のパラメータ生成機能へ進むための入口。

## Read this when
- oracle review finding merge のパラメータ生成機能を、互換 import 経路から利用または確認するとき

## Do not read this when
- 対応する oracle 実装の詳細を確認したいとき
- review finding merge 以外の機能を確認するとき

## hash
- a4d7c7e6d16ff5cc0f6f1ebf56e4a4cd1bc8239b094b3048d8e65376f9ed16a9

# `validate_finding_advocate.py`

## Summary
- oracle review advocate validation の canonical 実装を互換 import 経路として公開する薄いモジュール。review finding advocate の検証パラメータ生成を利用する実装やテストで、従来の src 側 import 経路を確認するときに読む。

## Read this when
- review finding advocate の検証パラメータ生成を src 側の互換 import 経路から利用する必要があるとき
- canonical 実装への再公開関係を確認するとき

## Do not read this when
- 検証パラメータ生成の実際の処理内容、入力条件、出力仕様を確認したいとき。canonical 実装を直接読む
- review advocate validation と無関係な oracle review 機能を調べるとき

## hash
- 461fcbe483378ad0de8724fd04347686c8354d8d1bdd61c89496ba121fb0ee42

# `validate_finding_challenger.py`

## Summary
- oracle review challenger validation の旧 import 経路を互換維持する薄い委譲モジュール。canonical 実装の詳細ではなく、既存 caller からの互換 import が必要な場合の入口として扱う。

## Read this when
- `acp.builder.oracle.review.validate_finding_challenger` からの既存 import を維持・確認する必要があるとき
- 互換 import 経路や canonical 実装への委譲関係を確認するとき

## Do not read this when
- oracle review challenger validation の実装内容を変更・確認するときは、canonical 実装を直接読む
- この互換経路を利用しない新規 caller を実装するとき

## hash
- d786c87e2d221b325dab298f376e2a25e92ac82dc194872d69e6a6df04d8f202

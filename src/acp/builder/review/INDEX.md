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
- review oracle 領域の realization 側互換入口を集めた package。finding の列挙・判定・統合、advocate/challenger 検証の各処理について、主に oracle 側実装の再公開または薄い adapter を提供する。
- この階層自体は review oracle の正本仕様や主要ロジックを保持する場所ではなく、realization implementation 側の import path から oracle 由来の実装へ到達するための境界として位置づく。
- 一部の adapter は oracle 側パラメータ生成を包み、実行側で許容された範囲の prompt placeholder typo 補正だけを行う。

## Read this when
- realization 側から review oracle の finding 列挙・判定・統合・検証機能へ到達する import 経路を確認したいとき。
- この階層のモジュールが独自ロジックを持つのか、oracle 側実装の再公開または薄い adapter なのかを切り分けたいとき。
- merge finding や finding advocate 検証で、oracle 側 prompt 由来の placeholder 表記補正が realization 側のどこで行われるかを確認したいとき。
- review oracle 関連の互換 import path を変更・削除してよいか判断するために、package 境界や再公開入口としての役割を確認したいとき。

## Do not read this when
- review oracle の正本仕様、prompt 本文、Structured Output schema、model 設定、reasoning effort、file access mode を確認したいとき。その場合は対応する oracle 側の仕様文書または実装を読む。
- finding 列挙・判定・統合・検証の具体的なアルゴリズム、入出力、判定基準を理解したいとき。この階層ではなく委譲先の oracle 側実装へ進む。
- review workflow 全体の制御、CLI 入出力、レビュー結果の検証観点、または review oracle 以外の builder 処理を調べたいとき。より上位または該当責務の本文を読む。
- 公開 API の詳細実装、関数・クラス・定数の新規定義、または再公開ではない処理本体を探しているとき。この階層の多くは互換境界としての薄い入口に留まる。

## hash
- cd535c81c0d262808645c95f3a38ac97d7ad94ba8222db6629903a884d244a9c

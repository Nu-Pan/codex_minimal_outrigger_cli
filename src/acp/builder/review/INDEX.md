# `oracle`

## Summary
- `cmoc review oracle` の AI 呼び出しパラメータ構築と Structured Output schema をまとめる領域。
- oracle file のレビュー所見について、新規列挙、擁護理由・反証理由の追加検証、採否判定、重複・矛盾の整理を行う各段階の出力契約と prompt 構築を扱う。
- レビュー対象を oracle file に限定した読み取り条件、既知理由や既存所見との重複回避、review oracle 標準を適用した agent 呼び出し設定を確認する入口になる。

## Read this when
- `cmoc review oracle` で、oracle file から所見候補を列挙し、検証し、採否判定し、整理する一連の agent 呼び出し仕様を追いたいとき。
- レビュー所見、既知の関連所見、既知の肯定理由・否定理由を prompt にどう渡し、重複しない新規情報だけを返させるか確認したいとき。
- oracle file レビュー向けの Structured Output schema と、それに対応する AgentCallParameter の紐付けを実装・テスト・調整したいとき。
- 所見の重大度、根拠、理由、採否、削除・置換・統合といったレビュー結果の構造化された受け渡し境界を確認したいとき。
- oracle file を根拠にした所見の妥当性支持と反証を分けて扱う検証フローを確認したいとき。

## Do not read this when
- oracle file や realization file の基本定義、編集責任、配置ルールだけを確認したいとき。
- 個別の正本仕様断片そのものや、レビュー対象としてどの oracle file を探索するかを調べたいとき。
- `cmoc review oracle` の CLI 入口、実行制御、保存、表示、集約、通知など、agent 呼び出しパラメータ構築より外側の処理を確認したいとき。
- oracle file 以外の realization file レビューや、通常の実装レビュー用 prompt 構築を探しているとき。
- 汎用的な AgentCallParameter、markdown rendering、path 解決、complete prompt 組み立て helper の共通処理だけを調べたいとき。

## hash
- 73e1b62f0387f4c1ad7bf7435affddf77d7905a178c57b525215fa4c2694cf01

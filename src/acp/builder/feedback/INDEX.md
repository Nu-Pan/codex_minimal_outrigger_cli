# `__init__.py`

## Summary
- feedback の issue 正規化・検証に対応する builder adapter パッケージ。対応する oracle 実装を起点に、feedback の normalize／verify 処理を確認する際の入口となる。

## Read this when
- feedback issue の normalization または verification に関する builder adapter の構成を確認するとき
- 対応する oracle の normalize_issue／verify_issue 実装との対応関係を確認するとき

## Do not read this when
- feedback 以外の builder adapter を調べるとき
- 正規化・検証処理そのものの詳細を確認する場合は、対応する oracle file を直接読む

## hash
- 5be652524e2cf162bcb1e9f7afa2fb8fff79cfa9828f6648565cc06ee9728f4c

# `normalize_issue.py`

## Summary
- feedback issue の同一性判断 builder を、canonical builder の互換 import 経路として再公開する対象。canonical prompt を取得し、動的な observation JSON と既存 issue candidate JSON の code fence を保護してから返す。

## Read this when
- feedback issue の同一性判断用 agent call parameter を互換 import 経路から構築するとき。
- canonical prompt の再公開時に、動的 JSON 内の backtick が後続の prompt section を命令として解釈されないよう保護する処理を確認するとき。

## Do not read this when
- canonical な feedback issue 同一性判断 builder の prompt 内容や仕様を確認するときは、対応する oracle file を直接読む。
- 動的 JSON の code fence 保護処理そのものを変更・確認するときは、prompt fence 保護の共通実装を直接読む。
- feedback issue の正規化以外の builder の挙動を確認するときは、この互換 import 経路を入口にしない。

## hash
- c6d131fb7f21aaa97e881a84777bc5f11b0d6178c3dad3543290f0c5e18e970f

# `verify_issue.py`

## Summary
- feedback issue candidate を固定済みの report cut references だけから検証する agent call parameter の互換 import 経路。canonical prompt を再公開し、動的 JSON 内の backtick が後続の prompt section を壊さないよう fence を保護する。

## Read this when
- feedback issue candidate の検証用 agent call parameter 構築経路を確認するとき
- candidate JSON と report cut references JSON の prompt 埋め込み時に code fence 保護が必要な処理を確認するとき

## Do not read this when
- 検証 prompt の正本文面、判定基準、Structured Output schema を確認したいとき
- feedback issue 以外の agent call parameter 構築処理を調べるとき

## hash
- 9dea2003b38f147230346e365b3dca841a88c884a47cd98355bda94be8b86db1

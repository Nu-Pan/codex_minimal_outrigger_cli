# `__init__.py`

## Summary
- 旧来の apply fork 系 import との互換性を保つためだけに残された package。実装本体ではなく、既存参照を壊さないための公開面維持と削除条件を示す。

## Read this when
- 旧来の apply fork 系 import 経路を維持する必要があるか判断するとき。
- 互換 package を削除できるか確認するため、realization 側と利用者向け公開面に同参照が残っているか調べるとき。

## Do not read this when
- apply fork の実処理や挙動を調べたいとき。
- 互換 import 経路ではなく、現行の実装責務や制御ロジックを変更したいとき。

## hash
- 9fbe41ef7b1f6461c182c9c72161a713cf2ce6cd068519b03772412301ad1bc7

# `_common.py`

## Summary
- `cmoc apply fork` の各 builder が共通で使う補助処理を置く。repo root の解決、`oracle/src` を import 可能にするための sys.path 調整、oracle 側の ACP parameter をそのまま受け渡すための薄い変換だけを担当する。

## Read this when
- `cmoc apply fork` 配下の builder から oracle 実装を呼び出す前に、作業ツリーと packaged layout のどちらでも `oracle` を import できるようにしたいとき。
- fork 系 builder の中で、repo root の決定方法をそろえたいとき。
- oracle 側の builder が返した `AgentCallParameter` を realization 側の公開型としてそのまま返す経路を確認したいとき。

## Do not read this when
- 個別の fork builder が何を構築するかを知りたいときは、それぞれの builder 本体を読む。
- `cmoc apply fork` 以外のサブコマンドや、oracle 以外の import 解決を変えたいときは読む対象ではない。
- `INDEX.md` のルーティング規則そのものを確認したいときは、この補助ファイルではなく該当階層の案内を読む。

## hash
- 921e1b602f59bee1303b21e22c887f86b0f50fd9bffcce8b377fdc2a309ac493

# `change_summary.py`

## Summary
- `cmoc apply fork` の変更要約用 agent call parameter を組み立てる入口。作業レポート向けの変更要約を作るときに読む。正本側の `oracle.acp_builder.apply.fork.change_summary` を参照して実体を委譲するため、ここでは委譲の流れだけを確認すればよい。

## Read this when
- `cmoc apply fork` の変更要約を作る処理の入出力や、どの正本実装に渡しているかを確認したいとき。

## Do not read this when
- `cmoc apply fork` の変更要約の正本仕様そのものを確認したいときは、対応する oracle 側を見る。変更要約以外の fork 系変換や共通処理を追いたいときも、まずはそれぞれの直接の入口を読む。

## hash
- 83474b219a58ee86b8aa07876c6e7e7ca83df70e821edef6a6e35e15cc907aa9

# `file_finding_enumeration.py`

## Summary
- `cmoc apply fork` の所見列挙向け agent call parameter を、実装側から正本の oracle 実装へ委譲して組み立てる入口。`cmoc apply fork` のファイル単位の所見列挙を扱う場合に読む。

## Read this when
- `cmoc apply fork` のファイル単位の所見列挙用 parameter 生成の入口を探している。
- oracle 側の parameter 生成結果を realization 側へ適合させる委譲処理を確認したい。

## Do not read this when
- 所見列挙の実際の判定ロジックや oracle 側の仕様を確認したい場合は、対応する oracle src を読む。
- `cmoc apply fork` の他の種別の parameter 生成や共通補助を探している場合は、同階層の別モジュールを読む。

## hash
- 80dc02e710af633432c40df6016f61908adb063d17bbb25471a955ba13b6f7fc

# `finding_application.py`

## Summary
- `cmoc apply fork` の所見適用用 agent call parameter を組み立てる入口。所見の list を受け取り、`oracle` 側の正本実装を import できる状態にしたうえで、その結果を realization 側へ適用するための変換だけを担う。

## Read this when
- `cmoc apply fork` で使う所見適用用の parameter 構築経路を確認したいとき。
- oracle 側の所見適用ロジックを呼び出す前提づくりや、realization 側への適用変換を追いたいとき。

## Do not read this when
- 所見内容そのものの解釈や生成ルールを確認したいときは、対応する oracle 側の正本実装を読む。
- 他の apply 系や fork 以外の agent call parameter 構築を追いたいときは、この入口ではなく該当する各モジュールを読む。

## hash
- 5cab8ad94b55b3e1e931423f52d74aaf3641ae04db265e97fa272bd79d32cd97

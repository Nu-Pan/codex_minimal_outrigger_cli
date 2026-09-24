# `__init__.py`

## Summary
- editing run の共通 lifecycle サブコマンド群を示すパッケージの入口。個別の処理や共通 helper の実装説明は担わない。

## Read this when
- editing run の lifecycle サブコマンド群を調べ始め、対象となるパッケージの範囲を確認したいとき。

## Do not read this when
- join や abandon の具体的な挙動を調べるときは各サブコマンドの実装へ進む。
- lifecycle helper の処理を調べるときは共通 runtime の実装へ進む。

## hash
- ee750515c16235f73dd57b6cd7864576f1957fe840d0ceb82b9658c56c959115

# `abandon.py`

## Summary
- active editing run を merge せずに破棄する `cmoc run abandon` の処理を担い、run の停止、資源の cleanup、state と lifecycle report の更新を行う。
- run の成果を session に取り込む処理や、session branch 自体を破棄する処理とは役割が異なる。

## Read this when
- 未 join の編集 run を破棄したいとき、または run join 後に残った run 資源の cleanup を再試行したいとき。
- active run の停止・cleanup の流れや、cleanup 完了後の state と report の扱いを調べるとき。

## Do not read this when
- run の変更を session に取り込む処理を調べるときは `cmoc run join` を読む。
- active session branch を home branch に戻して session 自体を破棄する処理を調べるときは `cmoc session abandon` を読む。

## hash
- 29fd9914e21a565b72ca6f751d807e0e02c536d75c51fa1776e5c001ff79c873

# `join.py`

## Summary
- `cmoc run join` の実行ライフサイクルをまとめ、active run の確認、共通 merge 処理の呼び出し、join 固有の state・report 更新、失敗時の復旧と cleanup を調整する。
- 差分検査や merge の共通処理は runtime helper に委譲し、run の破棄処理は別の lifecycle に分かれている。

## Read this when
- `cmoc run join` の実行順序や `--force-resolve`、join 後の state・report、失敗時の復旧や cleanup pending の扱いを確認・変更するとき。
- 共通 merge 処理の結果を join 側で run の種類ごとにどう反映するか追うとき。

## Do not read this when
- 差分検査、merge conflict 解決、INDEX 更新など共通処理の実装だけを調べるときは、それらを担う runtime helper を直接読む。
- run の停止や worktree・branch の破棄だけを調べるときは、abandon の lifecycle を読む。
- CLI コマンドや option の登録だけを調べるときは、コマンド定義を読む。

## hash
- 908869cb009c6790fd268053eeaccff300bc032e82c401427c6a2c302692be34

# `lifecycle.py`

## Summary
- 編集 run の共通 helper を旧 import 経路から利用するための互換 shim。型と関数を共通実装から再公開し、session-path 判定 helper では `base` 省略を受け付けて共通実装へ委譲する。

## Read this when
- 旧 import 経路の公開内容や互換性を確認するとき。
- session-path 判定 helper の `base` 省略呼び出しが維持されているか確認するとき。

## Do not read this when
- 編集 run の開始、state 遷移、commit、差分判定など、実動作の仕様や変更先を調べるときは共通実装へ進む。
- join・abandon・report のコマンド固有の処理を調べるときは、それぞれのコマンド実装へ進む。

## hash
- fdb88ac943650b370240fd73bacf3729399025ad99668bc0c35571ab5624a017

# `report.py`

## Summary
- editing run の fork/lifecycle report writer を共通実装から再公開し、旧 import 経路との互換性を保つ薄い shim。

## Read this when
- 旧来の import 経路の互換性や、この shim が再公開する report writer の所在を確認するとき。
- 呼び出し側の移行後に、この互換 shim を削除できるか判断するとき。

## Do not read this when
- report の生成内容や保存動作を調べたり変更したりするときは、実処理を担う共通実装を直接確認する。

## hash
- 79d887b69a865829ca361e6b448106bb8eb6e3635afa5c7300dc31a99beb8385

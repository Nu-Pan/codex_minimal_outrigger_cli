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
- `cmoc run join` の制御フローをまとめ、active run の確認から共通の検査・merge 処理の呼び出し、join 固有の state・report 更新、失敗時の復旧と cleanup までを調整する。
- join の成功・失敗・cleanup pending を通じた全体の状態遷移を追う入口となる。

## Read this when
- `cmoc run join` の実行順序や active run の条件、join 固有の state・report 更新を調べるとき。
- merge 後の処理に失敗した場合の復旧や、確定済み merge と cleanup pending の扱いを確認するとき。

## Do not read this when
- 差分検査や `--force-resolve` の詳細、conflict resolution、共通 merge・hook・cleanup の実装を調べるときは、共通の join runtime 処理から読む。
- run の破棄や、join 後に残った資源の cleanup 再試行を調べるときは、abandon の処理から読む。

## hash
- a7c43f8b9e7f8f5fac5ef922a7217ef64aa20cf4b3f84f78d728f346676dd7a6

# `lifecycle.py`

## Summary
- editing run の開始・状態遷移・差分処理などの共通 helper を旧 import 経路から再公開する、実装を持たない互換 shim です。

## Read this when
- 旧 import 経路の互換性や、そこから利用できる共通 lifecycle helper を確認するとき。

## Do not read this when
- 共通 lifecycle の具体的な挙動を調べたり変更したりするときは、正規実装を直接確認してください。
- run join や abandon の制御フローを調べるときは、それぞれのサブコマンド処理を確認してください。

## hash
- 4ce7349f863f1a9083e0bb8ae92f3d8b2d783364feae53a5f2b947dbe5e87145

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

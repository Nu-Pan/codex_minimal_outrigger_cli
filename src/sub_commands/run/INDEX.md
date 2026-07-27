# `__init__.py`

## Summary
- editing run の共通 lifecycle サブコマンドをまとめるパッケージの入口。関連する run サブコマンドの共通処理を確認する際に読む。

## Read this when
- editing run サブコマンドの共通 lifecycle や、その配下の実装を調査・変更するとき。

## Do not read this when
- editing run 以外のサブコマンドを扱うとき。具体的な処理の実装を確認する場合は、この入口ではなく配下の該当ファイルを直接読む。

## hash
- ee750515c16235f73dd57b6cd7864576f1957fe840d0ceb82b9658c56c959115

# `abandon.py`

## Summary
- `cmoc run abandon` の active editing run を停止・破棄する CLI runtime 実装。process の停止、run worktree と branch の cleanup、state の ready 化、lifecycle report の出力、結果表示を扱う。

## Read this when
- `cmoc run abandon` の cleanup lifecycle、running/error state の process 停止、run worktree・branch の削除、abandon 後の state/report を調査・変更するとき。

## Do not read this when
- 通常の run 開始・継続・完了処理を調査するとき。process tracking や lifecycle report の共通仕様だけを確認する場合は、それぞれの commons 実装を直接読む。

## hash
- 88b98c33afe0508f2e45f041528d705b178dd7da2d1da16e5127f79bbb26707b

# `join.py`

## Summary
- `cmoc run join` の active editing run 終了処理を一貫して扱う実装。join 前の doctor 処理、session/run branch の差分検査、想定外差分の拒否または force-resolve、merge、INDEX.md conflict の限定解決、post-join hook と refactor state 同期、report 保存、失敗時 rollback と error state 化、worktree・branch cleanup を担う。run join の lifecycle 不変条件や失敗復旧を確認する際の入口。

## Read this when
- `cmoc run join` の実装や CLI 挙動を変更・調査するとき
- run branch の merge、`--force-resolve`、INDEX.md conflict 処理を確認するとき
- join 後の state 同期、report、cleanup、失敗時 rollback を追跡するとき
- active run の joinable/error state と session/run worktree の差分検査を確認するとき

## Do not read this when
- run の開始・編集・abandon など join 以外の lifecycle を直接調べるとき
- workload 固有の処理や merge 対象ファイルの生成ロジックを調べるとき
- refactor state 同期や lifecycle report の共通実装そのものを変更・調査するときは、各共通モジュールを直接読む場合
- doctor preprocess の仕様だけを確認するときは、対応する oracle document を直接読む場合

## hash
- 60554582870b8434f16548704c86c92dd43989df15c3d913df64d473fe0e29a4

# `lifecycle.py`

## Summary
- editing run 共通 helper の旧 import path を維持する互換 shim。実体は commons.runtime_run_lifecycle にあり、関連する型・ライフサイクル操作を再公開する。

## Read this when
- editing run のライフサイクル処理や旧 import path との互換性を確認・変更するとき。

## Do not read this when
- 共通ライフサイクル処理そのものを実装・変更する場合は、commons 側の canonical 実装を直接読むとよい。

## hash
- 3de456333531bc878de445ccbaf683410ad0990c75f16028b6bcab36ac7d5939

# `report.py`

## Summary
- editing run report writer の旧 import path を維持する薄い互換 shim。共通実装を再公開し、対応する INDEX entry は互換性が不要になった時点で削除対象となる。

## Read this when
- 旧 import path から run report writer を利用するコードの互換性や移行を確認するとき。
- fork report または lifecycle report の writer の参照先を確認するとき。

## Do not read this when
- canonical な report writer の実装詳細を確認したいときは、commons 側の実装を直接読む。
- run サブコマンドの実行フローや report 生成仕様を調査するとき。

## hash
- 633bf26dd4d3ab3155dcddf2eb46c2b39b1617fa4914e30aeeca6e9cc0975d48

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
- `cmoc run abandon` の active editing run を安全に停止・破棄する CLI runtime。run 状態に応じたプロセス停止、run worktree と branch の削除、state の ready 化、process tracking の削除、lifecycle report の出力、結果表示までを一貫して扱う。

## Read this when
- `cmoc run abandon` の停止・cleanup lifecycle を変更または調査するとき
- running、error、joinable 各状態での process 停止や残存 child cleanup を確認するとき
- run worktree・branch・state・process tracking・lifecycle report の更新順序や失敗時挙動を確認するとき

## Do not read this when
- `run abandon` 以外の run サブコマンドの通常処理だけを調査するとき
- lifecycle report の共通仕様や active run 解決の詳細を確認することが目的のときは、対応する共通 runtime module を直接読む

## hash
- 7d64b59a60a2db6142ee9519f505a82d2df36506eb060b52e217971fdc6293c6

# `join.py`

## Summary
- `cmoc run join` の active editing run を session branch へ統合する一連の lifecycle を担当する。merge 前の差分検査、想定外差分の処理、merge conflict 対応、post-join hook、refactor state 同期、report 保存、run worktree・branch の cleanup、失敗時 rollback と error state 化を扱う。run join の成功・失敗・cleanup pending に関する実装を読む際の入口となる。

## Read this when
- `cmoc run join` の挙動、merge、force-resolve、post-join state 同期、report、cleanup を変更・調査するとき
- run join 失敗時の rollback、error state、INDEX.md 限定 conflict 処理を確認するとき
- active run の想定外差分検査や run resource cleanup の制御を追うとき

## Do not read this when
- run の開始・編集・abandon など join 以外の lifecycle を直接調査するとき
- 共通の git 操作、state 操作、report 生成の詳細だけを確認したいときは、対応する commons runtime module を先に読む
- INDEX.md の生成処理そのものや refactor state 同期の一般仕様だけを調査するとき

## hash
- 06c621e4f69c1412a7940e088eb2ea54dccb9b9b7ebcb9f57d940a48f68b4be1

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

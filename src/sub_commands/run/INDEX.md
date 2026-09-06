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
- `cmoc run abandon` の active editing run を停止し、run worktree・branch・state・process tracking を cleanup して ready 状態へ戻すライフサイクル実装。
- running・error・joinable の状態ごとに process や残存 Codex child を停止し、worktree と branch の削除結果を検証して lifecycle report と terminal result を確定する。

## Read this when
- `cmoc run abandon` の停止、破棄、cleanup 成否、警告、または ready 状態への遷移を確認・変更するとき。
- run worktree／branch の削除や process tracking の扱い、状態別の停止処理を追跡するとき。

## Do not read this when
- active run の通常実行・join・編集処理を確認したいとき。
- cleanup 実装ではなく、run lifecycle の状態解決や report 生成の共通仕様を直接確認したいとき。

## hash
- 22e1710f8c5f8744e0406c2bda7b38f69fee7199c62b3c506918fd389b7fc0a9

# `join.py`

## Summary
- `cmoc run join` の active editing run を対象に、差分検査、merge、post-join の INDEX・refactor state 同期、report 保存、state 更新、run 資源 cleanup までの共通 lifecycle を扱う。
- join の成功・失敗・cleanup pending にまたがる state と rollback の不変条件を確認するための入口である。

## Read this when
- `cmoc run join` の実行フロー、merge 前の clean・想定外差分検査、`--force-resolve` の復旧動作を確認または変更するとき
- merge 後の post-join hook、INDEX 再生成、refactor state 同期、lifecycle report、active run state の遷移を確認するとき
- merge conflict、post-join failure、report 保存失敗、worktree・branch cleanup failure の rollback と再試行条件を調べるとき

## Do not read this when
- workload 固有の編集処理や run の開始・abandon など、`cmoc run join` の共通 lifecycle より直接担当する別の実装を確認するとき
- INDEX.md の生成規則そのもの、refactor state の同期規則そのもの、または lifecycle report の書式だけを確認するときは、それぞれの専用実装を直接読む

## hash
- 7424843df552d068123dc689575b380aa6240eb87aa83f6d1468b900d16a4408

# `lifecycle.py`

## Summary
- editing run 共通 lifecycle helper の旧 import path を維持する薄い互換 shim。canonical な共通実装を再公開し、旧 path 固有の session path 判定呼び出しを commons 側へ委譲する。

## Read this when
- editing run の lifecycle 操作を旧 import path から利用するコードの互換性や公開 helper を確認するとき
- 旧 shim から canonical 実装へ移行する際に、再公開されるシンボルと委譲される session path 判定を確認するとき

## Do not read this when
- lifecycle 処理の本体仕様や新規変更を確認したいとき（commons 側の canonical 実装を直接読む）
- editing run の lifecycle helper の旧 import path 互換性が関係しない処理を調べるとき

## hash
- fdb88ac943650b370240fd73bacf3729399025ad99668bc0c35571ab5624a017

# `report.py`

## Summary
- 旧 import path から利用される editing run report writer の互換 shim。
- 共通処理の canonical 実装を再公開し、旧利用者が commons 側へ移行するまで互換性を保つ。
- 旧 import path の互換性や shim の削除条件を確認する際の入口であり、実装本体は commons 側にある。

## Read this when
- 旧 import path から run report writer を利用するコードの互換性を確認するとき。
- fork report または lifecycle report の writer の公開元を追跡するとき。
- commons 側への移行完了後に、この shim と対応する INDEX entry の削除可否を判断するとき。

## Do not read this when
- fork report または lifecycle report の具体的な実装内容を確認したいとき。
- 共通処理の挙動を調査・変更するとき。
- 旧 import path の互換性に関係しない run サブコマンドの処理を確認するとき。

## hash
- 79d887b69a865829ca361e6b448106bb8eb6e3635afa5c7300dc31a99beb8385

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
- `cmoc run abandon` の実装。active editing run を特定し、running process の停止、run worktree と branch の削除、state の ready 化、lifecycle report の出力、結果表示までの cleanup lifecycle を担う。run abandon の挙動や cleanup 失敗時の扱いを確認する入口。

## Read this when
- `cmoc run abandon` の実装・エラー処理・cleanup lifecycle を調査または変更するとき
- active run の process、worktree、branch、state、report が abandon でどう扱われるか確認するとき

## Do not read this when
- run の開始・継続・完了処理を調査するとき
- 共通の process ID、run lifecycle lock、active run 解決処理そのものを調査するときは、対応する `commons` 実装を直接読む

## hash
- c0182183cf26c59d5604f4d4b8fba97d01ca381447eba3f52b8bbfc594a01cec

# `join.py`

## Summary
- `cmoc run join` の active run 統合ライフサイクルを担当する。run branch と session branch の差分検査、merge、INDEX.md conflict の解決、post-join state 同期、report 保存、worktree・branch cleanup、および失敗時 rollback/error 化を扱う。run join の処理全体を確認する入口であり、個別の git・state・report helper の実装そのものを調べる対象ではない。

## Read this when
- `cmoc run join` の成功・失敗時の制御フローを調査または変更するとき
- run branch の想定外差分、merge conflict、`--force-resolve` の挙動を確認するとき
- post-join hook、state 同期、lifecycle report、run 資源 cleanup の連携を確認するとき
- merge または post-join 処理の失敗後に session を復元して error state にする挙動を確認するとき

## Do not read this when
- run join 以外のサブコマンドのライフサイクルだけを調べるとき
- git 操作、state 操作、process tracking、report 出力の共通実装だけを調べるときは、それぞれの helper module を直接読む
- join の利用者向け仕様や state の正本定義を確認するときは、対応する oracle doc を先に読む

## hash
- 7df92d2ceb682e728f9430beec54b772292d83a7d9d6df570b62cd52f276b8a8

# `lifecycle.py`

## Summary
- editing run のライフサイクル共通型・処理を commons から再エクスポートし、旧 import path との互換性を保つ薄い shim。

## Read this when
- editing run の旧 import path の互換性や、ライフサイクル関連の再エクスポート対象を確認するとき。

## Do not read this when
- canonical な共通実装の挙動や配置規則を確認したいときは、commons 側の実装と関連する oracle を直接読む。
- 旧 import path の互換性が不要になり、shim の削除可否だけを判断するとき。

## hash
- b5f3d0a269df7dec273e15fca5c9c6c79d2627656b67cc0a2f8cb171d26687ea

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

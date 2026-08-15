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
- `cmoc run abandon` の実装本体。active editing run を特定し、running・error・joinable の状態に応じてプロセスや Codex child を停止する。
- run worktree と run branch を削除し、cleanup 成否を primary report と lifecycle report に記録する。cleanup 完了時は state を ready に戻し、process tracking を削除して terminal result を返す。
- worktree または branch の削除に失敗した場合は state を保持したままエラーを返し、再実行可能な警告と詳細を提示する。

## Read this when
- `cmoc run abandon` の cleanup lifecycle、active run の停止処理、run worktree・branch の破棄動作を確認するとき。
- running・error・joinable state ごとの process cleanup と、cleanup 成否に応じた state・report 更新を調べるとき。
- abandon 後の terminal result、warning、primary report、lifecycle report の生成経路を確認するとき。

## Do not read this when
- run の通常作成・編集・join 処理を確認するときは、対応する run lifecycle や editing 実装を直接読む。
- doctor preprocess の仕様や一般的な worktree 操作だけを確認するときは、参照されている oracle または runtime 共通実装を直接読む。
- `cmoc run abandon` の挙動を変更しない利用者向けの一般的な CLI 案内を作成するとき。

## hash
- c3c9ab6f4f1059a44bc54a8e5846cfdce958985ab838f833950df9976b916509

# `join.py`

## Summary
- `cmoc run join` の active editing run を session branch へ統合する一連の lifecycle 実装。merge 前の差分検査、`--force-resolve` による想定外 run 差分の復元、INDEX.md だけを許可する conflict 解決、post-join hook、refactor state 同期、report 保存、run resource cleanup を扱う。
- merge または post-join 処理の失敗時に session worktree と run state を rollback し、error state と report を残して再試行可能にする責務も含む。run join の成功・失敗・cleanup pending の状態遷移や、run process tracking と cleanup の挙動を確認する際の実装入口である。

## Read this when
- `cmoc run join` の merge、差分検査、`--force-resolve`、INDEX.md conflict 処理を変更または調査するとき。
- join 後の post-join hook、refactor state 同期、lifecycle report、run worktree・branch cleanup の挙動を確認するとき。
- join 失敗時の rollback、error state、cleanup pending、run process tracking の不変条件を確認するとき。

## Do not read this when
- `cmoc run join` 以外の subcommand の固有処理だけを変更または調査するとき。
- INDEX.md の生成規則そのものや、join lifecycle を呼び出す共通 runtime API の仕様を直接確認するときは、それぞれの実装・仕様対象から読み始める場合。

## hash
- 441d2a3f856e726f89c6d9d326755fa2cd718e0f239d5911684e06d4012f3090

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

# `__init__.py`

## Summary
- cmoc の共有ランタイム helper 群に属するパッケージ入口であることを示すだけの、ごく小さい初期化本文。現時点では公開 import や初期化処理を持たず、この階層の実処理へ進む前にパッケージ全体の位置づけを確認するための入口になる。

## Read this when
- 共有ランタイム helper 群のパッケージ境界や、この階層が cmoc の共通実行時支援を扱う領域かを確認したいとき。
- パッケージ読み込み時に実行される初期化処理や、上位へ再公開される名前があるかを確認したいとき。

## Do not read this when
- 個別の helper 関数、クラス、定数、具体的な runtime 挙動を調べたいとき。その場合は同階層の実装本文へ進む。
- 共有 helper の仕様、テスト観点、または呼び出し元での使われ方を調べたいとき。この本文だけではそれらの根拠にならない。

## hash
- 7dba2bba25cf07b27346cef2bc3541a7faac13254b97577482a98e2046a63f45

# `cmoc_runtime.py`

## Summary
- cmoc の実行時共通基盤を集約する実装。例外表現、サブコマンドログ、git 操作、branch/session state、`.cmoc` 配下の保存先、設定 JSON 変換、worktree 操作、Codex CLI 呼び出し、quota/capacity retry、structured output 検証、hash・binary・gitignore 判定を扱う。
- 複数サブコマンドから使われる低レベルな副作用付き処理の入口であり、個別コマンド固有の手順ではなく、repository state・Codex CLI 実行・永続補助ファイルを扱う共通処理を確認するための対象。

## Read this when
- git command の実行、branch 判定、clean worktree 要求、managed branch 判定、worktree 作成・削除、branch 削除の挙動を確認または変更する。
- session state の構造、session/apply branch からの session-id 抽出、state file の読み書き、active session 検索を確認または変更する。
- `.cmoc` 配下の config、session、report、log、worktree、schema 保存先や `.gitignore` への `.cmoc` 除外処理を扱う。
- cmoc config の dict 変換、JSON 読み込み、既定値同期、不正設定時のエラー化を確認または変更する。
- Codex CLI を subprocess として呼び出す処理、profile 生成、CODEX_HOME 検証、structured output schema の準備、stdout/stderr/output/call log の記録を扱う。
- Codex CLI の capacity retry、quota polling、resume token 抽出、quota wait の共有制御、呼び出し結果の検証失敗時 retry を確認または変更する。
- CmocError の構造、利用者向けエラー表示、subcommand logger の event 記録、実行時間・quota 待ち時間の記録を扱う。
- file hash、text hash、binary 判定、git ignore 判定など、複数箇所で使う小さな runtime helper の挙動を確認する。

## Do not read this when
- 個別サブコマンドの CLI 引数、コマンド固有の処理順、利用者向け出力 schema を確認したいだけの場合は、そのサブコマンド実装や対応する schema を直接読む。
- config dataclass や AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort の定義そのものを確認したい場合は、それらの定義元を読む。
- oracle file や oracle standard の正本仕様内容を確認したい場合は、oracle 側の本文を読む。
- path keyword の定義や `<cmoc-root>` などの用語モデルを確認したい場合は、path model の定義元を読む。
- テスト観点や既存テストケースを探す場合は、対応する test 側の対象を読む。
- 純粋な文字列整形、JSON schema 本体、または command 固有の prompt 生成だけを変更する場合は、この共通 runtime に触れる必要があるかを先に絞り込む。

## hash
- 39b6bd90422efaf685ba124593d38830e9ff9bd528e6528b8806993f81b44464

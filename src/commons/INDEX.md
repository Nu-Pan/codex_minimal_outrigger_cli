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
- cmoc の実行時共通基盤をまとめる実装。共通エラー型、外部コマンド結果、Codex 呼び出し結果、subcommand ログ、session/apply 状態、設定の読み書き、管理 branch 判定、worktree 操作、実行用パス、Codex profile 生成、Codex CLI/TUI 呼び出し、quota/capacity retry、schema 検証、hash・binary・ignore 判定を扱う。
- 複数の subcommand から共有される低レベルな実行補助を集約しており、個別 command の業務フローではなく、git・filesystem・設定・状態・Codex 実行を支える入口として位置づけられる。

## Read this when
- cmoc の共通エラー表示、失敗時の次アクション、例外整形、または外部コマンド失敗の扱いを確認・変更したいとき。
- repository root、cmoc root、session/report/log/worktree/schema/config など、実行時に使う標準的な保存場所やパス生成規則を確認・変更したいとき。
- 管理 branch の判定、session id の抽出、session/apply 状態ファイルの読み書き、active session の探索を扱うとき。
- git command 実行、clean worktree 要求、branch 存在確認、worktree 作成・削除、branch 削除、git ignore 判定など、git 操作の共通 helper を扱うとき。
- cmoc config の dict 変換、読み込み、同期、書き込み、既定値補完、型変換エラーを扱うとき。
- Codex home の解決・検証、Codex profile の生成、file access mode から sandbox mode への変換、Codex subprocess 環境の構築を扱うとき。
- Codex CLI/TUI 呼び出し、JSONL/stdout/stderr/output/call log、structured output schema、semantic retry、capacity retry、quota polling/resume、subcommand logger 連携を調べるとき。
- 内容 hash に基づくファイル生成、sha256 計算、binary 判定の共通処理を扱うとき。

## Do not read this when
- 個別 subcommand の利用者向け手順、引数定義、command 固有の orchestration を知りたいだけなら、該当 command の実装を直接読む。
- AgentCallParameter、FileAccessMode、ModelClass、ReasoningEffort など agent 呼び出しパラメータそのものの定義を確認したいだけなら、その定義元を読む。
- 設定 dataclass の項目定義や既定値そのものを確認したいだけなら、設定モデルの定義元を読む。
- oracle の正本仕様、path keyword の仕様説明、INDEX 生成規則を確認したいだけなら、対応する oracle document を読む。
- テストケースの期待値や外部挙動の検証観点を確認したいだけなら、対応する test を読む。
- 特定の report や log の内容を調べたいだけなら、生成物そのものを読む。

## hash
- b2146b3bb52f70a7b4b86e6e652b0ed6753bd4aa846fd9420e3dc72a5dc577b9

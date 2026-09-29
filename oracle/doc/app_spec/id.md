# 共通 ID

共通 ID は、種類ごとの発行順を名前の辞書順で追え、文字列から発行日時も読める識別子とする。本書は書式、プレフィックス、採番・順序保証、および適用範囲を所有する。各 ID の識別対象と発行・引継ぎの時点は、「プレフィックス」に示す個別仕様を正本とする。

## ID のフォーマット

ID は `<プレフィックス>_<6桁の36進通番>_YYYY-MM-DD_HH-mm` 形式とする。例えば、`exec_000010_2026-09-29_15-04` となる。

- プレフィックスは、本書の「プレフィックス」に従う。
- 通番は、数字 `0123456789abcdefghijklmnopqrstuvwxyz` をこの順に用いる小文字の36進数とし、6 桁固定でゼロ埋めする。採番は本書の「採番と順序保証」に従う。
- 日時部分は、ID の発行確定時の年月日時分を、実行マシンのローカルタイムゾーンで表す。`YYYY` は年を 4 桁、`MM`、`DD`、`HH`、`mm` は月、日、時、分をそれぞれ 2 桁でゼロ埋めする。時は 24 時間表記とし、秒以下は含めない。
- プレフィックスと通番、通番と日付、および日付と時刻の間は `_`、日付内と時刻内の区切りは `-` とする。

日時単独の表記は、`{{cmoc-root}}/oracle/doc/app_spec/timestamp.md` の「タイムスタンプのフォーマット」を正本とする。ID の日時部分は本節で独立に定義し、そのタイムスタンプの継承や切り詰めとしては定義しない。

## プレフィックス

| プレフィックス | 対象 | 識別対象・発行・引継ぎの正本 |
|---|---|---|
| `exec` | 最外側のサブコマンド実行 | `{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」 |
| `sess` | cmoc の session | `{{cmoc-root}}/oracle/doc/app_spec/sub_command/session_fork.md` の「実行手順」と「`{{cmoc-session-branch}}` の命名規則」 |
| `run` | 編集 run | `{{cmoc-root}}/oracle/doc/app_spec/sub_command/editing_run.md` の「共通開始処理」 |
| `ac` | agent call | `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「基本」 |
| `cc` | Codex call | `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「基本」 |
| `eit` | editor input の handoff target | `{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「handoff target」 |
| `fbr` | feedback run | `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「feedback run」 |
| `fbg` | feedback の active generation | `{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「active generation」 |
| `fbo` | agent が提出した observation | `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「保存単位」 |

## 採番と順序保証

採番の管理単位は、`{{repo-root}}` とプレフィックスの組とする。同じ repository に属するターミナル、process、session、run、および worktree は、そのプレフィックスの通番を共有する。別のプレフィックスは独立に採番する。

- 採番は `000000` から開始し、`zzzzzz` までの 2,176,782,336 通りを使用する。例えば、`000009` の次は `00000a`、`00000z` の次は `000010` となる。
- 同じ管理単位では、発行確定順に通番を増加させる。欠番は許容するが、発行済み番号を再利用してはならない。
- 日付変更、再起動、実行失敗、ログ削除、または branch 切替によって採番をリセットしない。並行発行でも重複を防ぎ、確定済み番号は異常終了後にも再利用しない。
- `zzzzzz` の次は発行失敗とする。折り返しや自動的な桁追加は行わない。呼出し元への影響は、各機能の既存エラー契約に従う。

同じ repository・同じプレフィックスの ID 同士では、辞書順と発行確定順の一致を保証する。比較は `0–9`、`a–z` の文字順とし、数字列を数値として扱う自然順ソートは保証対象外とする。異なるプレフィックスを混ぜた一覧は種類別に並び、種類をまたぐ発行順や、異なる repository 間の発行順は保証しない。

同一分内の複数発行でも通番によって識別と順序を維持する。時計が巻き戻って日時部分が小さくなった場合も、その時点の日時を記録し、通番によって順序を維持する。完了順やファイル最終更新順は保証しない。

採番状態の保存場所・形式、排他方式、および使用 API は、以上の結果を満たす範囲で実装裁量とする。日時単独の表記との仕様上の独立性は、内部実装での日時処理の共用を禁止しない。

## 適用範囲

本書の共通規則は、「プレフィックス」で適用を明示した ID に使用する。発行は cmoc の管理処理が担い、呼び出される agent の指示文へ発行責務を移さない。

Codex が返す session ID、Git commit ID、hash から決定する issue ID、および event から決定する machine observation ID は、それぞれの生成契約に従う。共通 ID に置き換えない。

プレフィックスや通番から、親子関係、target の有効性、処理成功、または現在有効な publication を推定してはならない。対応記録、登録状態、current pointer など、各機能の判断契約を使用する。collector の受理順序は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_state.md` の「high-watermark」に従う。

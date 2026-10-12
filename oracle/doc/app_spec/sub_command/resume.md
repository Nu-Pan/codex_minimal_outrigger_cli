# `cmoc resume <exec-id>`

## 目的と公開入口

終了済みの cmoc 実行を実行 ID で指定し、その実行の Codex TUI の会話を、元の workload の制約で続ける。公開再開入口は `cmoc resume <exec-id>` だけとする。`cmoc tui` と `cmoc oracle investigation` に個別の再開オプションを設けない。

必須の位置引数は再開元の実行 ID 一つとし、TUI 種別や Codex session ID をユーザーに再指定させない。実行 ID の書式と採番は、`{{cmoc-root}}/oracle/doc/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。

本書で TUI 種別とは、会話を続ける workload の種類を指す。今回実際に呼び出された最外側のサブコマンドは常に `cmoc resume` であり、解決した TUI 種別でその記録を置き換えない。

## ログからの種別解決

cmoc は、呼び出し元と同じ repository の指定実行 ID に対応するサブコマンドログを読む。保存先と機械可読な記録の意味は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「サブコマンドログファイル」「TUI 再開のための実行記録」を正本とする。

| ログに記録された最外側のサブコマンド | 解決する TUI 種別 |
|---|---|
| `cmoc tui` | 汎用 TUI |
| `cmoc oracle investigation` | oracle 調査 TUI |
| `cmoc resume` | その実行に保存された解決済みの TUI 種別 |
| その他 | 非 TUI の実行として拒否する |

解決は構造化された記録だけで決定論的に行う。サブコマンドと保存された TUI 種別の矛盾、未知の種別、必要な情報の欠落を推測で補わない。agent による推論、自由文の解析、ファイルの時刻順、または非対話の `codex exec resume` の実行歴を判定根拠にしない。

## 対象の適格性と会話選択

対象は、exec とその TUI process の終了を確認でき、その process の終了時に開いていた主会話を一意に特定できる実行とする。正常終了だけでなく、この条件を満たす異常終了も対象とする。

- 主会話は、TUI 内で会話を切り替えた場合も含め、終了時点の Codex session ID で選ぶ。最初に取得した ID や再開要求時の ID を、終了時の主会話が確認済みであることの代わりに使わない。
- 実行中、終了確認不能、TUI 未起動、主会話未確定の実行は拒否する。ログの欠落・破損・解釈不能・対応の不整合、Codex session ID の不明も拒否理由とする。
- `cmoc resume` の実行 ID も同じ条件で次の再開元にできる。その実行自身のログから種別と主会話を特定できるものとし、過去の再開元ログを連鎖的にたどらなければ解決できない記録にしない。
- 同じ実行 ID を後日再指定した場合は、そこに記録された会話のその時点の続きへ戻る。指定 exec の終了時点へ会話や作業状態を巻き戻す意味ではない。
- 機能導入前の実行も、必要な記録が存在する場合だけ対象とする。不足情報を推測する互換処理は要求しない。

## workload と起動環境の保持

汎用 TUI の制約は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/tui.md` の「全バックエンド共通」を正本とする。oracle 調査 TUI の制約は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md` の「TUI 起動パラメータ」「調査結果と変更の扱い」を正本とする。再開によって、これらの作業範囲やファイルアクセスの権限を拡張しない。

保存された agent call 種別と file access mode を維持し、解決した workload の builder の選択値と一致することを起動前に確認する。一致しない場合は値を上書きして合わせず、制約を保持できないものとして拒否する。再開用パラメータの正確な構造は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「基本」で委譲した oracle src に従う。workload ごとの正確な構築は、次の builder へ委譲する。

- 汎用 TUI: `{{cmoc-root}}/oracle/src/oracle/acp_builder/tui/launch_tui.py` の `build_tui_launch_tui_parameter`。元の agent call 種別と制約を持つ、初期 prompt なしの再開パラメータを構築する。
- oracle 調査 TUI: `{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py` の `build_oracle_investigation_launch_tui_parameter`。調査 workload の agent call 種別と制約を保って同じ構築を行う。

cwd は、ログに保存された実際の cwd を照合して明示設定する。存在するディレクトリであり、保存時の work-root と同じ worktree、かつ呼び出し元と同じ repository に属することを確認する。現在の cmoc process の cwd で代用しない。path context の導出は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「agent call の path context」に従う。

現在有効な `$CODEX_HOME` が実際に指す場所を、保存された使用場所と照合し、異なる場合は拒否する。過去の環境値を黙って復元したり、別の保存場所から会話を探索したりしない。環境値の決定と事前検証は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「環境変数 `$CODEX_HOME`」「preflight validation」に従う。

model provider・Model・Reasoning Effort は、再開時点の元 TUI 種別の `agent_call_kind` に対応する設定を使用する。設定取得の正本は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「agent call ごとの直接設定」とする。過去のモデル設定の固定や、`resume` 専用の agent call 種別・設定 entry は設けない。sandbox と承認設定も、対話 resume に適用する共通規則に従って明示設定する。

## 実行手順

1. 新しい最外側の invocation を開始し、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」に従って新しい実行 ID とログを用意する。指定された再開元実行 ID との対応を記録する。
2. `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「Doctor Preprocess」に従う doctor preprocess と、本書の種別解決・対象検査・環境照合を行う。doctor の処理対象には、照合した保存 cwd から導出する work-root を含める。
3. 同じ `$CODEX_HOME` の同じ Codex session が cmoc 管理下で同時起動しないよう使用を確保する。異なる exec ID からの再開も競合として扱い、検査と起動の間の競合を防ぐ。既存 process の終了が不明な場合に、使用中の状態を推測で解除しない。排他手法は固定しない。
4. 解決した TUI 種別の builder に、確定した Codex session ID と保存された cwd を渡す。新しい agent call と Codex call を開始し、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「TUI の新規起動と対話 resume」に従って process 用の設定と接続を準備する。
5. 入力エディタを開かず、指定した会話の対話 resume を起動する。追加指示は、再開した TUI でユーザーから受け取る。
6. 新しい process の会話対応と終了を記録し、その process 用の MCP 接続・capability・callback と会話の使用を終了処理で解放する。起動失敗の場合も、確保済みの資源を回収する。会話の使用は process の停止を確認するまで解放しない。

## 失敗条件と表示

対象検査・環境照合の不合格、同じ会話の使用中、会話の削除・利用不能、および対話 resume の起動失敗は、理由の分かる失敗にする。起動後に会話の利用不能が判明した場合も、新規会話や「最新の会話」へ自動で切り替えてはならない。対象実行 ID、失敗した条件、関係する記録や path を診断可能にする。

ログと console の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI と自動補完の境界」、通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「TUI の通知境界」に従う。非 TUI の対象を拒否した場合も、今回の `cmoc resume` には TUI の起動前エラーの境界を適用する。エラー分類は、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラー分類」に従う。

## 検証の分担

Fake Codex CLI による通常検証では、外部から得る会話情報を制御したうえで、次の cmoc の決定論的制御を確認する。

- 両 TUI 種別と再開済み exec の種別解決、非 TUI・ログ不足・破損・未終了・主会話不明の対象検査。
- 会話切替を含む記録の更新、異常終了の適格性、起動失敗と起動確認済みの区別、新旧の実行・call とログの対応、および再度の resume。
- cwd・`$CODEX_HOME`・file access mode の照合、同じ会話の競合、初期 prompt の非送信、元の agent call 種別による設定取得。
- 新しい process への MCP context の帰属と終了処理、および TUI のログ・通知境界。

Fake による成功は、Codex CLI が必要な外部契約を満たす証明にはしない。実装前に確認する外部契約は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の「実装前に検証する TUI の外部契約」に集約する。検証手段の選択と Real Codex CLI を使うテストの実行条件は、`{{cmoc-root}}/oracle/doc/dev_rule/test_execution.md` の「通常検証と追加検証を選択する」に従う。

## 対象外

- cmoc の workflow session や編集 run の処理途中の再開、Git 作業状態の巻き戻し。
- Codex 以外の TUI の再開、任意の外部会話 ID を直接指定する入口。
- cmoc 独自の会話本文の保存。会話本文の保管と復元は Codex 側に委ねる。

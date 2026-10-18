# `cmoc resume <exec-id>`

## 目的と公開入口

終了済みの cmoc 実行を実行 ID で指定し、その実行で固定した Codex session ID の会話を、元の TUI workload の制約で続ける。公開再開入口は `cmoc resume <exec-id>` だけとする。`cmoc tui` と `cmoc oracle investigation` に個別の再開オプションを設けない。

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

再開する会話は、`{{cmoc-root}}/oracle/doc/app_spec/codex_tui_rule.md` の「TUI の固定 session ID」に従って選ぶ。対象は、次のすべてを確認できる実行とし、満たさない場合は拒否する。

- 初回 exec の正常な process 終了と call の最終成功。
- 必要なログに欠落・破損・解釈不能・対応の不整合がなく、固定した Codex session ID を一意に特定できること。
- 最外側の cmoc 実行と、関連する起動済みの全 Codex process の終了。process の未起動と、起動後の終了確認不能を区別する。
- 本書の「workload と起動環境の保持」に従う workload と環境の一致。

この条件を満たせば、TUI の正常終了に加え、初回成功後の TUI 準備・起動失敗や、生成後の異常終了も再開対象とする。TUI が実際に会話を開いたか、入力可能になったかは適格性の条件にしない。初回 exec 自体の失敗・取消は対象外とし、UUID の取得だけでは初回成功を確認したことにならない。

- `cmoc resume` の実行 ID も同じ条件で次の再開元にできる。初回成功は、その実行が引き継いだ根拠で判断する。その実行自身のログから種別と適格性を判断できるものとし、過去の再開元ログを連鎖的にたどることを要求しない。必要な記録の保存は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI 再開のための実行記録」に従う。
- 同じ実行 ID を後日再指定した場合は、そこに記録された会話のその時点の続きへ戻る。指定した cmoc 実行の終了時点へ会話や作業状態を巻き戻す意味ではない。
- 機能導入前の実行も、必要な記録が存在する場合だけ対象とする。不足情報を推測する互換処理は要求しない。

## workload と起動環境の保持

汎用 TUI の制約は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/tui.md` の「全バックエンド共通」を正本とする。oracle 調査 TUI の制約は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_investigation.md` の「TUI 起動パラメータ」「調査結果と変更の扱い」を正本とする。再開によって、これらの作業範囲やファイルアクセスの権限を拡張しない。

保存された agent call 種別と file access mode を維持し、解決した workload の builder の選択値と一致することを起動前に確認する。一致しない場合は値を上書きして合わせず、制約を保持できないものとして拒否する。再開用パラメータの正確な構造は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「呼び出し単位と ID」で委譲した oracle src に従う。workload ごとの正確な構築は、次の builder へ委譲する。

- 汎用 TUI: `{{cmoc-root}}/oracle/src/oracle/acp_builder/tui/launch_tui.py` の `build_tui_request`。元の agent call 種別と制約を持つ、初期 prompt なしの再開パラメータを構築する。
- oracle 調査 TUI: `{{cmoc-root}}/oracle/src/oracle/acp_builder/oracle/investigation/launch_tui.py` の `build_oracle_investigation_request`。調査 workload の agent call 種別と制約を保って同じ構築を行う。

cwd は、ログに保存された実際の cwd を照合して明示設定する。存在するディレクトリであり、保存時の work-root と同じ worktree、かつ呼び出し元と同じ repository に属することを確認する。現在の cmoc process の cwd で代用しない。path context の導出は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「agent call の path context」に従う。

現在有効な `$CODEX_HOME` が実際に指す場所を、保存された使用場所と照合し、異なる場合は拒否する。過去の環境値を黙って復元したり、別の保存場所から会話を探索したりしない。環境値の決定と事前検証は、`{{cmoc-root}}/oracle/doc/app_spec/codex_common_rule.md` の「環境変数 `$CODEX_HOME`」「preflight validation」に従う。

model provider・Model・Reasoning Effort・provider-local 設定の取得は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「TUI 起動での設定の確定」に従う。内部の自動移行と後日の公開 resume の取得時点を混同しない。sandbox と承認設定も、対話 resume に適用する共通規則に従って明示設定する。

## 実行手順

1. 新しい最外側の invocation を開始し、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」に従って新しい実行 ID とログを用意する。指定された再開元実行 ID との対応を記録する。
2. `{{cmoc-root}}/oracle/doc/app_spec/doctor_preprocess.md` の「Doctor Preprocess」に従う doctor preprocess と、本書の種別解決・対象検査・環境照合を行う。doctor の処理対象には、照合した保存 cwd から導出する work-root を含める。
3. `{{cmoc-root}}/oracle/doc/app_spec/codex_tui_rule.md` の「会話の使用と排他」に従って固定した session ID の使用を確保する。異なる実行 ID からの再開も競合として扱う。
4. 解決した TUI 種別の builder に、確定した Codex session ID と保存された cwd を渡す。新しい agent call と Codex call を開始し、`{{cmoc-root}}/oracle/doc/app_spec/codex_tui_rule.md` の「process ごとの資源準備」に従って process 用の設定と接続を準備する。起動前の記録は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI 再開のための実行記録」に従う。
5. 入力エディタを開かず、指定した会話の対話 resume を起動する。追加指示は、再開した TUI でユーザーから受け取る。
6. 新しい process の終了を待ち、その結果を記録する。その process 用の MCP 接続・capability・通知 context を終了処理で回収する。起動失敗の場合も、確保済みの資源を回収する。会話の使用の解放は、`{{cmoc-root}}/oracle/doc/app_spec/codex_tui_rule.md` の「会話の使用と排他」に従う。

## 失敗条件と表示

対象検査・環境照合の不合格、同じ固定 session ID の使用中、対話 resume の生成失敗、および生成後の異常終了は、理由の分かる失敗にする。指定した会話の削除・利用不能で再開できない場合も、新規会話や「最新の会話」へ自動で切り替えてはならない。対象実行 ID、失敗した条件、関係する記録や path を診断可能にする。

ログと console の扱いは、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI と自動補完の境界」、通知は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「TUI の通知境界」に従う。非 TUI の対象を拒否した場合も、今回の `cmoc resume` には TUI の起動前エラーの境界を適用する。エラー分類は、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラー分類」に従う。

## 検証の分担

Fake Codex CLI による通常検証は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「TUI の二段階起動と公開 resume」に従う。新規起動から後日の公開再開までの制御を同じ検証範囲として扱う。

Fake による成功は、Codex CLI が必要な外部契約を満たす証明にはしない。実装前に確認する外部契約は、`{{cmoc-root}}/oracle/doc/app_spec/codex_tui_rule.md` の「実装前に検証する TUI の外部契約」に集約する。検証手段の選択と Real Codex CLI を使うテストの実行条件は、`{{cmoc-root}}/oracle/doc/dev_rule/test_execution.md` の「通常検証と追加検証を選択する」に従う。

## 対象外

- cmoc の workflow session や編集 run の処理途中の再開、Git 作業状態の巻き戻し。
- Codex 以外の TUI の再開、任意の外部会話 ID を直接指定する入口。
- cmoc 独自の会話本文の保存。会話本文の保管と復元は Codex 側に委ねる。

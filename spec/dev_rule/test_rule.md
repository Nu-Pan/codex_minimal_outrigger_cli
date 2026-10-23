# cmoc テスト実装規約

## 責務境界

本書は、realization test が満たすべき意味上の要件を定める。検査の実行手順と環境構築は、次の正本に従う。

- 構築済み環境での test と品質検査の選択・実行・完了判定・報告は、`{{cmoc-root}}/spec/dev_rule/test_execution.md` の「cmoc の test・品質検査実行手順」を正本とする
- 開発環境の新規構築、依存関係の追加、および pip 操作は、`{{cmoc-root}}/spec/dev_rule/development_environment.md` の「cmoc 開発環境」を正本とする

## goal

- cmoc の決定論的な制御ロジックが仕様どおりに動作することを検証する。例えば、git 状態の検査、作業ディレクトリの決定、対象ファイルの列挙、設定生成、ログ保存、状態更新、エラー処理などを対象とする。
- Codex CLI 呼び出しを伴う経路では、cmoc が責任を持つ結合動作を検証する。例えば、prompt 渡し、argv による設定、出力保存、schema 指定、response 後の処理などを対象とする。決定論的な検証の範囲は本書の「Fake Codex CLI」、実 CLI との結合を検証する成立条件は本書の「実経路統合テスト」で定める。

## non-goal

- LLM の回答品質や、Codex CLI に依頼した仕事の意味的な成功は cmoc の自動テストの目的としない
- Codex CLI 自体または model provider の正しさや安定性を保証することは目的としない
- Fake Codex CLI の成功によって Real Codex CLI との互換性を保証することは目的としない。実 CLI の引数・設定解釈、実際の応答形式、MCP 接続、TUI・通知 hook、認証・sandbox などとの結合は、Fake Codex CLI では検証できない。

## 基本

- pytest を使用する
- realization test は `{{cmoc-root}}/test` に実装する
- pytest の `tmp_path` を `{{test-root}}` とし、被テスト cmoc の HOME、repository、worktree、設定、および実行成果物をそのツリー内に構築する
- `{{cmoc-root}}/spec/app_spec/download_asset_cache.md` の「保存先と共有範囲」が定める固定キャッシュパスも、テスト時は `{{test-root}}` 内へ置き換え、実ユーザーのキャッシュを読み書きしない。共有を検証する複数の cmoc 配置・process は、同じテスト内の置換先を使用する

## テストの削除・統合

検出能力を維持する判断基準は、`{{cmoc-root}}/spec/app_spec/oracle_and_realization.md` の「realization refactor の改善判断」に従う。cmoc で維持すべき検証範囲は、本書の goal と個別仕様の検証要件から特定する。境界条件、失敗時挙動、外部から観測可能な結果に加え、実経路統合テストについては本書の「検証要件」が定める公開末端サブコマンドとの対応を維持する。

通常検証で実経路統合テストを実行しないことは、そのケースを不要とする根拠にはならない。実行の選択は `{{cmoc-root}}/spec/dev_rule/test_execution.md` の「通常検証と追加検証を選択する」に従い、Fake Codex CLI と Real Codex CLI の役割の違いを維持する。

## 実経路統合テスト

実経路統合テストは、利用者向け CLI entrypoint を独立 process で実行する realization test である。本番と同じ code path、実在の外部 executable、および必要な実推論を使い、response 後の処理と外部から観測可能な結果まで検証する。

### 用語と選択

- 正本用語は「実経路統合テスト」とする
- 個々の test case は「実経路統合テストケース」と表記する
- `e2e` を実経路統合テストの同義語、正本用語、または pytest marker として導入してはならない
- 実経路統合テストを分離選択する pytest marker が必要な場合は、`real_path_integration` だけを使用する

### 検証要件

実行時点で公開されている全末端サブコマンドを対象とし、各実経路統合テストケースで終了 code とコマンド固有の外部から観測可能な結果を検証する。

公開末端サブコマンドと実経路統合テストケースの対応は、機械的に比較可能にする。サブコマンドの追加または rename に対して、対応する実経路統合テストケースがなければ test を失敗させる。新規の公開末端サブコマンドには、同じ変更で対応する実経路統合テストケースを追加する。

Codex CLI 呼び出しには、実在の Codex CLI executable（Real Codex CLI）と実推論を使用する。Fake、mock、stub、記録済み response、または起動確認だけでは代替できない。

本番との差は、次のために必要な範囲だけ許容する。

- `{{test-root}}` による隔離
- 決定論的な入力
- 対話操作の自動化
- 本書が定めるテスト用 `CmocConfig` の直接設定
- `{{cmoc-root}}/spec/dev_rule/test_execution.md` の「Real Codex CLI を使う追加検証を起動する」が定めるテスト runner の command の起動場所

`--help`、shell completion、不正入力、事前条件違反、handler の直接呼び出し、または process を分離しない確認は、実経路統合テストとはみなさない。

### Model provider、Model、Reasoning Effort、および quota

- テスト用 `CmocConfig` でも、`{{cmoc-root}}/spec/app_spec/codex_model_provider.md` の「agent call ごとの直接設定」「回復確認 probe の設定例外」に従って model provider、Model、および Reasoning Effort の直接文字列を取得する
- テスト用 `CmocConfig` は、同仕様の委譲先が定める共有設定、個別設定、および provider 定義を備えた構造とする
- テスト用 `CmocConfig` の直接設定は、必要な実推論を維持しながら実経路統合テストの quota 消費を抑えるために、通常の既定設定と異なる値を使用してよい
- 実経路統合テスト専用の cmoc 固有なモデル分類または推論強度分類を導入してはならない
- 自動テストによる quota 消費を一律には禁止せず、テスト用 `CmocConfig` で選択される model provider の quota 消費を許容する
- 実経路統合テストの仕様または pytest command へ、具体的な model provider または Model 名を固定してはならない
- model provider に対する cmoc の責務境界は、`{{cmoc-root}}/spec/app_spec/codex_model_provider.md` の「cmoc の責務境界」を正本とし、実経路統合テストのために広げてはならない
- 通常の Codex CLI の共通契約は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「Codex CLI 共通呼び出し規約」、非対話 call の quota 枯渇時の待機と再開は、`{{cmoc-root}}/spec/app_spec/codex_exec_rule.md` の「`codex exec` が失敗した場合」を正本とする

## Fake Codex CLI

Fake Codex CLI は、Real Codex CLI の代わりに決定論的な応答を返し、cmoc の制御ロジックと Codex CLI 呼び出しの前後処理を検証するために使用する。

### agent call の設定選択と固定

設定の生成・検証は単体テスト、起動設定への反映は Fake Codex CLI を中心に、次を確認する。意味仕様は、`{{cmoc-root}}/spec/app_spec/codex_model_provider.md` の「agent call ごとの直接設定」「回復確認 probe の設定例外」と、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「呼び出し単位と ID」「Model provider、Model、Reasoning Effort」を正本とする。設定の正確なキーと既定値は、`{{cmoc-root}}/referenece/src/oracle/other/cmoc_config.py` の `CmocConfigCodex.agent_calls` を参照する。

| 検証対象 | 確認する結果 |
|---|---|
| 共有する呼び出し種別と設定の反映 | 共有対象の4 builder が、設定定義の共有専用キーと一致する `agent_call_kind` を返し、その値をキーとする `agent_calls` の各項目の変更が、すべての対象経路の起動 argv に反映される。run join は自動 join と明示 join の両方を確認する。ログ・feedback の分類も共有する種別を使い、各実行の agent call ID は区別する |
| 設定の配置と個別上書きの拒否 | 生成する設定では共有設定と個別設定を `agent_calls` に置き、共有対象の builder ごとの entry を含めない。保存設定に共有対象の builder 関数名の entry または個別上書きを加えると、通常の構造検証で拒否する |
| 共有設定欠落時の拒否 | 共有する `agent_call_kind` の entry が欠けた場合、共有対象の builder 関数名の entry を代わりに置いた場合も含め、起動前に拒否し、別キーへ fallback しない |
| 対象外の個別選択 | 共有対象外7種では、それぞれの builder 関数の `__name__`、返された `agent_call_kind`、および設定定義の個別キーが一致する。7種に異なる設定値を用意し、対応する `agent_calls` の entry を選ぶ。primary report 確認を本命 call の設定で代用しない |
| その他の設定不備の拒否 | 必須の個別設定・provider 定義の欠落、構造・型・値の制約違反、および provider 参照不整合では、暗黙の補完・変換をせず起動前に拒否する |
| 同一 call 内の固定 | 設定元を変更しても、初回・Structured Output 補正・retry・回復待ち後の再開では、確定済みの直接文字列と provider-local 設定を保持する |
| probe の例外 | 一時障害の回復確認では、共有設定を使う本命 call を含め、停止した call の確定値と同じ認証適用先を使う。quota から一時障害の確認へ切り替わった後の条件保持と、一時障害の確認を含まない quota 待機での probe 個別設定の選択を区別する |

TUI の設定確定時点は、次節の「TUI の二段階起動と公開 resume」で検証する。この設定統合のために Real Codex CLI を使うテストを追加・実行するのは、人間の明示指示がある場合に限る。実行の選択と手順は、`{{cmoc-root}}/spec/dev_rule/test_execution.md` の「通常検証と追加検証を選択する」に従う。

### TUI の二段階起動と公開 resume

汎用 TUI と oracle 調査 TUI の新規起動、および後日の `cmoc resume` では、Fake から得る初回 exec の session ID・終端情報、process の生成・終了、および通知 callback を制御し、次を確認する。TUI 内部の会話状態や入力待ち状態を cmoc へ通知する仕組みは Fake に要求しない。

| 検証対象 | 確認する cmoc の制御 |
|---|---|
| 確定入力と完全 prompt | 確定済み入力から builder が構築した完全本文を初回 call の prompt ファイルに保存し、同じ本文を stdin へ渡す。`_orig.md` の再読・代用や argv への本文混入がなく、保存失敗では起動しない。入力確定後の手動送信を要しない |
| 初回の完了と移行 | UUID の取得だけ、成功情報だけで process が未終了、終了コードだけ、終端情報の矛盾では移行しない。CLI の正常終了・call の最終成功・記録保存を確認後に、同じ UUID へ一度だけ対話移行する |
| prompt 不在の再開 | 自動移行と公開 resume の両方で、prompt 本文・空文字列・skeleton・補助指示を送らず、prompt ファイルや prompt 用 stdin 入力を作らない。新規入力と検査済み再開入力の排他条件も確認する |
| 失敗と取消 | 初回失敗では quota・一時障害でも再送・retry・回復待ち・probe・自動 TUI 移行をしない。初回実行中の取消では自然完了を待たず子 process を停止し、成功との競合でも後続処理を始めない。取消を作業完了として表示・通知しない。初回成功後の TUI 起動失敗も自動 retry せず、各終了経路の記録と資源回収を保つ |
| 再開適格性 | 両 workload と再開済み実行の種別を解決する。初回成功・固定した session ID・必要なログと環境・関連 process の終了を確認できれば、TUI の正常終了、準備・起動失敗、異常終了を扱える。実際に会話を開いたかは条件にしない。非 TUI、初回失敗・取消、ログの欠落・破損・不整合、実行中・終了確認不能、ID 不明、環境不一致を拒否する |
| ID とログ | 最外側の実行、初回 exec、TUI の call を対応付ける。内部移行で実行 ID とサブコマンド名を保ち、公開 resume では新しい実行・call・ログへ記録する。固定した ID とその取得元、初回成功の根拠、今回の環境と process の生成・終了・終了コードを保持し、再開後のログだけで再度の適格性を判断できる。指定した ID を実会話の観測結果として記録しない。同じ実行 ID の再指定で、固定した会話の現在の続きへ戻る |
| 設定と MCP | 二段階の間に設定元を変えても初回開始時の確定値を共用し、公開 resume は再開時点の設定を使う。cwd・`$CODEX_HOME`・file access mode の照合と process ごとの argv override を保つ。feedback・handoff・文書検索の context と接続・capability は各 process に帰属し、終了済みのものを再使用しない。初回 handoff の送信元は実際の初回 call ID とする |
| 表示と終了待ち | 初回は短い進行表示だけを出し、TUI へ制御を渡した後は混入させない。起動管理側は TUI の内部状態を確認せず process の終了を待つ。正常終了時に非対話用 primary report やサブコマンド完了 toast を追加しない |
| 初回処理完了通知 | exec の turn callback は無効とし、初回成功と TUI process の生成成功がそろった時点で 1 回通知する。初回成功だけ、TUI 生成前の失敗、初回取消、公開 resume では発火しない。入力可能確認を要せず、生成後の異常終了は別の失敗として扱う |
| 応答完了通知 | Codex から直接呼ばれる通知専用処理で、固定した ID だけを対象にし、別 ID・subagent・同じ turn の重複を除く。通知の準備・設定・送信失敗や欠落で TUI の起動・利用・主処理の結果を変更せず、再実行しない |
| 排他 | 同じ `$CODEX_HOME`・同じ固定した session ID の競合を、初回からの移行中と公開 resume の検査から起動までを含めて防ぐ。process の終了確認前に使用を解放しない。セッション切り替えの追跡・禁止や切り替え先の排他を要求しない |

意味仕様は、`{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「TUI の新規起動と対話 resume」、`{{cmoc-root}}/spec/app_spec/sub_command/resume.md` の「対象の適格性と会話選択」、および各節から参照するログ・設定・MCP・中断・通知仕様を正本とする。

Fake の状態は cmoc の分岐を検証するための入力であり、実 CLI に同じ API・event・callback が存在する証拠ではない。実 CLI の未検証事項は、`{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「実装前に検証する TUI の外部契約」と、`{{cmoc-root}}/spec/app_spec/windows_toast_notification.md` の「実装前に検証する Codex CLI の外部契約」に従う。Real Codex CLI を使うテストの実行条件は、`{{cmoc-root}}/spec/dev_rule/test_execution.md` の「通常検証と追加検証を選択する」を変更しない。

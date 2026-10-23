# Codex CLI 共通呼び出し規約

## 適用範囲と正本の分担

cmoc からの Codex CLI 呼び出しは、原則として `codex exec` で行う。本書は、非対話の exec と対話型の TUI に共通する契約を、各節の対象条件に従って適用する。実行形式に固有の契約は次の文書を正本とする。

| 実行形式 | 正本と責務 |
|---|---|
| TUI | `{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「Codex TUI 呼び出し規約」。新規起動の二段階実行、対話 resume、および TUI process の管理。 |
| exec | `{{cmoc-root}}/spec/app_spec/codex_exec_rule.md` の「`codex exec` 呼び出し規約」。非対話の入出力、Structured Output、成功・失敗判定、および回復。 |

## 呼び出し単位と ID

論理的な実行単位と個々の CLI 呼び出しを次のように区別する。

| 用語 | 実行単位 | cmoc が付与する識別情報 |
|---|---|---|
| agent call | 1 個の `AgentCallParameter` を入力とする論理的な実行。初回実行、Structured Output の補正、retry、および回復待ち後の再開を合わせて 1 回と数える。回復確認 probe は別の agent call とする。 | 呼び出し種別を表す安定した低カーディナリティの `agent_call_kind` と、一意な agent call ID |
| Codex call | 初回実行、補正、retry、回復待ち後の再開、および probe を含む個々の Codex CLI 呼び出し。 | 各 CLI 呼び出し、および TUI process ごとに一意な Codex call ID |

`AgentCallParameter` を構築する builder の関数名は、用途を中心とした `build_<用途>_request` とする。個別設定を持つ call ではその関数の `__name__`、設定を共有する call では共有専用キーを `agent_call_kind` に指定する。

ログ・feedback の分類にも同じ `agent_call_kind` を使う。複数の builder が同じ種別を使う場合も、各実行は agent call ID で区別する。共有対象と設定取得の規則は、`{{cmoc-root}}/spec/app_spec/codex_model_provider.md` の「agent call ごとの直接設定」に従う。

agent call ID と Codex call ID の書式と採番は、`{{cmoc-root}}/spec/app_spec/id.md` の「ID のフォーマット」「プレフィックス」「採番と順序保証」に従う。cmoc は、論理 agent call の開始前に agent call ID を発行し、上表の同じ論理 call を通して保持する。Codex call ID は、個々の CLI 呼び出しまたは TUI process の開始前に発行する。

`{{execution-id}}` は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「実行 ID の開始表示」を正本とする。`{{codex-call-id}}` は上表の Codex call ID を表す。

個別 agent call の意味上の責務と判断基準は、対応する oracle doc を正本とする。AgentCallParameter builder は、その oracle doc から明示的に委譲された範囲で、正確な prompt 文面と workload 固有の起動パラメータを構築する。ただし、model provider、Model、および Reasoning Effort は構築対象から除く。

`AgentCallParameter` の field 名、型、既定値、および初期 prompt と対話再開の排他条件を含む正確な構造は、`{{cmoc-root}}/reference/src/oracle/acp_builder/basic.py` の `AgentCallParameter` と `TuiResumeTarget` へ委譲する。

## Codex session ID

Codex session ID は、Codex が返す外部の識別子をそのまま使用する。cmoc の session ID、agent call ID、および Codex call ID とは区別する。

## agent call の path context

agent call の path context は、その call に設定する cwd を起点に決める。

| 識別子 | 意味 |
|---|---|
| `agent_call_cwd` | 子 agent call に設定する cwd |
| `work_root` | `agent_call_cwd` を含む最寄りの Git worktree root |
| `repo_root` | `work_root` が属する Git repository の main worktree root |

`AgentCallParameter.agent_call_cwd` は必須の呼び出しパラメータとし、cmoc process の cwd から暗黙に補完してはならない。`work_root` と `repo_root` は、linked worktree、submodule、および separate git directory を含め、Git が保持する repository metadata から導出する。名前が `.git` であるだけの通常の file または directory を、Git repository metadata として扱ってはならない。

path context に関する正確な定義は、次の oracle src へ委譲する。

- call-scoped path context、root placeholder、および Git command を含む導出処理：`{{cmoc-root}}/reference/src/oracle/other/path_model.py` の `RootPathPlaceHolder`、`AgentCallPathContext`、`resolve_work_root`、および `resolve_repo_root`
- prompt part との受け渡し：`{{cmoc-root}}/reference/src/oracle/prompt_builder/basic.py` の `PlaceholderMap`
- 完全 prompt への統合：`{{cmoc-root}}/reference/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt`

### `{{work-root}}` に対する仮定

cmoc による操作対象 worktree である `{{work-root}}` は、次の要件を満たすものと仮定する。

- git で管理されている
- `{{work-root}}/oracle` 配下に断片的な正本情報が記載されている（`{{cmoc-root}}` 配下がそうであるように）
- `{{work-root}}` 固有の作業のノウハウと、言語、framework、tool 固有の手順は、Codex CLI が参照可能な追跡対象の文書、設定、script、または skill として対象リポジトリが用意する。配置先は `.agents/skills` に限定しない

### cmoc process の cwd との関係

- cmoc process は、対象 Git repository のいずれかの worktree root をカレントディレクトリとして実行する
- cmoc process の cwd と `AgentCallParameter.agent_call_cwd` は、異なる値を許容する
- cmoc process の cwd が `{{repo-root}}` であっても、run 用 `AgentCallParameter.agent_call_cwd` は `{{run-root}}` とする

call-scoped path context の適用範囲を次に示す。

- 同じ agent call の cwd、file access、routing、file 分類、および path placeholder は、同一の call-scoped path context と整合させる
- cmoc process の cwd だけを根拠として、子 agent call の path context を決定してはならない
- call-scoped path context の構築に process-global な `chdir` を使用してはならない
- 並列 agent call は call-scoped path context を共有または変更してはならない

### non-goal

- `{{repo-root}}`、`{{run-root}}`、および `{{cmoc-run-worktree}}` の既存の意味や配置は変更しない
- 全 agent call で `{{work-root}} != {{repo-root}}` とすることは目的としない
- agent call のためだけに新しい root placeholder を追加しない

## 環境変数 `$CODEX_HOME`

cmoc 呼び出し時点で `$CODEX_HOME` が設定済みなら、その値をそのまま Codex CLI に渡す。未設定なら、`CODEX_HOME=${HOME}/.codex` 相当の絶対パスを設定して渡す。

## preflight validation

cmoc は Codex CLI 呼び出し前に、Codex CLI が実際に参照する `$CODEX_HOME` がディレクトリとして存在することを検証する。この preflight validation に失敗した場合は、cmoc の実行を即時失敗させる。model provider 固有の認証要件を cmoc が一律に検証してはならない。

ただし、primary report の重要事項確認用 call の開始不能には、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「確認の停止・失敗と保存」「確認結果と終了結果の分離」を適用する。上記の即時失敗を最外側の終了結果へ適用する際は、この例外に従う。

## Codex CLI 引数による設定上書き

cmoc は、`AgentCallParameter`、`CmocConfig` などから決まる呼び出し単位の設定を、Codex CLI の argv で明示的に上書きする。cmoc が上書きする設定については、`$CODEX_HOME/config.toml` や project config の値に依存してはならない。

- すべての Codex CLI 呼び出しで、専用引数 `--no-daemon` を必ず指定する
- cmoc は Codex CLI 呼び出しに `--profile` (`-p`) を指定してはならない
- cmoc は Codex CLI 呼び出しのために `$CODEX_HOME/{{name}}.config.toml` を生成してはならない
- 上書き対象に専用引数が存在する場合は専用引数を使う
- 専用引数が存在しない設定は、`--config` (`-c`) と `key=value` 形式の設定値を使って上書きする
    - `--config` は設定項目ごとに繰り返してよい
    - `key=value` は 1 個の argv 要素として渡す
    - `value` は Codex CLI が解釈する TOML 値とする
- すべての Codex CLI 呼び出しで、次の承認設定を呼び出し単位の argv により明示的に上書きする
    - `approval_policy`: `"on-request"`
    - `approvals_reviewer`: `"auto_review"`
- Codex CLI 呼び出しにおける Windows toast 通知の effective configuration、`codex exec` と TUI の境界、および callback の検証条件は、`{{cmoc-root}}/spec/app_spec/windows_toast_notification.md` の「Windows toast 通知」を正本とする

## ファイルアクセス制限

### Codex CLI sandbox

すべての Codex CLI 呼び出しで、専用引数 `--sandbox` を明示する。`AgentCallParameter` を使う呼び出しでは、すべての有効な file access mode に `workspace-write` を使う。

| file access mode | sandbox |
|---|---|
| `READONLY`, `PURE_ORACLE_READ`, `REPO_WRITE`, `PURE_ORACLE_WRITE`, `REALIZATION_WRITE`, `NO_POLICY` | `--sandbox workspace-write` |

表にない file access mode を受け取った場合は、sandbox を推測せず Codex CLI 呼び出し前に失敗させる。`AgentCallParameter` を使用しない動作確認用の呼び出しでは `--sandbox read-only` を使う。

`AgentCallParameter.file_access_mode` は、プロンプトで指示する詳細なファイルアクセス制限を選ぶ論理 mode とする。`READONLY` と `PURE_ORACLE_READ` でも一時作業領域への書き込みを許容し、リポジトリ全体への書き込みを OS sandbox で禁止することは目的としない。

sandbox mode の選択は専用引数だけで行い、`--config` で `sandbox_mode` を上書きしてはならない。`workspace-write` を使う呼び出しでは、`/tmp` を書き込み対象に含める補助設定として、`sandbox_workspace_write.exclude_slash_tmp=false` を呼び出し単位で明示的に上書きする。この補助設定には、本書の「Codex CLI 引数による設定上書き」に従って `--config` を使う。

### command 単位の sandbox 外実行

- `--sandbox` は agent call 内で実行する command の既定境界を定めるものとし、承認済みの command 単位 sandbox escalation まで禁止するものではない
- command 単位 sandbox escalation は、作業固有の oracle file が sandbox 外実行を必要条件として明示し、agent が対象 command と理由を限定して要求する場合に限り許容する
- escalation は対象 command とその descendant process だけへ適用し、agent call 全体の sandbox mode、`AgentCallParameter.file_access_mode`、または詳細なファイルアクセス制限を変更しない
- command 単位 escalation のために `--sandbox danger-full-access` または `--dangerously-bypass-approvals-and-sandbox` を agent call 全体へ指定してはならない
- cmoc は command 単位 escalation のための Codex exec rule を生成せず、永続的な prefix allow rule に依存しない

### model provider transport と Codex sandbox のネットワークアクセス

- Codex CLI と model provider の間の transport は、Codex agent が sandbox 内で実行する command のネットワークアクセスとは別のものとして扱う
- model provider の選択または provider-local 設定を理由に、Codex sandbox のネットワークアクセス設定を追加または変更してはならない
- agent が実行する command にネットワークアクセスが必要な場合は、model provider 設定とは独立して扱う

### 詳細なファイルアクセス制限

詳細なファイルアクセス制限は、agent が直接行うファイルアクセスに適用する deny-list とする。共通制限または各 mode の追加制限で禁止されていない読み書きは許可する。個別 agent call の file access mode は、対応する oracle doc の作業範囲と一致させ、AgentCallParameter builder が正確な選択値を構築する。

#### 共通制限と mode 別の追加制限

agent による `.agents` ツリー内の編集は、file access mode にかかわらず禁止する。

`NO_POLICY` 以外の全 file access mode には、次の共通制限を適用する。

- `{{work-root}}` ツリー外への書き込みを禁止する。
- `{{work-root}}/.git`、`{{work-root}}/.codex`、および `{{work-root}}/.cmoc` ツリー内の書き込みを禁止する。
- Git metadata は配置先によらず変更を禁止する。
- `AGENTS.md` の書き込みを禁止する。
- `{{work-root}}/memo` の読み書きを禁止する。

`NO_POLICY` 以外の各 mode は、共通制限に次の制限を追加する。

| file access mode | 追加制限 |
|---|---|
| `READONLY` | oracle file と realization file の書き込みを禁止する。 |
| `PURE_ORACLE_READ` | oracle file の書き込みと realization file の読み書きを禁止する。 |
| `REPO_WRITE` | 追加の制限を設けない。 |
| `PURE_ORACLE_WRITE` | realization file の読み書きを禁止する。 |
| `REALIZATION_WRITE` | oracle file の書き込みを禁止する。 |

`NO_POLICY` は、共通 file access policy が存在しない有効な特殊 mode とする。必要な instruction は個別の `AgentCallParameter` builder がすべて構築する。

#### 一時作業領域

`NO_POLICY` 以外の agent call では、共通 file access policy の例外として `/tmp` と `%TMPDIR` のツリー内の読み書きを許可し、一時作業領域として使ってよい。例外の優先関係は、本書の「SDPolicy の例外」に従う。

一時作業領域を、禁止・制限事項の迂回に使ってはならない。

#### 読み取りの範囲

`{{work-root}}` ツリー外であることだけを理由に読み取りを禁止しない。外部ログ、設定、ライブラリ、Git metadata も読み取りを許可する。ただし、この許可は、明示的な読み取り禁止、mode 別のアクセス制限、および workload 固有の閲覧・判断材料の制限を解除しない。MCP や Git の履歴・差分を経由しても、明示的な読み取り禁止を迂回してはならない。

一度読んだ情報の影響を排除できないため、realization file の読み取り禁止は、判断の根拠への採用だけでなく閲覧自体に適用する。また、外部読み取りの許可によって、対象 worktree の正本、追従対象 revision、作業範囲、または編集対象を変更してはならない。

#### prompt の構築と sandbox との関係

`build_file_access_policy` の結果は、共通 file access policy の有無を表す。Python 上の正確な不在値と戻り値型、および各 mode の正確な prompt 文面は、`{{cmoc-root}}/reference/src/oracle/prompt_builder/policy/file_access.py` の `build_file_access_policy` へ委譲する。一時作業領域の読み書きの例外は、対象の禁止と同じ file access policy 内で表現する。

`build_complete_prompt` はこの結果に基づいて共通 file access policy の追加可否を決める。完全 prompt への正確な追加条件は、`{{cmoc-root}}/reference/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する。

path ごとの読み書き可否などの詳細な制限を sandbox に反映しようとしてはならない。詳細なファイルアクセス制限がプロンプトだけで指示され、sandbox では強制されないことを許容する。

### 書き込み主体の責任分界

agent の直接ファイルアクセス制限は、次の書き込みには適用しない。

- MCP 経由の外部ツールによるファイル書き込み。書き込み先や file access mode を問わない
- Structured Output の受け取り側による保存・更新と、cmoc 自身のログ保存、report 保存、索引同期などの管理処理。各機能が定める出力契約と受理条件に従う。Structured Output 自体がファイルを書き込むわけではない

MCP の責任分界は次のとおりとする。

- cmoc が提供する MCP の書き込みは、各 tool の仕様と検証で管理する。ユーザー設定・プロジェクト設定で追加された MCP の書き込み先を cmoc は制限・保証せず、その制御のための検査や仕組みを追加しない
- MCP の例外はファイルアクセス上の書き込み制限だけに適用し、他の policy、各機能の利用条件、または workload の作業範囲を解除しない

`{{work-root}}/.cmoc` は cmoc の管理領域とする。agent から必要な更新を依頼する場合は、各機能が提供する MCP を使用する。cmoc 自身の管理処理を MCP 経由へ変更する必要はない。

cmoc の管理データは `.cmoc/gt` または `.cmoc/gu` 配下に配置する。所有 root、保存先、Git 追跡・非追跡の責務、および保存記録と作業ファイルの用途・信頼性・lifecycle は、各機能の仕様に従う。アクセス区分を表す `ar`・`aw` の中間階層、それを含む旧配置への互換機構、および旧配置からの自動移行は設けない。

この責任分界を理由に、sandbox、permission profile、network access、または承認設定を拡張してはならない。必要性が確定していない MCP、汎用ファイル操作 MCP、または将来用の管理機構を追加しない。

### permission profile の不使用と動的生成禁止

- cmoc は、入力の種類や伝達経路を問わず、permission profile の生成（動的生成を含む）、更新、選択、Codex CLI への注入、および事前作成された permission profile への依存を行ってはならない
- oracle file が特定の path に対するアクセス制限を要求する場合も、その制限はプロンプトへ反映し、permission profile や path 単位の sandbox 設定へ変換してはならない
- agent-facing な分類文面で伝える Git ignore 判定は、`{{cmoc-root}}/spec/app_spec/cmoc_basic_instruction_file_enumeration.md` の「分類結果」が定める境界だけを表す
- `git check-ignore` の判定結果をファイル分類や対象ファイルの選別に使用してよいが、Codex CLI の sandbox または permission profile を組み立てる入力にしてはならない

## agent call の差分検証

仕様にない検証の追加によって、正常な作業が停止することを防ぐ。

- cmoc は agent call の差分に対し、oracle file が要求する条件の機械的検証だけを行う。
- ファイルアクセス制限や agent の作業範囲の指示だけを根拠に、差分の検証、受理拒否、またはリカバリ処理を追加してはならない。

本節は、agent 自身が守るファイルアクセス制限を緩和せず、通常の実装修正やテスト実行一般を新たに禁止しない。

## Model provider、Model、Reasoning Effort

- agent call ごとの直接設定、値の意味、検証境界、および provider に対する cmoc の責務境界は、`{{cmoc-root}}/spec/app_spec/codex_model_provider.md` の「Codex model provider」を正本とする
- cmoc は各 agent call に使用する設定を、同仕様の「agent call ごとの直接設定」が定める設定取得キーの選択規則と、「回復確認 probe の設定例外」に従って取得する
- `cmoc oracle edit` の設定の確定時点と両回での共用は、`{{cmoc-root}}/spec/app_spec/sub_command/oracle_edit.md` の「ユーザー指示と prompt の構築」に従う
- 取得した model provider、Model、Reasoning Effort、および provider-local 設定は、初回、Structured Output の補正、retry、および回復待ち後の再開を含む同一 agent call 内の全 Codex call で変更せず使用する
- Codex CLI に対する Model と Reasoning Effort は、すべての呼び出しで次の argv により明示的に上書きする
    - Model: `--model`, `{{model-name}}`
    - Reasoning Effort: `--config`, `model_reasoning_effort="{{reasoning-effort}}"`
- model provider ID は、次と同じ形の argv により呼び出し単位で明示的に上書きする
    ```text
    --config 'model_provider={{provider ID の TOML value}}'
    ```
- 選択した provider の provider-local 設定は、各 key/value を次と同じ形の argv により呼び出し単位で明示的に上書きする
    ```text
    --config 'model_providers.{{provider ID の TOML key segment}}.{{provider-local key の TOML key segment}}={{provider-local setting の TOML value}}'
    ```
- model provider ID、provider-local key、および provider-local setting は、意味を変えず Codex CLI が解釈できる TOML key/value として符号化する
- 選択していない provider の設定を argv に渡してはならない
- 実経路統合テストで使用する `CmocConfig` の要件は、`{{cmoc-root}}/spec/dev_rule/test_rule.md` の「実経路統合テスト」を正本とする
- cmoc は Model provider、Model、Reasoning Effort の設定情報を Codex CLI プロンプトに注入しない

## prompt の共通原則

prompt の一般規則は、`{{cmoc-root}}/spec/app_spec/cmoc_basic_instruction.md` の「oracle doc と oracle src の正本責務」から「正本責務に基づく優先関係」までを正本とする。本節は prompt 固有の規則だけを定義する。

### prompt literal の役割と制限

prompt literal は、受信 agent がその agent call を実行するために必要な情報を伝える agent-facing な表現とする。含めてよい内容は、次の範囲に限定する。

- call 固有の目的、作業範囲、および入力
- runtime の path および対象
- 受信 agent が実行時に知る必要がある制約
- oracle doc が所有する規則の必要最小限の agent-facing な表現

prompt literal に、次の内容を正本として置いてはならない。

- 受信 agent の判断に不要な cmoc の内部仕様、内部 algorithm、状態遷移、または設計理由
- oracle doc に存在しない新しい要求、禁止、判断基準、goal、non-goal、または意味上の優先関係
- 正本を prompt literal 側へ移すことを目的とする詳細説明
- oracle doc との競合時に prompt literal を優先させる規定

### caller 固有の objective

caller 固有の objective は、名目的な担当 role ではなく、その agent call 固有の目的を伝える。

- task は常に設け、その agent call で実行する行為と対象を示す。
- scope は、対象、根拠、起点、または作業範囲を task だけでは特定できない場合に設ける。scope は file access の許可または禁止を定義しない。
- completion criteria は、agent call 終了後に検証可能で、schema または policy だけでは表現されない call 固有の完了状態がある場合に設ける。
- non-goals は、隣接作業への逸脱が予想される場合に限り、call 固有の対象外を示す。一般的な禁止操作またはアクセス制限を置かない。

独立した role または role 用の構造は設けない。agent call の種別を機械的に識別する値は `AgentCallParameter.agent_call_kind` とする。評価方向または責務に意味がある場合は、task の行為と判断対象、named policy、または call 固有の static prompt で具体化する。

objective は、専用機構が所有する次の内容を重複させない。

- 権限と一般的なアクセス禁止は、`AgentCallParameter.file_access_mode` と file access policy が所有する。
- 再利用する判断基準と作業規定は、named policy が所有する。
- call 固有の判断基準と、schema 外の決定論的事後条件は、caller の static prompt が所有する。
- runtime input は、caller の dynamic prompt が所有する。
- Structured Output の構造と schema で表現できる出力要件は、`AgentCallParameter.structured_output_schema_path` が指す schema が所有する。

objective の外側の block、正確な引数、項目名、構築順序、任意項目の省略条件、および rendering は、`{{cmoc-root}}/reference/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する。

### call 固有の実行時指示の優先関係

`prompt > oracle file > installed skill` と表現される優先関係は、cmoc の恒常的な意味仕様ではなく、call 固有の目的、作業範囲、入力、および権限に適用する。この正確な agent-facing literal は、`{{cmoc-root}}/reference/src/oracle/prompt_builder/policy/oracle.py` の `build_oracle_policy` へ委譲する。

call 固有の実行時指示の優先関係は、prompt literal に cmoc の新しい意味仕様を作る権限を与えない。prompt literal と oracle doc が所有する意味仕様が食い違う場合は、prompt literal による仕様変更とは扱わず、oracle file 間の不整合として扱う。

### SDPolicy の例外

`SDPolicy.exception` は、同じ `SDPolicy` 内の「必須」「禁止」「許容」に優越する。他の policy、個別機能の利用条件、または workload 全体の制限を解除するものではない。

カテゴリの正確な構造と agent 向け表示は、`{{cmoc-root}}/reference/src/oracle/other/struct_doc.py` の `SDPolicy` と `_render_sd_policy_as_markdown` へ委譲する。

### Git 差分の参照入力

初期 prompt の文字数を差分本文の大きさや変更 path 数に比例させないため、cmoc が Git 差分を agent の判断材料として自動付加する場合は、取得に必要な参照情報だけを渡す。差分本文や変更 path 一覧は渡さない。agent が取得した差分も会話の入力となるため、総トークン数の削減は保証しない。

- 比較する repository、比較範囲、および対象条件は個別 workload が所有する。agent はその指定に従って必要な差分を Git から取得する
- 取得失敗を正常に取得できた空差分として扱ってはならない。取得できない場合は個別 workload の既存の失敗処理に従い、独立した状態や追加の agent call を設けない
- cmoc 自身が行う差分検査、変更 path の検証、空差分判定、および commit・rollback の責務は廃止・緩和しない
- ユーザー自身が入力する文章に差分を含めることは禁止しない
- Git command の具体的な組み合わせ、差分を読む回数・分割方法、および表示形式は固定しない。新しい汎用の差分入力 schema、永続 state、差分保存ファイル、root placeholder の追加は目的としない

### prompt の構築と受け渡し

初期入力を伴う呼び出しでは、`AgentCallParameter.prompt` に完全 prompt 本文を設定する。cmoc は、builder が生成して確定した値を変更せず、初回 Codex call に渡す。realization implementation は、prompt 本文に独自の指示、注意書き、説明、整形、要約、補完、翻訳、補助文脈、モデル・reasoning effort 情報、その他の意味変更を加えてはならない。

- 完全 prompt の共通構築順序は、`{{cmoc-root}}/reference/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する。同関数が、prompt part、目的、および placeholder 定義を統合する正確な順序を所有する
- prompt の共通 rendering は、`{{cmoc-root}}/reference/src/oracle/other/struct_doc.py` の `render_sd_node_as_markdown` へ委譲する。同関数が、構造化された prompt を Markdown 文字列へ変換する正確な rendering を所有する

prompt の確定前後に行う処理は、次のように区別する。

- editor input handoff の本文生成と送信元情報の注入は、`{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の「本文の生成」に従い、受信側の editor input 確定前に完結させる。
- Codex CLI の実行形式に必要な保存、stdin 入力、末尾改行などの機械的処理は、プロンプトの意味内容を変更しない範囲に限って許可する。

プロンプト本文を argv に載せてはならない。argv に載せてよいのは、フラグ、モデル名、設定上書き値、Codex session ID、短い固定文字列、短いファイルパスのみとする。

## feedback reporter と collector context

- reporting の意味は `{{cmoc-root}}/spec/app_spec/feedback_observation.md` の「agent による報告」を正本とする。正確な agent 向け文面と完全 prompt への配置は、同文書が参照する oracle src を正本とする
- `AgentCallParameter` は、reporter の提供を有効にするかを agent call 単位で保持する。正確な field 名、型、および既定値は、`{{cmoc-root}}/reference/src/oracle/acp_builder/basic.py` の `AgentCallParameter` へ委譲する
- builder が完全 prompt を構築する場合は、reporter の提供判断と同じ値を渡す。有効な call には報告規定を注入し、無効な call には注入しない。正確な選択引数と配置は、`{{cmoc-root}}/reference/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する
- 提供を無効にする call は、`{{cmoc-root}}/spec/app_spec/sub_command/feedback_report.md` の「issue 処理 call の observation 報告」と、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「重要事項確認用 call > agent の責務と境界」に従う。対象外の builder は、reporter と報告規定をともに有効にする既定の契約を維持する
- 初回、Structured Output の補正、retry、および回復待ち後の再開を含む同一 agent call の全 Codex call で、この提供判断を維持する
- 提供が有効な場合、cmoc は Codex call の開始前に、`{{cmoc-root}}/spec/app_spec/feedback_observation.md` の「collector と transport」が定める call context と capability を登録し、call-scoped な local stdio MCP reporter/client を利用可能にする。無効な場合は、その call 用の reporter/client を起動せず、reporter context と capability を登録しない
- cmoc は call-scoped な Codex CLI の argv override により提供判断を反映する。有効な場合の MCP server namespace `cmoc_feedback`、公開 tool `submit_observation`、同 tool の approval behavior、および MCP process に必要な起動情報の設定には、本書の「Codex CLI 引数による設定上書き」を適用する
- cmoc は、提供の有効・無効のどちらでも `cmoc_feedback` の effective configuration 全体を呼び出し単位で管理する。user config、`$CODEX_HOME/config.toml`、または project config にある次の情報には依存してはならない。また、これらの設定によって、別 tool の公開または reporter の置換を許してはならない
    - server 定義
    - tool 設定
    - approval behavior
    - 起動情報
- 無効な call では、同名の外部 server 設定を含めて `cmoc_feedback` を無効にし、その namespace の tool を提供しない。cmoc による有効化の省略だけで済ませてはならない。永続的な user/project 設定を書き換えず、呼び出し単位の実効設定でこの非提供を成立させる
- 通常の `cmoc_feedback.submit_observation` は、human approval、auto-review、または command sandbox escalation を要求せずに実行できるよう設定する
- reporter と collector の残りの lifecycle、および意図的な非提供と利用不能な障害の扱いは、`{{cmoc-root}}/spec/app_spec/feedback_observation.md` の「agent による報告」「collector と transport」「rule registry」を正本とする

## editor input handoff MCP

editor input handoff の提供対象、利用条件、および agent の責務は、`{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の「概要」「agent の責務と権限」を正本とする。

- `AgentCallParameter.enable_editor_input_handoff_mcp` は、`cmoc_editor_input` MCP server の有効化を呼び出し単位で指定する。field の正確な型と既定値は、`{{cmoc-root}}/reference/src/oracle/acp_builder/basic.py` の `AgentCallParameter` へ委譲する
- 提供対象外の builder は `enable_editor_input_handoff_mcp` の既定値を使用する
- 有効な各 call には `cmoc_editor_input` MCP server を提供する。handoff ガイド取得と上書きの公開 tool は、`{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の「MCP interface」に従う。MCP の提供によって、sandbox、network access、file access mode、または agent call の成功条件を変更してはならない
- handoff instruction は MCP の有効化とは別に `build_complete_prompt` の `editor_input_handoff_policy` で選択する。正確な定義と配置は、`{{cmoc-root}}/reference/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する
- handoff instruction の正確な agent 向け文面は、`{{cmoc-root}}/reference/src/oracle/prompt_builder/policy/editor_input_handoff.py` の `build_editor_input_handoff_policy` へ委譲する
- 有効な各 Codex process について、cmoc の起動・呼び出し管理経路が、実際の送信元情報を MCP の呼び出し元コンテキストへ供給する。情報の意味、process 間の分離、および正確な構造の委譲は、`{{cmoc-root}}/spec/app_spec/editor_input_handoff.md` の「送信元情報」と「正本の分担」に従う
- 各 process の起動前に、その process の Codex call ID の確保、MCP への送信元情報の供給、および `{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「handoff 送信元情報の記録」に従う記録と flush を完了する。ログの対応付けと MCP への供給には同じ実際の値を使い、別の call の ID を代用せず、当該 process の起動時に別の ID を再発行しない

## 文書検索 MCP

検索の対象、信頼境界、同期、結果、失敗、および資源管理は、`{{cmoc-root}}/spec/app_spec/document_search.md` の「cmoc 専用文書検索」を正本とする。本節は call と MCP 接続の責務を所有する。

- 検索 MCP の有効化を呼び出し単位で指定する。正確な field・型・既定値は、`{{cmoc-root}}/reference/src/oracle/acp_builder/basic.py` の `AgentCallParameter` へ委譲する。builder が完全 prompt を構築する場合は、その検索有効状態を起動パラメータと一致させる。
- oracle edit、oracle investigation、汎用 TUI、realization apply、refactor の所見調査・修正、feedback の normalization・remediation、および run/session join の競合解消では、関連原文への到達のため検索を提供する。短い応答だけで可用性を確認する回復 probe と、固定した report 本文だけを読む重要事項確認用 call では検索を無効にする。
- 各 call では検索要求時の自動同期を使う。起動時の検索設定・検索用コンポーネントの検査と索引同期は、`{{cmoc-root}}/spec/app_spec/doctor_preprocess.md` の「実行手順」「検索索引の同期」に従う。Structured Output の補正・retry・再開でも検索の有効状態と work-root を維持する。
- 有効な各 Codex process に local stdio MCP 接続を設ける。検索 server の cwd、実行ファイル、引数、許可 tool、approval behavior、起動・tool 期限、および信頼された context の供給を、呼び出し単位の argv override で管理する。設定の符号化には本書の「Codex CLI 引数による設定上書き」を使う。
- 起動管理側は、内側の検索要求の全体上限に停止・回収・返送の余裕を加えて、外側の MCP tool 期限を設定する。有効な設定変更時も、実行途中の動的延長に依存せずこの関係を保つ。内側の期限と停止は、`{{cmoc-root}}/spec/app_spec/document_search.md` の「排他、期限、終了」に従う。余裕の具体値は実装に委ね、同文書の「製品受入条件」で連携を検証する。
- 起動管理側は、検索の診断記録を呼出し元のサブコマンドログへ届け、実行 ID・Codex call・対象 work-root と対応付ける信頼された context を供給する。context は MCP 引数や agent の申告から決めない。記録と相関の要件は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「索引同期の診断記録」に従う。
- server namespace と公開 tool の正確な名前は、`{{cmoc-root}}/reference/src/oracle/other/document_search.py` の `SEARCH_MCP_SERVER` と `SEARCH_TOOL_NAME` を使う。この namespace の user/project 設定に依存せず、別 server・tool・work-root への差替えを許さない。無効な call では同名の外部設定を残して検索を提供してはならない。
- 通常の検索 tool は human approval、auto-review、command escalation を要求せず利用できるよう設定する。これは sandbox、permission profile、network access、file access mode の拡張を意味しない。
- `$CODEX_HOME/config.toml` を書き換えない。既存 feedback/handoff MCP の設定と接続を保持して共存させ、検索設定の注入で上書き・無効化しない。
- Codex process の終了時は起動管理側が接続を閉じ、検索側の子 process 回収まで確認する。TUI と `codex exec` のどちらにも同じ接続境界を適用する。

## Codex CLI 呼び出し情報の保存

- Codex CLI 呼び出しに関する情報は `{{repo-root}}/.cmoc/gu/log/codex/{{execution-id}}/{{codex-call-id}}_call.json` に保存すること
- 呼び出し記録から、親の実行 ID、agent call ID、および個々の Codex call ID の対応を追跡可能にする
- 後続の Codex call は、先行する Codex call の log または出力を上書きしてはならない

# `codex exec` 呼び出し規約

## 基本

cmoc からの Codex CLI 呼び出しは、原則として `codex exec` で行う。本書では、論理的な実行単位と個々の CLI 呼び出しを次のように区別する。

| 用語 | 実行単位 | cmoc が付与する識別情報 |
|---|---|---|
| agent call | 1 個の `AgentCallParameter` を入力とする論理的な実行。初回実行、Structured Output の補正、retry、および回復待ち後の再開を合わせて 1 回と数える。回復確認 probe は別の agent call とする。 | 対応する builder を表す安定した低カーディナリティの `agent_call_kind` と、一意な agent call ID |
| Codex call | 初回実行、補正、retry、回復待ち後の再開、および probe を含む個々の Codex CLI 呼び出し。 | 各 CLI 呼び出し、および TUI process ごとに一意な Codex call ID |

最外側の末端サブコマンドの invocation を識別する実行 ID は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「実行 ID の開始表示」を正本とする。agent call ID および Codex call ID とは識別対象を区別する。

個別 agent call の意味上の責務と判断基準は、対応する oracle doc を正本とする。AgentCallParameter builder は、その oracle doc から明示的に委譲された範囲で、正確な prompt 文面と workload 固有の起動パラメータを構築する。ただし、model provider、Model、および Reasoning Effort は構築対象から除く。

`AgentCallParameter` の field 名、型、および既定値を含む正確な構造は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/basic.py` の `AgentCallParameter` へ委譲する。

## agent call の path context

agent call の path context は、その call に設定する cwd を起点に決める。

| 識別子 | 意味 |
|---|---|
| `agent_call_cwd` | 子 agent call に設定する cwd |
| `work_root` | `agent_call_cwd` を含む最寄りの Git worktree root |
| `repo_root` | `work_root` が属する Git repository の main worktree root |

`AgentCallParameter.agent_call_cwd` は必須の呼び出しパラメータとし、cmoc process の cwd から暗黙に補完してはならない。`work_root` と `repo_root` は、linked worktree、submodule、および separate git directory を含め、Git が保持する repository metadata から導出する。名前が `.git` であるだけの通常の file または directory を、Git repository metadata として扱ってはならない。

path context に関する正確な定義は、次の oracle src へ委譲する。

- call-scoped path context、root placeholder、および Git command を含む導出処理：`{{cmoc-root}}/oracle/src/oracle/other/path_model.py` の `RootPathPlaceHolder`、`AgentCallPathContext`、`resolve_work_root`、および `resolve_repo_root`
- prompt part との受け渡し：`{{cmoc-root}}/oracle/src/oracle/prompt_builder/basic.py` の `PlaceholderMap`
- 完全 prompt への統合：`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt`

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

## Codex CLI 引数による設定上書き

cmoc は、`AgentCallParameter`、`CmocConfig` などから決まる呼び出し単位の設定を、Codex CLI の argv で明示的に上書きする。cmoc が上書きする設定については、`$CODEX_HOME/config.toml` や project config の値に依存してはならない。

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
- Codex CLI 呼び出しにおける Windows toast 通知の effective configuration、`codex exec` と TUI の境界、および callback の検証条件は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` の「Windows toast 通知」を正本とする

## ファイルアクセス制限

### Codex CLI sandbox

すべての Codex CLI 呼び出しで、専用引数 `--sandbox` を明示する。`AgentCallParameter` を使う呼び出しでは、すべての有効な file access mode に `workspace-write` を使う。

| file access mode | sandbox |
|---|---|
| `READONLY`, `PURE_ORACLE_READ`, `REPO_WRITE`, `PURE_ORACLE_WRITE`, `REALIZATION_WRITE`, `NO_POLICY` | `--sandbox workspace-write` |

表にない file access mode を受け取った場合は、sandbox を推測せず Codex CLI 呼び出し前に失敗させる。`AgentCallParameter` を使用しない動作確認用の呼び出しでは `--sandbox read-only` を使う。

`AgentCallParameter.file_access_mode` は、プロンプトで指示する詳細なファイルアクセス制限を選ぶ論理 mode とする。`READONLY` と `PURE_ORACLE_READ` でも検証・調査用の一時作業領域への書き込みを許容し、リポジトリ全体への書き込みを OS sandbox で禁止することは目的としない。

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
- `AGENTS.md` と `INDEX.md` の書き込みを禁止する。
- `{{work-root}}/memo` の読み書きを禁止する。

`NO_POLICY` 以外の各 mode は、共通制限に次の制限を追加する。

| file access mode | 追加制限 |
|---|---|
| `READONLY` | oracle file と realization file の書き込みを禁止する。 |
| `PURE_ORACLE_READ` | oracle file の書き込みと realization file の読み書きを禁止する。 |
| `REPO_WRITE` | 追加の制限を設けない。 |
| `PURE_ORACLE_WRITE` | realization file の読み書きを禁止する。 |
| `REALIZATION_WRITE` | oracle file の書き込みを禁止する。 |

`NO_POLICY` は、共通 file access policy が存在しない有効な特殊 mode とする。本書の「検証・調査用の一時作業領域」の利用規定も共通 prompt からは注入しない。必要な instruction は個別の `AgentCallParameter` builder がすべて構築する。

#### 検証・調査用の一時作業領域

`NO_POLICY` 以外の agent call では、検証・調査用の一時ファイルが必要な場合、agent が `/tmp` 配下に作業専用の一時ディレクトリを作成し、一時作業領域として使用する。一時ファイルはその中に集め、不要になった一時ファイルとディレクトリは agent が削除する。

この作成・利用・後片付けに必要な書き込みだけを、共通制限の「`{{work-root}}` ツリー外への書き込み禁止」の例外とする。他のファイルアクセス禁止は解除しない。一時作業領域へのコピーなどを使って、禁止された読み取りや workload の作業対象・判断材料の制限を迂回してはならない。

workload が限定する編集対象は作業成果物の範囲を表し、この一時作業領域の利用とは区別する。一時作業領域は agent call の cwd、`{{work-root}}`、または Git worktree を置き換えない。固定のディレクトリ名や cmoc による新しい永続管理機構は設けない。

#### 読み取りの範囲

`{{work-root}}` ツリー外であることだけを理由に読み取りを禁止しない。外部ログ、設定、ライブラリ、Git metadata も読み取りを許可する。ただし、この許可は、明示的な読み取り禁止、mode 別のアクセス制限、および workload 固有の閲覧・判断材料の制限を解除しない。MCP や Git の履歴・差分を経由しても、明示的な読み取り禁止を迂回してはならない。

一度読んだ情報の影響を排除できないため、realization file の読み取り禁止は、判断の根拠への採用だけでなく閲覧自体に適用する。また、外部読み取りの許可によって、対象 worktree の正本、追従対象 revision、作業範囲、または編集対象を変更してはならない。

#### prompt の構築と sandbox との関係

`build_file_access_policy` の結果は、共通 file access policy の有無を表す。Python 上の正確な不在値と戻り値型、および一時作業領域の利用規定を含む `NO_POLICY` 以外の mode の正確な prompt 文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/file_access.py` の `build_file_access_policy` へ委譲する。一時作業領域への書き込みの例外は、対象の禁止と同じ file access policy 内で表現する。

`build_complete_prompt` はこの結果に基づいて共通 file access policy の追加可否を決める。完全 prompt への正確な追加条件は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する。

path ごとの読み書き可否などの詳細な制限を sandbox に反映しようとしてはならない。詳細なファイルアクセス制限がプロンプトだけで指示され、sandbox では強制されないことを許容する。

### 書き込み主体の責任分界

agent の直接ファイルアクセス制限は、次の書き込みには適用しない。

- MCP 経由の外部ツールによるファイル書き込み。書き込み先や file access mode を問わない
- Structured Output の受け取り側による保存・更新と、cmoc 自身のログ保存、report 保存、indexing その他の管理処理。各機能が定める出力契約と受理条件に従う。Structured Output 自体がファイルを書き込むわけではない

MCP の責任分界は次のとおりとする。

- cmoc が提供する MCP の書き込みは、各 tool の仕様と検証で管理する。ユーザー設定・プロジェクト設定で追加された MCP の書き込み先を cmoc は制限・保証せず、その制御のための検査や仕組みを追加しない
- MCP の例外はファイルアクセス上の書き込み制限だけに適用し、他の policy、各機能の利用条件、または workload の作業範囲を解除しない

`{{work-root}}/.cmoc` は cmoc の管理領域とする。agent から必要な更新を依頼する場合は、各機能が提供する MCP を使用する。cmoc 自身の管理処理を MCP 経由へ変更する必要はない。

cmoc の管理データは `.cmoc/gt` または `.cmoc/gu` 配下に配置する。所有 root、保存先、Git 追跡・非追跡の責務、および保存記録と作業ファイルの用途・信頼性・lifecycle は、各機能の仕様に従う。アクセス区分を表す `ar`・`aw` の中間階層、それを含む旧配置への互換機構、および旧配置からの自動移行は設けない。

この責任分界を理由に、sandbox、permission profile、network access、または承認設定を拡張してはならない。必要性が確定していない MCP、汎用ファイル操作 MCP、または将来用の管理機構を追加しない。

### permission profile の不使用と動的生成禁止

- cmoc は、入力の種類や伝達経路を問わず、permission profile の生成（動的生成を含む）、更新、選択、Codex CLI への注入、および事前作成された permission profile への依存を行ってはならない
- oracle file が特定の path に対するアクセス制限を要求する場合も、その制限はプロンプトへ反映し、permission profile や path 単位の sandbox 設定へ変換してはならない
- agent-facing な分類文面で伝える Git ignore 判定は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md` の「分類結果」が定める境界だけを表す
- `git check-ignore` の判定結果をファイル分類や対象ファイルの選別に使用してよいが、Codex CLI の sandbox または permission profile を組み立てる入力にしてはならない

## agent call の差分検証

仕様にない検証の追加によって、正常な作業が停止することを防ぐ。

- cmoc は agent call の差分に対し、oracle file が要求する条件の機械的検証だけを行う。
- ファイルアクセス制限や agent の作業範囲の指示だけを根拠に、差分の検証、受理拒否、またはリカバリ処理を追加してはならない。

本節は、agent 自身が守るファイルアクセス制限を緩和せず、通常の実装修正やテスト実行一般を新たに禁止しない。

## Model provider、Model、Reasoning Effort

- agent call ごとの直接設定、値の意味、検証境界、および provider に対する cmoc の責務境界は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「Codex model provider」を正本とする
- cmoc は各 agent call に使用する設定を、同仕様の「agent call ごとの直接設定」と「回復確認 probe の設定例外」に従って取得する
- `cmoc oracle edit` の設定の確定時点と両回での共用は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md` の「ユーザー指示と prompt の構築」に従う
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
- 実経路統合テストで使用する `CmocConfig` の要件は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` の「実経路統合テスト」を正本とする
- cmoc は Model provider、Model、Reasoning Effort の設定情報を Codex CLI プロンプトに注入しない

## プロンプトの渡し方

prompt の一般規則は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization.md` の「oracle doc と oracle src の正本責務」から「正本責務に基づく優先関係」までを正本とする。本節は prompt 固有の規則だけを定義する。

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

独立した role または role 用の構造は設けない。agent call の機械的な識別は `AgentCallParameter.agent_call_kind` が担う。評価方向または責務に意味がある場合は、task の行為と判断対象、named policy、または call 固有の static prompt で具体化する。

objective は、専用機構が所有する次の内容を重複させない。

- 権限と一般的なアクセス禁止は、`AgentCallParameter.file_access_mode` と file access policy が所有する。
- 再利用する判断基準と作業規定は、named policy が所有する。
- call 固有の判断基準と、schema 外の決定論的事後条件は、caller の static prompt が所有する。
- runtime input は、caller の dynamic prompt が所有する。
- Structured Output の構造と schema で表現できる出力要件は、`AgentCallParameter.structured_output_schema_path` が指す schema が所有する。

objective の外側の block、正確な引数、項目名、構築順序、任意項目の省略条件、および rendering は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する。

### call 固有の実行時指示の優先関係

`prompt > oracle file > installed skill` と表現される優先関係は、cmoc の恒常的な意味仕様ではなく、call 固有の目的、作業範囲、入力、および権限に適用する。この正確な agent-facing literal は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/oracle.py` の `build_oracle_policy` へ委譲する。

call 固有の実行時指示の優先関係は、prompt literal に cmoc の新しい意味仕様を作る権限を与えない。prompt literal と oracle doc が所有する意味仕様が食い違う場合は、prompt literal による仕様変更とは扱わず、oracle file 間の不整合として扱う。

### SDPolicy の例外

`SDPolicy.exception` は、同じ `SDPolicy` 内の「必須」「禁止」「許容」に優越する。他の policy、個別機能の利用条件、または workload 全体の制限を解除するものではない。

カテゴリの正確な構造と agent 向け表示は、`{{cmoc-root}}/oracle/src/oracle/other/struct_doc.py` の `SDPolicy` と `_render_sd_policy_as_markdown` へ委譲する。

### Git 差分の参照入力

初期 prompt の文字数を差分本文の大きさや変更 path 数に比例させないため、cmoc が Git 差分を agent の判断材料として自動付加する場合は、取得に必要な参照情報だけを渡す。差分本文や変更 path 一覧は渡さない。agent が取得した差分も会話の入力となるため、総トークン数の削減は保証しない。

- 比較する repository、比較範囲、および対象条件は個別 workload が所有する。agent はその指定に従って必要な差分を Git から取得する
- 取得失敗を正常に取得できた空差分として扱ってはならない。取得できない場合は個別 workload の既存の失敗処理に従い、独立した状態や追加の agent call を設けない
- cmoc 自身が行う差分検査、変更 path の検証、空差分判定、および commit・rollback の責務は廃止・緩和しない
- ユーザー自身が入力する文章に差分を含めることは禁止しない
- Git command の具体的な組み合わせ、差分を読む回数・分割方法、および表示形式は固定しない。新しい汎用の差分入力 schema、永続 state、差分保存ファイル、root placeholder の追加は目的としない

### prompt の構築と受け渡し

`AgentCallParameter.prompt` には、原則として完全 prompt 本文を設定する。cmoc は、builder が生成して確定した値を変更せず、初回 Codex call に渡す。realization implementation は、prompt 本文に独自の指示、注意書き、説明、整形、要約、補完、翻訳、補助文脈、モデル・reasoning effort 情報、その他の意味変更を加えてはならない。

- 完全 prompt の共通構築順序は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する。同関数が、prompt part、目的、および placeholder 定義を統合する正確な順序を所有する
- prompt の共通 rendering は、`{{cmoc-root}}/oracle/src/oracle/other/struct_doc.py` の `render_sd_node_as_markdown` へ委譲する。同関数が、構造化された prompt を Markdown 文字列へ変換する正確な rendering を所有する

prompt の確定前後に行う処理は、次のように区別する。

- editor input handoff の本文生成と送信元情報の注入は、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「本文の生成」に従い、受信側の editor input 確定前に完結させる。
- Structured Output の補正 prompt は、本書の「同じ session での出力補正」に従い、次の turn の入力として構築する。初回 prompt は加工しない。
- Codex CLI の実行形式に必要な保存、stdin 入力、末尾改行などの機械的処理は、プロンプトの意味内容を変更しない範囲に限って許可する。

`AgentCallParameter.prompt` は、`{{repo-root}}/.cmoc/gu/log/codex/{{time-stamp}}_prompt.md` に保存する。初回 Codex call のコマンド末尾に `-` を付け、このファイルを stdin へリダイレクト入力する。

プロンプト本文を argv に載せてはならない。argv に載せてよいのは、フラグ、モデル名、設定上書き値、短い固定文字列、短いファイルパスのみとする。

## feedback reporter と collector context

- reporting の意味は `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「agent による報告」を正本とする。正確な agent 向け文面と完全 prompt への配置は、同文書が参照する oracle src を正本とする
- cmoc は Codex call の開始前に、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「collector と transport」が定める call context と capability を登録し、call-scoped な local stdio MCP reporter/client を利用可能にする
- cmoc は call-scoped な Codex CLI `--config` override により、MCP server namespace `cmoc_feedback`、公開 tool `submit_observation`、同 tool の approval behavior、および MCP process に必要な起動情報を設定する
- cmoc は、`cmoc_feedback` の effective configuration 全体を呼び出し単位で管理する。user config、`$CODEX_HOME/config.toml`、または project config にある次の情報には依存してはならない。また、これらの設定によって、別 tool の公開または reporter の置換を許してはならない
    - server 定義
    - tool 設定
    - approval behavior
    - 起動情報
- 通常の `cmoc_feedback.submit_observation` は、human approval、auto-review、または command sandbox escalation を要求せずに実行できるよう設定する
- reporter と collector の残りの lifecycle は、同仕様の「collector と transport」を正本とする。初回 prompt で注入済みの reporting instruction は、correction schema または correction prompt へ重複させない

## editor input handoff MCP

editor input handoff の利用条件と agent の責務は、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「agent の責務と権限」を正本とする。

- `AgentCallParameter.enable_editor_input_handoff_mcp` は、`cmoc_editor_input` MCP server の有効化を呼び出し単位で指定する。field の正確な型と既定値は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/basic.py` の `AgentCallParameter` へ委譲する
- Codex TUI を起動する `AgentCallParameter` builder だけが、MCP と handoff instruction の両方を有効にする。それ以外の builder は `enable_editor_input_handoff_mcp` の既定値を使用する
- 有効な Codex TUI call には `cmoc_editor_input` MCP server を提供する。handoff ガイド取得と上書きの公開 tool は、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「MCP interface」に従う。MCP の提供によって、sandbox、network access、file access mode、または agent call の成功条件を変更してはならない
- handoff instruction は MCP の有効化とは別に `build_complete_prompt` の `editor_input_handoff_policy` で選択する。正確な定義と配置は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する
- handoff instruction の正確な agent 向け文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/editor_input_handoff.py` の `build_editor_input_handoff_policy` へ委譲する
- `cmoc tui` と `cmoc oracle investigation` では、cmoc の起動・呼び出し管理経路が、送信元 TUI process に対応する実際の送信元情報を MCP の呼び出し元コンテキストへ供給する。情報の意味、process 間の分離、および正確な構造の委譲は、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` の「送信元情報」と「正本の分担」に従う
- TUI process の起動前に、その process の Codex call ID の確保、MCP への送信元情報の供給、および `{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「TUI 送信元情報の記録」に従う記録と flush を完了する。ログの対応付けと MCP への供給には同じ実際の値を使い、indexing など別の Codex call の ID を代用せず、TUI 起動時に別の ID を再発行しない
- この準備を skeleton 構築の前提にはしない。送信元情報は、skeleton と入力確定後の TUI prompt のいずれの builder 引数にも含めず、転記用の情報を prompt へ注入しない

## Codex CLI 呼び出し情報の保存

- Codex CLI 呼び出しに関する情報は `{{repo-root}}/.cmoc/gu/log/codex/{{time-stamp}}_call.json` に保存すること
- `{{time-stamp}}_stdout.jsonl`, `{{time-stamp}}_stderr.log`, `{{time-stamp}}_output.json` に残らない情報だけを `{{time-stamp}}_call.json` に書くこと
- 同一の Codex CLI 呼び出しでは、`{{time-stamp}}` を一致させる
- 初回、補正、retry、回復待ち後の再開、および各 probe の Codex call ごとに、別の `{{time-stamp}}` と log 一式を作成する
- 後続の Codex call は、先行する Codex call の log または出力を上書きしてはならない
- 停止した呼び出しと probe・再開の対応、および各確認結果は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「診断記録」に従ってサブコマンドログから追跡可能にする

## stdout, stderr の扱い

- `--json` を必ず指定すること
- stdout は `{{repo-root}}/.cmoc/gu/log/codex/{{time-stamp}}_stdout.jsonl` に出力すること
- stderr は `{{repo-root}}/.cmoc/gu/log/codex/{{time-stamp}}_stderr.log` に出力すること
- stdout, stderr をコンソールに出力しないこと

## Codex session ID

- Codex call の session ID は、対応する `{{repo-root}}/.cmoc/gu/log/codex/{{time-stamp}}_stdout.jsonl` から読み取る
- `type == thread.started` である要素の `thread_id` field を session ID とする

    ```json
    {"type":"thread.started","thread_id":"019efe07-4886-7423-b252-625febbe31eb"}
    ```

## `--output-last-message`

- `--output-last-message {{repo-root}}/.cmoc/gu/log/codex/{{time-stamp}}_output.json` を必ず指定すること
- cmoc が Codex CLI の作業結果を取り出す必要がある場合、`{{time-stamp}}_output.json` から読み出すこと

## Structured Output

- Codex CLI に Structured Output を要求する場合は、必ず `--output-schema` を使うこと
- `--output-schema` を使わずにプロンプト上だけで JSON 出力を要求するのは禁止
- スキーマは、一度 `{{repo-root}}/.cmoc/gu/schema/{{hash}}.json` に保存して、これを Codex CLI に参照させること
- `{{hash}}` は schema 本文の SHA256 ハッシュとする
- Structured Output の出力要件は、JSON Schema で説明できる限り schema だけで説明し、schema を正本とする。対象は次の事項とする
    - field の意味
    - 型
    - 必須性
    - 列挙値
    - 配列要素数
    - 入れ子
    - field 間の構造的な組み合わせ
- 出力要件を schema と prompt の両方で説明してはならない。prompt には schema で説明できない要件だけを記載する
- 実行時状態との照合が必要で schema に置けない決定論的事後条件は、workload 固有の oracle doc を正本とする。対応する AgentCallParameter builder は、その正確な agent 向け文面を所有する
- schema または宣言済みの決定論的事後条件に含まれない意味的品質を、機械的な受理条件にしてはならない
- 次の agent call では、Structured Output の自然言語部分を原則として日本語とする
    - realization refactor
    - feedback issue remediation
- 対象の Structured Output でも、識別子、path、command、log 原文、および引用は元の表記を維持してよい

### 機械的検証と正式な結果

- 初回と補正の各 Structured Output に、次の機械的検証を同じ順序で行う
    1. JSON parse
    2. JSON Schema validation
    3. 初回 prompt で宣言された決定論的事後条件の検証
- cmoc が正式な結果として解釈してよいのは、最後に全検証に合格した出力だけとする
- 検証に不合格だった出力を、部分的な結果、fallback、または後続処理の入力として解釈してはいけない
- 不合格だった出力と、初回および各補正の Codex call log は、破棄、上書き、または改変してはいけない

### 同じ session での出力補正

- JSON parse、JSON Schema validation、または宣言済みの決定論的事後条件の検証に不合格だった場合は、出力補正可能な失敗として扱う
- 初回 Codex call 後の補正は、初回と同じ Codex session に対する `codex exec resume` で行う
- session ID を取得できず同じ session を再開できない場合は、新しい session で代替せず、出力修正だけでは解消できない失敗として扱う
- 補正 prompt では、同じ schema に従う完全な置換出力を返すよう依頼する。差分、patch、または不合格出力の一部分だけを返すよう依頼してはいけない
- 補正 prompt では、作業成果物を変更せず Structured Output だけを修正するよう明示する
- 補正 prompt には、検出できた検証エラーを出力修正に必要な範囲でまとめる
- 各検証エラーには、違反した条件、対象 field または位置、期待値、および観測値を含める
- 補正 prompt で、初回応答前に宣言されていなかった受理条件を追加してはいけない
- 補正 Codex call は初回 Codex call 後に最大 2 回まで行う。したがって、出力生成 turn は初回を含めて最大 3 回とする
- 回復待ち、待機理由の変更、probe の成功、または再開後の再発によって、補正回数の上限をリセットしてはならない
- 出力補正の間隔を開ける必要はない

### 補正 turn の実行条件

- 補正 turn は Structured Output の修正専用とし、作業成果物を変更させてはいけない
- 初回 Codex call 完了時に、agent call の開始前を基準とする作業成果物の差分を固定する
- Codex call ごとの prompt、log、および Structured Output schema の保存物は、本節でいう作業成果物の差分に含めない
- 補正中は、固定した差分を変動させてはいけない。補正 turn が差分を変動させた場合は、初回 Codex call 完了時の状態へ戻し、出力修正だけでは解消できない失敗として扱う
- 補正 turn では indexing preflight を再実行しない
- 補正 turn の cwd と Structured Output schema は、元の agent call と整合させる

### 補正不能時の扱い

- 最大 2 回の補正後も検証に合格しない場合は、検証を緩和せず既存のエラー処理へ移る
- prompt、schema、および validator が矛盾している場合は、補正によって矛盾を隠そうとせず既存のエラー処理へ移る
- 作業成果物の差分変動、session の再開不能、またはその他の出力修正だけでは解消できない失敗も、検証を緩和せず既存のエラー処理へ移る
- Structured Output の正式な結果を得られず既存のエラー処理へ移る場合は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「rule registry」が定める `codex.structured_output_validation_exhausted` v1 event を、同仕様の安定 field とともに subcommand log へ記録する

## `codex exec` の並列呼び出し

- fork-join 的な並列化が可能な場合は `codex exec` を並列実行してもよい
- ただし、最大並列数は `CmocConfig.num_parallel` で制限すること

## `codex exec` が失敗した場合

### 基本的な考え方

一時的な利用不能によって、それまでの作業を失ったり、本来の作業を繰り返して浪費したりすることを避ける。cmoc が管理する `codex exec` と `codex exec resume` が quota 枯渇または対象の一時障害で失敗した場合は、呼び出しを保留し、最小限の回復確認 probe で利用可能になるまで待つ。TUI 内部と、その他の外部処理には、この回復待ちを適用しない。

### 最終的な成功と失敗の判断

- CLI の正常終了と、当該 Codex call の最終的な成功をともに確認できた場合は、途中にエラーが記録されていても通常の出力取得・検証へ進む。途中のエラー記録だけで回復待ちを開始してはならない
- 成功を確認できない場合や終端情報が矛盾する場合は、回復済みと推定しない。最終的な失敗を識別できる診断に基づいて以下の分類を行い、原因を判別できなければ回復待ちの対象外とする
- CLI の実行成功と、Structured Output を正式な結果として受理できることは区別する。出力受理には本書の「機械的検証と正式な結果」を適用する

### Structured Output の出力契約違反

- Structured Output の機械的検証に不合格だった場合は、回復待ちへ入れず、本書の「同じ session での出力補正」に従う
- schema または宣言済みの決定論的事後条件に含まれない意味的な判定を、出力補正の開始条件にしてはいけない
- 補正用の CLI 呼び出し自体が quota 枯渇または対象の一時障害で停止した場合には回復待ちを適用するが、補正上限、同じ session の再開、および「補正 turn の実行条件」は維持する。これらを満たして再開できない場合は「補正不能時の扱い」に従う

### quota 枯渇・レートリミットで停止した場合

本書の「最終的な成功と失敗の判断」を経て、Codex call の最終的な失敗が stdout JSONL の次の明示的診断によるものと確認できる場合は、quota 枯渇に分類する。例えば、5h limit または weekly limit が枯渇し、credits もない場合が該当する。

- `{"type":"error","message":"...Quota exceeded..."}`
- `{"type":"turn.failed","error":{"message":"...Quota exceeded..."}}`
- `{"type":"error","message":"...You've hit your usage limit..."}`
- `{"type":"turn.failed","error":{"message":"...You've hit your usage limit..."}}`
- `{"type":"error","message":"...out of credits.."}`
- `{"type":"turn.failed","error":{"message":"...out of credits..."}}`
- `{"type":"error","message":"...You hit your spend cap..."}`
- `{"type":"turn.failed","error":{"message":"...You hit your spend cap..."}}`

### 一時障害で失敗した場合

一時障害は、Codex CLI と選択した model provider の間の一時的な利用不能と識別できる失敗に限る。基本対象は、Codex call の最終的な失敗が stdout JSONL の次の診断によるものと確認できる capacity 不足とする。

- `{"type":"error", "message": "...Selected model is at capacity..."}`
- `{"type":"turn.failed", "error":{"message": "...Selected model is at capacity..."}}`

capacity 以外を対象に含める場合も、CLI と provider 間の一時的な利用不能と識別できることを必要条件とする。作業中の command、tool、または別の外部処理の失敗を、Codex CLI 自体の一時障害として扱ってはならない。具体的な追加診断の採否は、本書の「未確定事項」で区別する。

capacity 不足も本書の「回復待ちと再開」に従う。短時間 retry を先行させる段階は要求しない。

### 回復待ちの対象外

quota 枯渇にも対象の一時障害にも分類できない失敗では、回復待ちへ入らず終了処理へ移る。認証・設定不備、恒久エラー、および原因不明の失敗がこれに該当する。HTTP status や「タイムアウト」などの語だけで、一時障害と断定してはならない。

### 回復確認 probe

probe は、停止した本来の作業を進めず、短い応答を 1 回返して利用可能性を確認する呼び出しとする。

- 停止した呼び出しとは別の Codex session で、読み取り専用で実行する。追加の調査や作業を行わない
- probe は 1 回の確認結果を返す。probe 自身の失敗から、別の回復待ちを再帰的に開始してはならない
- 無応答が続く場合も有限時間でその確認を終え、成功を確認できなかった失敗として分類する。無応答だけから、復旧または以前と同じ待機理由を推定しない
- 本書の「最終的な成功と失敗の判断」に従って当該 Codex call の成功を確認し、所定の短い応答も得られた場合だけ、再開を試みるための成功とする。probe の成功を、本来の作業の成功として扱ってはならない

probe の設定取得と、一時障害の確認に必要な設定継承は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「回復確認 probe の設定例外」を正本とする。

quota availability probe の正確な prompt 文面、prompt part の選択、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/quota_probe.py` の `build_quota_availability_probe_parameter` へ委譲する。回復確認の目的、成功条件、待機・再開の判断は本書が所有し、builder または generated prompt へ委譲しない。

### 回復待ちと再開

#### 待機理由と確認間隔

quota と一時障害の回復待ちは、次の共通規則に従う。

- 待機中は、それまでの作業状態と呼び出し記録を保持する
- quota の確認は 30 分に 1 回とする。一時障害の確認間隔は「未確定事項」に従い、quota の間隔と混同しない
- probe の直近の確認結果が quota または対象の一時障害なら、その理由で待機する。理由が変わった場合は、待機理由と確認間隔を切り替えて通知する
- 対象外の失敗へ変わった場合は、以前の理由で待ち続けず、待機を終了してエラー処理へ移る
- 回復待ちを確認回数または総待機時間だけで自動打切りしてはならない。復旧、対象外の失敗、または適用対象で受理したユーザー中断まで待機する。probe 1 回の無応答を打ち切ることは、総待機時間の上限とは区別する

#### 並列呼び出しの確認結果共有

復旧確認に関わる呼び出し条件と待機理由が同じで、probe の設定継承の適用範囲を含めて確認結果を適用できると分かる範囲では、代表一つの probe を共有する。条件の同等性が分からない呼び出しへ成功結果を広げてはならない。理由が変わった場合もこの共有条件を満たす範囲で扱う。

#### 復旧後の再開と再発

probe が成功したら、保留していた呼び出しの再開を試みる。通常の作業呼び出しは、次の規則に従う。

- 再開対象の session ID は、本書の「Codex session ID」に従って、停止した Codex call の stdout JSONL から取得する。同じ agent call で既に特定できた元の session ID は保持し、後続 call で再取得できないことだけを理由に未取得扱いにしない
- session ID を取得できた場合は、その session を `codex exec resume` で復元し、停止した呼び出しと同じ prompt、同じ設定で実行する
- session ID を取得できない場合は、同じ prompt と設定で再実行する
- session ID があるのに再開できない場合は、新しい session へ自動で切り替えず、失敗として終了処理へ移る。ただし、再開用 CLI 呼び出しの失敗が quota または対象の一時障害なら、再分類して回復待ちへ戻る

Structured Output の補正には、本書の「同じ session での出力補正」と「補正 turn の実行条件」を優先する。補正の session を特定できない場合を、通常の作業呼び出しの再実行で代替してはならない。

再開後も、最終的な成功・失敗の判断と出力検証を省略しない。quota または対象の一時障害が再発した場合は、改めて分類した理由で待機へ戻る。

#### 中断と終了処理

ユーザー中断の対象と優先関係は、`{{cmoc-root}}/oracle/doc/app_spec/subcommand_interruption.md` の「対象」と「共通動作」に従う。回復待ちを導入したことだけを根拠に、中断対象外のサブコマンドへ正常中断を追加してはならない。

待機対象外の失敗または再開不能で続行を断念する場合は、`{{cmoc-root}}/oracle/doc/app_spec/error_handling.md` の「エラー分類」と「エラー終了の確定」に従う。終了時の commit、rollback、部分成果、および state の扱いは各 workload の正本を維持し、共通の回復処理で一律に変更しない。特に、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_edit.md` の「終了と差分」に対する自動 rollback を追加してはならない。

#### 表示と記録

待機理由、継続、次回確認、理由変更、復旧後の再開、および待機終了の console 表示は、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` の「進行通知」に従う。各 probe とその結果、呼び出しとの対応、および待機時間を含む経過は、同仕様の「診断記録」に従う。

### 未確定事項

次の事項は、採用済みの回復待ち方針から区別して未確定のまま残す。

- 一時障害の確認間隔。5 分は暫定候補であり、確定値ではない
- capacity 以外の具体的な診断集合と厳密な対応表。HTTP 503、接続断、応答タイムアウトは追加候補であり、個別診断の採否は未確定とする。対象範囲の境界は「一時障害で失敗した場合」に従う
- probe の設定継承を、一時障害の確認を含まない既存 quota 待機全体にも適用するか。確定済みの例外と理由変更時の適用範囲は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` の「回復確認 probe の設定例外」に従う
- 中断対象外サブコマンドの長期待機を終了する操作と、そのときの成果の扱い。正常中断の対象を追加するには個別仕様の変更が必要であり、既存の終了・差分規則は維持する

一方、合意した失敗分類を認識する方法、probe の無応答を判定する具体時間、待機の細かな調整、代表 probe の選定、およびログの具体的な項目・文言は、確定済みの振る舞いを満たす範囲で実装裁量とする。この裁量によって、上記の未確定事項を確定済みの人間判断として扱ってはならない。

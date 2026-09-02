# `codex exec` 呼び出し規約

## 基本

- cmoc からの Codex CLI 呼び出しは、原則として `codex exec` で行う
- 個別 agent call の意味上の責務と判断基準は、対応する oracle doc を正本とする
- 個別 agent call の AgentCallParameter builder は、対応する oracle doc が明示的に委譲した範囲で、正確な prompt 文面と、model provider、Model、および Reasoning Effort を除く workload 固有の起動パラメータを構築する
- `AgentCallParameter` の field 名、型、および既定値を含む正確な構造は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/basic.py` の `AgentCallParameter` へ委譲する
- 本書で agent call とは、1 個の `AgentCallParameter` に対する論理的な呼び出し単位を指す
- Structured Output の出力補正を行う場合も、初回 `codex exec` と補正用 `codex exec resume` を合わせて 1 回の agent call とする
- 本書で Codex call とは、初回実行や補正を含む個々の Codex CLI 呼び出しを指す
- cmoc は agent call ごとに、対応する builder を表す安定した低カーディナリティの `agent_call_kind` と一意な agent call ID を付与する
- cmoc は初回、補正、および TUI process ごとに一意な Codex call ID を付与する

## agent call の path context

- `agent_call_cwd` は、子 agent call に設定する cwd とする
- `work_root` は、`agent_call_cwd` を含む最寄りの Git worktree root とする
- `repo_root` は、`work_root` が属する Git repository の main worktree root とする
- `work_root` と `repo_root` は、linked worktree、submodule、および separate git directory を含め、Git が保持する repository metadata から導出する
- 名前が `.git` であるだけの通常の file または directory を Git repository metadata として扱ってはならない
- `AgentCallParameter.agent_call_cwd` は必須の呼び出しパラメータとし、cmoc process の cwd から暗黙に補完してはならない
- call-scoped path context、root placeholder、および Git command を含む導出処理の正確な定義は、`{{cmoc-root}}/oracle/src/oracle/other/path_model.py` の `RootPathPlaceHolder`、`AgentCallPathContext`、`resolve_work_root`、および `resolve_repo_root` へ委譲する。prompt part との受け渡しは `{{cmoc-root}}/oracle/src/oracle/prompt_builder/basic.py` の `PlaceholderMap`、完全 prompt への統合は `{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する

### `{{work-root}}` に対する仮定

cmoc による操作対象 worktree である `{{work-root}}` は、次の要件を満たすものと仮定する。

- git で管理されている
- `{{work-root}}/oracle` 配下に断片的な正本情報が記載されている（`{{cmoc-root}}` 配下がそうであるように）
- `{{work-root}}` に固有の作業のノウハウは、Codex CLI が参照可能な追跡対象の文書、設定、script、または skill としてリポジトリ上に用意されている
- `{{work-root}}/oracle` 配下の file 別に `codex exec` session を起動する責任は cmoc が負う
- 言語、framework、tool 固有の手順を用意する責任は `{{work-root}}` が負い、その配置先を `.agents/skills` に限定しない

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

- cmoc 呼び出し時点で `$CODEX_HOME` が設定済みであるなら、それをそのまま Codex CLI に渡す
- cmoc 呼び出し時点で `$CODEX_HOME` が未設定であるなら、`CODEX_HOME=${HOME}/.codex` 相当の絶対パスを設定して Codex CLI に渡す

## preflight validation

- cmoc は Codex CLI 呼び出し前に「Codex CLI が実際に参照する `$CODEX_HOME`」に対する preflight validation を行う
- preflight validation では `$CODEX_HOME` がディレクトリとして存在することを確かめる
- model provider 固有の認証要件を cmoc が一律に検証してはならない
- preflight validation に失敗した場合、cmoc の実行を即時失敗させる

## Codex CLI 引数による設定上書き

- cmoc は Codex CLI 呼び出しに `--profile` (`-p`) を指定してはならない
- cmoc は Codex CLI 呼び出しのために `$CODEX_HOME/{{name}}.config.toml` を生成してはならない
- `AgentCallParameter`, `CmocConfig` などから決まる呼び出し単位の設定は、Codex CLI の argv で明示的に上書きする
- 上書き対象に専用引数が存在する場合は専用引数を使う
- 専用引数が存在しない設定は、`--config` (`-c`) と `key=value` 形式の設定値を使って上書きする
    - `--config` は設定項目ごとに繰り返してよい
    - `key=value` は 1 個の argv 要素として渡す
    - `value` は Codex CLI が解釈する TOML 値とする
- cmoc が上書きする設定について、`$CODEX_HOME/config.toml` や project config の値に依存してはならない
- 全ての Codex CLI 呼び出しで、次の承認設定を呼び出し単位の argv により明示的に上書きする
    - `approval_policy`: `"on-request"`
    - `approvals_reviewer`: `"auto_review"`
- Codex CLI 呼び出しにおける Windows toast 通知の effective configuration、`codex exec` と TUI の境界、および callback の検証条件は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする

## ファイルアクセス制限

### Codex CLI sandbox

- 全ての Codex CLI 呼び出しで、専用引数 `--sandbox` を明示する
- `--sandbox` の値は `read-only` または `workspace-write` のどちらかに限定する
- `AgentCallParameter.file_access_mode` は次のように `--sandbox` へ対応付ける
    - `READONLY`, `PURE_ORACLE_READ`: `--sandbox read-only`
    - `REPO_WRITE`, `PURE_ORACLE_WRITE`, `REALIZATION_WRITE`, `NO_POLICY`: `--sandbox workspace-write`
- `AgentCallParameter` を使用しない動作確認用の Codex CLI 呼び出しでは `--sandbox read-only` を使う
- 上記にない file access mode を受け取った場合は、sandbox を推測せず Codex CLI 呼び出し前に失敗させる
- `$CODEX_HOME/config.toml` や project config の sandbox 設定に依存してはならない
- sandbox は専用引数で指定し、`--config` で上書きしてはならない

### command 単位の sandbox 外実行

- `--sandbox` は agent call 内で実行する command の既定境界を定めるものとし、承認済みの command 単位 sandbox escalation まで禁止するものではない
- command 単位 sandbox escalation は、作業固有の oracle file が sandbox 外実行を必要条件として明示し、agent が対象 command と理由を限定して要求する場合に限り許容する
- escalation は対象 command とその descendant process だけへ適用し、agent call 全体の sandbox mode、`AgentCallParameter.file_access_mode`、または詳細なファイルアクセス制限を変更しない
- command 単位 escalation のために `--sandbox danger-full-access` または `--dangerously-bypass-approvals-and-sandbox` を agent call 全体へ指定してはならない
- cmoc 自己開発の GPU test に許容する command と具体的な escalation 手順は、`{{cmoc-root}}/oracle/doc/dev_rule/test_execution.md` を正本とする
- GPU test の具体的な手順も、この節が定める一般的な command 単位 escalation 境界を広げてはいけない
- cmoc は command 単位 escalation のための Codex exec rule を生成せず、永続的な prefix allow rule に依存しない

### model provider transport と Codex sandbox のネットワークアクセス

- Codex CLI と model provider の間の transport は、Codex agent が sandbox 内で実行する command のネットワークアクセスとは別のものとして扱う
- model provider の選択または provider-local 設定を理由に、Codex sandbox のネットワークアクセス設定を追加または変更してはならない
- agent が実行する command にネットワークアクセスが必要な場合は、model provider 設定とは独立して扱う

### 詳細なファイルアクセス制限

- 詳細なファイルアクセス制限は deny-list とする。共通制限または各 mode の追加制限で禁止されていない読み書きは許可する
- `NO_POLICY` 以外の全 file access mode では、次の制限を共通で適用する
    - `{{work-root}}` と `{{repo-root}}` が同一の場合は、`{{work-root}}` ツリー外の読み書きを禁止する。両者が異なる場合は、`{{work-root}}` ツリー外かつ `{{repo-root}}/.cmoc/g*/ar` ツリー外の読み書きを禁止する
    - `{{work-root}}/.git`、`{{work-root}}/.agents`、`{{work-root}}/.codex`、および `{{work-root}}/.cmoc/g*/ar` ツリー内の書き込みを禁止する。`{{work-root}}` と `{{repo-root}}` が異なる場合は、`{{repo-root}}/.cmoc/g*/ar` ツリー内の書き込みも禁止する
    - `AGENTS.md` と `INDEX.md` の書き込みを禁止する
    - `{{work-root}}/memo` の読み書きを禁止する
- `NO_POLICY` 以外の各 mode は、共通制限に次の制限を追加する
    - `READONLY`: oracle file と realization file の書き込みを禁止する
    - `PURE_ORACLE_READ`: oracle file の書き込みと realization file の読み書きを禁止する
    - `REPO_WRITE`: 追加の制限を設けない
    - `PURE_ORACLE_WRITE`: realization file の読み書きを禁止する
    - `REALIZATION_WRITE`: oracle file の書き込みを禁止する
- `NO_POLICY` は、共通 file access policy が存在しない有効な特殊 mode とする。必要な instruction は個別の `AgentCallParameter` builder がすべて構築する
- 個別 agent call が選択する file access mode は、対応する oracle doc の作業範囲と一致させる。AgentCallParameter builder は、その正確な選択値を構築する
- `build_file_access_policy` の結果は、共通 file access policy の有無を表す。Python 上の正確な不在値と戻り値型、および `NO_POLICY` 以外の mode の正確な prompt 文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/file_access.py` の `build_file_access_policy` へ委譲する
- `build_complete_prompt` はその結果を処理し、共通 file access policy の追加可否を決める。完全 prompt への正確な追加条件は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する
- path ごとの読み書き可否など、`read-only` と `workspace-write` だけでは表現できない制限を sandbox に反映しようとしてはならない
- 詳細なファイルアクセス制限がプロンプトだけで指示され、sandbox では強制されないことを許容する

### permission profile の不使用と動的生成禁止

- cmoc は、動的生成を含め、permission profile の生成、更新、選択、Codex CLI への注入、および事前作成された permission profile への依存をしてはならない
- この禁止は動的生成の入力の種類を問わず、`AgentCallParameter`、file access mode、プロンプト、oracle file、設定、実在 path、ファイル一覧、`.gitignore` の規則、`git check-ignore` の判定結果、およびそれらの組み合わせを入力とする場合を含む
- permission profile を一時ファイル、設定ファイル、argv、環境変数、`--config` など、いかなる経路でも Codex CLI に注入してはならない
- oracle file が特定の path に対するアクセス制限を要求する場合も、その制限はプロンプトへ反映し、permission profile や path 単位の sandbox 設定へ変換してはならない
- agent-facing な分類文面で伝える Git ignore 判定は、`{{cmoc-root}}/oracle/doc/app_spec/oracle_and_realization_file_enumeration.md` の「分類結果」が定める境界だけを表す
- `git check-ignore` の判定結果をファイル分類や対象ファイルの選別に使用してよいが、Codex CLI の sandbox または permission profile を組み立てる入力にしてはならない

## ファイルアクセス制限違反の事後検証とリカバリ

- agent call が発生させた差分がファイルアクセス制限に違反していないかの事後検証は禁止とする

## Model provider、Model、Reasoning Effort

- agent call ごとの直接設定、値の意味、検証境界、および provider に対する cmoc の責務境界は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` を正本とする
- cmoc は agent call ごとに、`AgentCallParameter.agent_call_kind` を key として `CmocConfigCodex` の対応する設定を取得する
- 取得した model provider、Model、および Reasoning Effort は、初回、Structured Output の補正、retry、および quota 待機後の resume を含む同一 agent call 内の全 Codex call で変更せず使用する
- quota availability probe は独立した agent call とし、probe 自身の `agent_call_kind` に対応する設定を使用する
- Codex CLI に対する Model と Reasoning Effort は、全ての呼び出しで次の argv により明示的に上書きする
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
- model provider の選択と provider-local 設定に `--profile`、`$CODEX_HOME/config.toml`、または project config を使用してはならない
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
- completion criteria は、agent call 終了後に検証可能な call 固有の状態がある場合に設ける。
- non-goals は、隣接作業への逸脱が予想される場合に限り、call 固有の対象外を示す。一般的な禁止操作またはアクセス制限を置かない。

独立した role または role 用の構造は設けない。agent call の機械的な識別は `AgentCallParameter.agent_call_kind` が担う。評価方向または責務に意味がある場合は、task の行為と判断対象、named policy、または call 固有の static prompt で具体化する。

objective は、専用機構が所有する次の内容を重複させない。

- 権限と一般的なアクセス禁止は、`AgentCallParameter.file_access_mode` と file access policy が所有する。
- 再利用する判断基準と作業規定は、named policy が所有する。
- call 固有の判断基準と、schema 外の決定論的事後条件は、caller の static prompt が所有する。
- runtime input は、caller の dynamic prompt が所有する。
- Structured Output の構造と schema で表現できる出力要件は、`AgentCallParameter.structured_output_schema_path` が指す schema が所有する。

Structured Output schema に従うことだけを、completion criteria として重複させてはならない。schema または policy だけでは表現されない call 固有の完了状態がある場合だけ、completion criteria を設ける。

objective の外側の block、正確な引数、項目名、構築順序、任意項目の省略条件、および rendering は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する。

### call 固有の実行時指示の優先関係

`prompt > oracle file > installed skill` と表現される優先関係は、cmoc の恒常的な意味仕様ではなく、call 固有の目的、作業範囲、入力、および権限に適用する。この正確な agent-facing literal は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/oracle.py` の `build_oracle_policy` へ委譲する。

call 固有の実行時指示の優先関係は、prompt literal に cmoc の新しい意味仕様を作る権限を与えない。prompt literal と oracle doc が所有する意味仕様が食い違う場合は、prompt literal による仕様変更とは扱わず、oracle file 間の不整合として扱う。

### prompt の構築と受け渡し

- 完全 prompt の共通構築順序は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する。同関数が、prompt part、目的、および placeholder 定義を統合する正確な順序を所有する
- prompt の共通 rendering は、`{{cmoc-root}}/oracle/src/oracle/other/struct_doc.py` の `render_sd_node_as_markdown` へ委譲する。同関数が、構造化された prompt を Markdown 文字列へ変換する正確な rendering を所有する
- builder が生成した `AgentCallParameter.prompt` は、初回 Codex call の stdin へ渡す入力とする。意味仕様または prompt 文面の正本ではない
- `AgentCallParameter.prompt` には、原則として完全 prompt 本文を設定する
- realization implementation は、prompt 本文に独自の指示、注意書き、説明、整形、要約、補完、翻訳、補助文脈、モデル・reasoning effort 情報、その他の意味変更を加えてはならない
- cmoc は、確定した `AgentCallParameter.prompt` を変更せず、初回 Codex call に渡す
- Structured Output の補正 prompt は、初回 prompt を加工したものではなく、本書の出力補正規則に従う次の turn の入力として構築する
- Codex CLI の実行形式に必要な保存、stdin 入力、末尾改行などの機械的処理は、プロンプトの意味内容を変更しない範囲に限って許可する
- プロンプト本文を argv に載せてはならない
- `AgentCallParameter.prompt` は、`{{repo-root}}/.cmoc/gu/ar/log/codex/{{time-stamp}}_prompt.md` に保存する
- `AgentCallParameter.prompt` は stdin 経由で渡す。コマンド末尾に `-` を付け、`{{time-stamp}}_prompt.md` をリダイレクト入力する
- argv に載せてよいのは、フラグ、モデル名、設定上書き値、短い固定文字列、短いファイルパスのみとする

## feedback reporter と collector context

- reporting の意味は `{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` を正本とする。正確な agent 向け文面と完全 prompt への配置は、同文書が参照する oracle src を正本とする
- cmoc は Codex call の開始前に、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` の「collector と transport」が定める call context と capability を登録し、call-scoped な local stdio MCP reporter/client を利用可能にする
- cmoc は call-scoped な Codex CLI `--config` override により、MCP server namespace `cmoc_feedback`、公開 tool `submit_observation`、同 tool の approval behavior、および MCP process に必要な起動情報を設定する
- cmoc は `cmoc_feedback` の effective configuration 全体を呼び出し単位で支配する。user config、`$CODEX_HOME/config.toml`、または project config の server 定義、tool 設定、approval behavior、および起動情報に依存してはならず、それらによって別 tool の公開または reporter の置換を許してはならない
- 通常の `cmoc_feedback.submit_observation` は、human approval、auto-review、または command sandbox escalation を要求せずに実行できるよう設定する
- reporter と collector の残りの lifecycle は、同仕様の「collector と transport」を正本とする。初回 prompt で注入済みの reporting instruction は、correction schema または correction prompt へ重複させない

## editor input handoff MCP

editor input handoff の意味仕様は、`{{cmoc-root}}/oracle/doc/app_spec/editor_input_handoff.md` を正本とする。

- `AgentCallParameter.enable_editor_input_handoff_mcp` は、`cmoc_editor_input` MCP server の有効化を呼び出し単位で指定する。field の正確な型と既定値は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/basic.py` の `AgentCallParameter` へ委譲する
- Codex TUI を起動する `AgentCallParameter` builder だけが MCP を有効にする。それ以外の builder は既定値を使用する
- 有効な Codex TUI call には、`overwrite` だけを公開する `cmoc_editor_input` MCP server を提供する。MCP の提供によって、sandbox、network access、file access mode、または agent call の成功条件を変更してはならない
- handoff instruction は MCP の有効化とは別に `build_complete_prompt` の `editor_input_handoff_policy` で選択する。正確な定義と配置は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` の `build_complete_prompt` へ委譲する
- Codex TUI の builder は MCP と handoff instruction の両方を有効にする。agent 向け文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/editor_input_handoff.py` の `build_editor_input_handoff_policy` へ委譲する

## Codex CLI 呼び出し情報の保存

- Codex CLI 呼び出しに関する情報は `{{repo-root}}/.cmoc/gu/ar/log/codex/{{time-stamp}}_call.json` に保存すること
- `{{time-stamp}}_stdout.jsonl`, `{{time-stamp}}_stderr.log`, `{{time-stamp}}_output.json` に残らない情報だけを `{{time-stamp}}_call.json` に書くこと
- 同一の Codex CLI 呼び出しの間で `{{time-stamp}}` は一致しなければならない
- 1 回の agent call に初回と補正の複数 Codex call が含まれる場合は、Codex call ごとに別の `{{time-stamp}}` と log 一式を作成する
- 後続の Codex call は、先行する Codex call の log または出力を上書きしてはならない

## stdout, stderr の扱い

- `--json` を必ず指定すること
- stdout は `{{repo-root}}/.cmoc/gu/ar/log/codex/{{time-stamp}}_stdout.jsonl` に出力すること
- stderr は `{{repo-root}}/.cmoc/gu/ar/log/codex/{{time-stamp}}_stderr.log` に出力すること
- stdout, stderr をコンソールには流さないこと

## Codex session ID

- Codex call の session ID は、対応する `{{repo-root}}/.cmoc/gu/ar/log/codex/{{time-stamp}}_stdout.jsonl` から読み取る
- `type == thread.started` である要素の `thread_id` field を session ID とする

    ```json
    {"type":"thread.started","thread_id":"019efe07-4886-7423-b252-625febbe31eb"}
    ```

## `--output-last-message`

- `--output-last-message {{repo-root}}/.cmoc/gu/ar/log/codex/{{time-stamp}}_output.json` を必ず指定すること
- cmoc が Codex CLI の作業結果を取り出す必要がある場合、`{{time-stamp}}_output.json` から読み出すこと

## Structured Output

- Codex CLI に Structured Output を要求する場合は、必ず `--output-schema` を使うこと
- `--output-schema` を使わずにプロンプト上だけで JSON 出力を要求するのは禁止
- スキーマは、一度 `{{repo-root}}/.cmoc/gu/ar/schema/{{hash}}.json` に保存して、これを Codex CLI に参照させること
- `{{hash}}` は schema 本文の SHA256 ハッシュとする
- Structured Output の field の意味、型、必須性、列挙値、配列要素数、入れ子、および field 間の構造的な組み合わせは、JSON Schema で説明できる限り schema だけで説明し、schema を正本とする
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
- cmoc が正式な結果として解釈してよいのは、最後に全検証へ合格した出力だけとする
- 検証へ不合格だった出力を、部分的な結果、fallback、または後続処理の入力として解釈してはいけない
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
- 補正後の出力も、初回出力と同じ機械的検証へ通す
- 補正 Codex call は初回 Codex call 後に最大 2 回まで行う。したがって、出力生成 turn は初回を含めて最大 3 回とする
- 出力補正の間隔を開ける必要はない

### 補正 turn の実行条件

- 補正 turn は Structured Output の修正専用とし、作業成果物を変更させてはいけない
- 初回 Codex call 完了時に、agent call の開始前を基準とする作業成果物の差分を固定する
- Codex call ごとの prompt、log、および Structured Output schema の保存物は、本節でいう作業成果物の差分に含めない
- 補正中は、固定した差分を変動させてはいけない。補正 turn が差分を変動させた場合は、初回 Codex call 完了時の状態へ戻し、出力修正だけでは解消できない失敗として扱う
- 差分不変性の検査を、file access mode 違反の判定またはリカバリに使用してはいけない
- 補正 turn では indexing preflight を再実行しない
- 補正 turn の cwd と Structured Output schema は、元の agent call と整合させる

### 補正不能時の扱い

- 最大 2 回の補正後も検証へ合格しない場合は、検証を緩和せず既存のエラー処理へ移る
- prompt、schema、および validator が矛盾している場合は、補正によって矛盾を隠そうとせず既存のエラー処理へ移る
- 作業成果物の差分変動、session の再開不能、またはその他の出力修正だけでは解消できない失敗も、検証を緩和せず既存のエラー処理へ移る
- Structured Output の正式な結果を得られず既存のエラー処理へ移る場合は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` が定める `codex.structured_output_validation_exhausted` v1 event を、同仕様の安定 field とともに subcommand log へ記録する

## `codex exec` の並列呼び出し

- fork-join 的な並列化が可能な場合は `codex exec` を並列実行しても良い
- ただし、最大並列数は `CmocConfig.num_parallel` で制限すること

## `codex exec` が失敗した場合

### 基本的な考え方

- 異常な状態に基づいた無駄な作業によるトークンの浪費を避けたい
- quota 不足で停止した場合は quota が復活するまで待機・再開してほしい
- OpenAI サーバー側の一時的な問題であることが明白な既知のエラーなら、自動的にリトライしてほしい

### Structured Output の出力契約違反

- Structured Output の機械的検証に不合格だった場合は、本書の「同じ session での出力補正」に従う
- schema または宣言済みの決定論的事後条件に含まれない意味的な判定を、出力補正の開始条件にしてはいけない

### quota 枯渇・レートリミットで停止した場合

- quota が枯渇して Codex CLI の実行が停止した場合、再び実行可能な状態になるまで待機し、再開する
- quota が枯渇とは
    - e.g. 5h limit が枯渇して credits も無い
    - e.g. weekly limit が枯渇して credits も無い
- 再び実行可能な状態とは
    - e.g. 5h limit がリセットされて、元々 weekly limit も残っていたので、実行可能になった
    - e.g. 人間が credits を追加購入した
- 待機とは
    - 動作確認用のミニマルな Codex CLI 呼び出しを定期的に繰り返し実行する（ポーリング待機）
    - 動作確認の間隔は 30 分に１回とする
- quota availability probe の task は短い応答を 1 回返すことに限定し、追加の調査または作業を non-goal とする
- probe の正確な prompt 文面、prompt part の選択、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/quota_probe.py` の `build_quota_availability_probe_parameter` へ委譲する
- 並列に呼び出した Codex CLI 呼び出しが同時に待機に突入した場合
    - 一番最初に待機に入ったスレッドだけが代表してポーリングを行う
    - 複数スレッドで並列にポーリングを行うのは禁止
- 再開対象の session ID は、本書の「Codex session ID」に従って停止した Codex call の stdout JSONL から取得する
- 再開とは
    - 停止した時のセッションを `codex exec ... resume ...` サブコマンドで復元したうえで、全く同じプロンプトで実行する
    - セッション ID の取得に失敗した場合、resume せずに単に同一の設定で再実行する
- quota 枯渇の判定方法
    - `codex exec --json` の stdout JSONL に、以下のいずれかが含まれている場合
        - `{"type":"error","message":"...Quota exceeded..."}`
        - `{"type":"turn.failed","error":{"message":"...Quota exceeded..."}}`
        - `{"type":"error","message":"...You've hit your usage limit..."}`
        - `{"type":"turn.failed","error":{"message":"...You've hit your usage limit..."}}`
        - `{"type":"error","message":"...out of credits.."}`
        - `{"type":"turn.failed","error":{"message":"...out of credits..."}}`
        - `{"type":"error","message":"...You hit your spend cap..."}`
        - `{"type":"turn.failed","error":{"message":"...You hit your spend cap..."}}`
- ユーザー向けメッセージについて
    - quota 枯渇による待機を行う場合、`{{cmoc-root}}/oracle/doc/app_spec/console_and_file_log.md` に従って、待機開始、継続中、および再開を簡潔な進行通知として表示する
    - 動作確認用 Codex call ごとのログパス、経過時間、および戻り値を console へ列挙しない
    - 動作確認用 Codex call とその結果は、サブコマンドログから追跡可能にする

### サーバーの一時的不調で失敗した場合

- `codex exec --json` の stdout JSONL に、以下のいずれかが含まれている場合
    - `{"type":"error", "message": "...Selected model is at capacity..."}`
    - `{"type":"turn.failed", "error":{"message": "...Selected model is at capacity..."}}`
- 8 回までリトライする
- リトライの間隔は 5 sec を初期値として、リトライ失敗 1 回毎に間隔を倍に増やす
- リトライが全て失敗したら、続行しようとせずに即時コマンド全体を失敗させる

### それ以外の想定外のエラー

- 続行しようとしない
- 即時コマンド全体を失敗させる

## `.agents` 配下を編集出来ない問題

- `.agents` ツリー内 Codex CLI で特別扱いされているため、人間が個別に approve しないと編集出来ない
- `codex exec` は個別の approve が出来ないので `{{repo-root}}/.agents` 配下は絶対に編集できない（やろうとしても失敗する）
- `.agents` ツリー内編集は cmoc としても禁止とする

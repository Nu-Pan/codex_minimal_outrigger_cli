# `codex exec` 呼び出し規約

## 基本

- cmoc からの Codex CLI 呼び出しは、原則として `codex exec` で行う
- 個別 agent call の意味上の責務と判断基準は、対応する oracle doc を正本とする
- `{{cmoc-root}}/oracle/src/oracle/acp_builder` ツリー内の AgentCallParameter builder は、個別 agent call の正確な prompt 文面と起動パラメータを構築する
- 本書で agent call とは、1 個の `AgentCallParameter` に対する論理的な呼び出し単位を指す
- Structured Output の出力補正を行う場合も、初回 `codex exec` と補正用 `codex exec resume` を合わせて 1 回の agent call とする
- 本書で Codex call とは、初回実行や補正を含む個々の Codex CLI 呼び出しを指す
- cmoc は agent call ごとに、対応する builder を表す安定した低カーディナリティの `agent_call_kind` と一意な agent call ID を付与する
- cmoc は初回、補正、および TUI process ごとに一意な Codex call ID を付与する

## agent call の path context

- `agent_call_cwd` は、子 agent call に設定する cwd とする
- `work_root` は、`agent_call_cwd` を含む最寄りの Git worktree root とする
- `repo_root` は、`work_root` が属する Git repository の main worktree root とする
- `AgentCallParameter.agent_call_cwd` は必須の呼び出しパラメータとし、cmoc process の cwd から暗黙に補完してはならない
- call-scoped path context、root placeholder、および導出処理の正確な定義は、`{{cmoc-root}}/oracle/src/oracle/other/path_model.py` を参照する。prompt part との受け渡しは `{{cmoc-root}}/oracle/src/oracle/prompt_builder/basic.py`、完全 prompt への統合は `{{cmoc-root}}/oracle/src/oracle/prompt_builder/complete_prompt.py` を参照する

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
- 全 file access mode では、次の制限を共通で適用する
    - `{{work-root}}` と `{{repo-root}}` が同一の場合は、`{{work-root}}` ツリー外の読み書きを禁止する。両者が異なる場合は、`{{work-root}}` ツリー外かつ `{{repo-root}}/.cmoc/g*/ar` ツリー外の読み書きを禁止する
    - `{{work-root}}/.git`、`{{work-root}}/.agents`、`{{work-root}}/.codex`、および `{{work-root}}/.cmoc/g*/ar` ツリー内の書き込みを禁止する。`{{work-root}}` と `{{repo-root}}` が異なる場合は、`{{repo-root}}/.cmoc/g*/ar` ツリー内の書き込みも禁止する
    - `AGENTS.md` と `INDEX.md` の書き込みを禁止する
    - `{{work-root}}/memo` の読み書きを禁止する
- 各 mode は、共通制限に次の制限を追加する
    - `READONLY`: oracle file と realization file の書き込みを禁止する
    - `PURE_ORACLE_READ`: oracle file の書き込みと realization file の読み書きを禁止する
    - `REPO_WRITE`: 追加の制限を設けない
    - `PURE_ORACLE_WRITE`: realization file の読み書きを禁止する
    - `REALIZATION_WRITE`: oracle file の書き込みを禁止する
    - `NO_POLICY`: 詳細な file access instruction を prompt に追加しない特殊 mode とする
- 個別 agent call が選択する file access mode は、対応する oracle doc の作業範囲と一致させる。AgentCallParameter builder は、その正確な選択値を構築する
- 本節の制限を agent へ伝える正確な prompt 文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/file_access.py` を参照する
- path ごとの読み書き可否など、`read-only` と `workspace-write` だけでは表現できない制限を sandbox に反映しようとしてはならない
- 詳細なファイルアクセス制限がプロンプトだけで指示され、sandbox では強制されないことを許容する

### permission profile の不使用と動的生成禁止

- cmoc は、動的生成を含め、permission profile の生成、更新、選択、Codex CLI への注入、および事前作成された permission profile への依存をしてはならない
- この禁止は動的生成の入力の種類を問わず、`AgentCallParameter`、file access mode、プロンプト、oracle file、設定、実在 path、ファイル一覧、`.gitignore` の規則、`git check-ignore` の判定結果、およびそれらの組み合わせを入力とする場合を含む
- permission profile を一時ファイル、設定ファイル、argv、環境変数、`--config` など、いかなる経路でも Codex CLI に注入してはならない
- oracle file が特定の path に対するアクセス制限を要求する場合も、その制限はプロンプトへ反映し、permission profile や path 単位の sandbox 設定へ変換してはならない
- `{{work-root}}/oracle/src/oracle/prompt_builder/parts/oracle_and_realization_basic.py` にある `git check-ignore` の条件は、oracle file と realization file を分類する境界条件を述べるためだけのものとする
- `git check-ignore` の判定結果をファイル分類や対象ファイルの選別に使用してよいが、Codex CLI の sandbox または permission profile を組み立てる入力にしてはならない

## ファイルアクセス制限違反の事後検証とリカバリ

- agent call が発生させた差分がファイルアクセス制限に違反していないかの事後検証は禁止とする

## Model provider, Model, Reasoning Effort

- Codex CLI に対する Model, Reasoning Effort は、全ての呼び出しで以下の argv により明示的に上書きする
    - Model: `--model`, `{{model-name}}`
    - Reasoning Effort: `--config`, `model_reasoning_effort="{{reasoning-effort}}"`
- `{{model-name}}` は `AgentCallParameter.model_class` を `CmocConfigCodex.model` で解決したモデル名とする
- `{{reasoning-effort}}` は `AgentCallParameter.reasoning_effort` を `CmocConfigCodex.reasoning_effort` で解決した値とする
- `AgentCallParameter.model_class` から解決した `CodexModelSpec.model_provider` が `None` の場合は、model provider に関する argv override を渡さない
- null でない model provider ID は、`{{cmoc-root}}/oracle/doc/app_spec/codex_model_provider.md` に従って Codex CLI 起動前に解決し、解決できなければエラーとする
- null でない model provider ID は、次と同じ形の argv により呼び出し単位で明示的に上書きする
    ```text
    --config 'model_provider={{provider ID の TOML value}}'
    ```
- 選択した provider の `CodexModelProviderConfig.settings` は、各 key/value を次と同じ形の argv により呼び出し単位で明示的に上書きする
    ```text
    --config 'model_providers.{{provider ID の TOML key segment}}.{{provider-local key の TOML key segment}}={{provider-local setting の TOML value}}'
    ```
- model provider ID、provider-local key、および provider-local setting は、意味を変えず Codex CLI が解釈できる TOML key/value として符号化する
- 選択していない provider の設定を argv に渡してはならない
- model provider の選択と provider-local 設定に `--profile`、`$CODEX_HOME/config.toml`、または project config を使用してはならない
- 実経路統合テスト以外の通常実行では、各 AgentCallParameter builder の実行可能部分と docstring が、model class と reasoning effort の正確な選択と選択理由を所有する
- 実際の model provider、model、および reasoning effort の値は `CmocConfigCodex` から解決する
- 実経路統合テストだけに適用する model class と reasoning effort の例外は、`{{cmoc-root}}/oracle/doc/dev_rule/test_rule.md` を正本とする
- この例外によって、通常実行の AgentCallParameter builder の責務を変更してはならない
- cmoc は Model provider, Model, Reasoning Effort 設定についての情報を Codex CLI プロンプトに注入しない

## プロンプトの渡し方

- 初回 Codex call に渡す正確な prompt 文面と構築方法は、`{{cmoc-root}}/oracle/src/oracle/acp_builder` と `{{cmoc-root}}/oracle/src/oracle/prompt_builder` を参照する
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
- cmoc は initial call、Structured Output の correction call、および TUI call の開始前に、invocation-scoped collector へその Codex call の context と capability を登録し、call-scoped な local stdio MCP reporter/client を利用可能にする
- cmoc は call-scoped な Codex CLI `--config` override により、MCP server namespace `cmoc_feedback`、公開 tool `submit_observation`、同 tool の approval behavior、および MCP process に必要な起動情報を設定する
- cmoc は `cmoc_feedback` の effective configuration 全体を呼び出し単位で支配する。user config、`$CODEX_HOME/config.toml`、または project config の server 定義、tool 設定、approval behavior、および起動情報に依存してはならず、それらによって別 tool の公開または reporter の置換を許してはならない
- 通常の `cmoc_feedback.submit_observation` は、human approval、auto-review、または command sandbox escalation を要求せずに実行できるよう設定する
- reporter の起動失敗または reporter・collector の利用不能が、Codex call の開始または本命 workload の成功を妨げないようにする
- capability value を prompt、Codex argv、Codex call log、または submit payload に含めてはならない。MCP process へ capability を安全に渡す具体方式と環境変数名は、この非露出要件を満たす限り実装裁量とする
- Structured Output の correction call は元の agent call ID を共有し、新しい Codex call ID、capability、および MCP context を使用する。初回 prompt で注入済みの reporting instruction を correction schema または correction prompt へ重複させない
- parallel call ごとに capability と MCP context を分離する。一つの call の停止、drain、または capability 無効化によって別 call の受付を変更してはならない
- 一つの TUI process では、全 turn にわたって同じ Codex call ID、capability、および MCP reporter context を維持する
- reporter submission は agent call の正式な Structured Output、作業成果物の差分、および Codex CLI の戻り値とは独立して受理する
- reporter または collector の利用不能は `feedback.reporter_unavailable` event と warning を記録するが、本命 Codex call の開始、終了、Structured Output 検証、retry、および戻り値を変更しない
- Codex call 終了時は、その capability の新規受付を止め、受付済み request を drain し、accepted とする observation の永続化を完了してから、その capability と MCP context を無効化する

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
- 補正 turn の model、reasoning effort、cwd、および Structured Output schema は、元の agent call と整合させる

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

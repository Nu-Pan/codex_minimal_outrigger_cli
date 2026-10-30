# `codex exec` 呼び出し規約

本書は、`codex exec` と `codex exec resume` の非対話 call に適用する。呼び出し単位、環境、設定、prompt の共通原則、MCP 接続、および記録の共通契約は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「Codex CLI 共通呼び出し規約」に従う。

TUI 起動用の初回 exec も本書の対象とする。二段階全体の手順と対話 process の管理は、`{{cmoc-root}}/spec/app_spec/codex_tui_rule.md` の「TUI の新規起動と対話 resume」を正本とし、初回 exec の回復には本書の「TUI 起動用の初回 exec の回復例外」を適用する。

## prompt の保存と stdin 入力

完全 prompt の確定と意味内容を変更しない受け渡しは、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「prompt の構築と受け渡し」に従う。

初期入力のある `AgentCallParameter.prompt` は、初回 Codex call の ID を用いた `{{repo-root}}/.cmoc/gu/log/codex/{{execution-id}}/{{codex-call-id}}_prompt.md` に保存する。TUI 起動用を含む非対話の初回 Codex call では、保存を完了してから、コマンド末尾に `-` を付け、このファイルの同じ本文を stdin へリダイレクト入力する。機械的な処理を行う場合も、保存本文と stdin に渡した本文を一致させる。保存に失敗した場合は call を開始しない。

入力原文の `_orig.md` は、`{{cmoc-root}}/spec/app_spec/prompt_editor_input.md` の「ファイルの役割」に従う入力記録であり、完全 prompt の代わりに stdin へ渡さない。完全 prompt は確定済み入力から構築し、そのために editor input file を再読しない。

Structured Output の補正 prompt は、本書の「同じ session での出力補正」に従い、次の turn の入力として構築する。初回 prompt は加工しない。

feedback reporter の提供が無効な call の補正・再開 prompt に報告規定を追加してはならない。提供判断の維持は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「feedback reporter と collector context」に従う。

## 非対話 call の記録

呼び出し記録の保存先と親の実行・call との対応は、`{{cmoc-root}}/spec/app_spec/codex_common_rule.md` の「Codex CLI 呼び出し情報の保存」に従う。非対話の入出力については、次の規則を加える。

- `{{codex-call-id}}_stdout.jsonl`, `{{codex-call-id}}_stderr.log`, `{{codex-call-id}}_output.json` に残らない情報だけを、同じディレクトリの `{{codex-call-id}}_call.json` に書くこと
- 同一の Codex call について保存する prompt、call、stdout、stderr、output の一式は、同じ `{{execution-id}}` ディレクトリ内で同じ `{{codex-call-id}}` にそろえる
- 初回、補正、retry、回復待ち後の再開、および各 probe の Codex call ごとに、別の Codex call ID と log 一式を作成する
- 停止した呼び出しと probe・再開の対応、および各確認結果は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「診断記録」に従ってサブコマンドログから追跡可能にする

## stdout, stderr の扱い

- `--json` を必ず指定すること
- stdout は `{{repo-root}}/.cmoc/gu/log/codex/{{execution-id}}/{{codex-call-id}}_stdout.jsonl` に出力すること
- stderr は `{{repo-root}}/.cmoc/gu/log/codex/{{execution-id}}/{{codex-call-id}}_stderr.log` に出力すること
- stdout, stderr をコンソールに出力しないこと

## 非対話 call の会話 ID の取得

次の規則は、`codex exec` と `codex exec resume` に適用する。

- Codex call の session ID は、対応する `{{repo-root}}/.cmoc/gu/log/codex/{{execution-id}}/{{codex-call-id}}_stdout.jsonl` から読み取る
- `type == thread.started` である要素の `thread_id` field を session ID とする

    ```json
    {"type":"thread.started","thread_id":"019efe07-4886-7423-b252-625febbe31eb"}
    ```

## `--output-last-message`

- `--output-last-message {{repo-root}}/.cmoc/gu/log/codex/{{execution-id}}/{{codex-call-id}}_output.json` を必ず指定すること
- cmoc が Codex CLI の作業結果を取り出す必要がある場合、その Codex call に対応する `{{codex-call-id}}_output.json` から読み出すこと

## Structured Output

primary report の重要事項確認にも、本節の schema の責務、機械的検証、出力補正、および不受理出力の保持を適用する。正式な全文確認不能の応答を受理した場合の扱いは、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「回復待ちと出力補正」に従う。

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
    - primary report の重要事項確認
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
- 初回 prompt で注入済みの reporting instruction は、correction schema または correction prompt へ重複させない
- 補正 Codex call は初回 Codex call 後に最大 2 回まで行う。したがって、出力生成 turn は初回を含めて最大 3 回とする
- 回復待ち、待機理由の変更、probe の成功、または再開後の再発によって、補正回数の上限をリセットしてはならない
- 出力補正の間隔を開ける必要はない

### 補正 turn の実行条件

- 補正 turn は Structured Output の修正専用とし、作業成果物を変更させてはいけない
- 初回 Codex call 完了時に、agent call の開始前を基準とする作業成果物の差分を固定する
- Codex call ごとの prompt、log、および Structured Output schema の保存物は、本節でいう作業成果物の差分に含めない
- 補正中は、固定した差分を変動させてはいけない。補正 turn が差分を変動させた場合は、初回 Codex call 完了時の状態へ戻し、出力修正だけでは解消できない失敗として扱う
- 補正 turn の cwd と Structured Output schema は、元の agent call と整合させる

### 補正不能時の扱い

以下の「既存のエラー処理」について、primary report の重要事項確認用 call には、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「確認の停止・失敗と保存」「確認結果と終了結果の分離」の例外を適用する。不受理出力の保持と失敗の記録は省略しない。

- 最大 2 回の補正後も検証に合格しない場合は、検証を緩和せず既存のエラー処理へ移る
- prompt、schema、および validator が矛盾している場合は、補正によって矛盾を隠そうとせず既存のエラー処理へ移る
- 作業成果物の差分変動、session の再開不能、またはその他の出力修正だけでは解消できない失敗も、検証を緩和せず既存のエラー処理へ移る
- Structured Output の正式な結果を得られず既存のエラー処理へ移る場合は、`{{cmoc-root}}/spec/app_spec/feedback_observation.md` の「rule registry」が定める `codex.structured_output_validation_exhausted` v1 event を、同仕様の安定 field とともに subcommand log へ記録する

## `codex exec` の並列呼び出し

- fork-join 的な並列化が可能な場合は `codex exec` を並列実行してもよい
- ただし、最大並列数は `CmocConfig.num_parallel` で制限すること

## `codex exec` が失敗した場合

### 基本的な考え方

一時的な利用不能によって、それまでの作業を失ったり、本来の作業を繰り返して浪費したりすることを避ける。cmoc が管理する `codex exec` と `codex exec resume` が quota 枯渇または対象の一時障害で失敗した場合は、呼び出しを保留し、最小限の回復確認 probe で利用可能になるまで待つ。ただし、次の「TUI 起動用の初回 exec の回復例外」を優先し、確認専用 call には「primary report の重要事項確認の回復境界」を適用する。TUI 内部と、その他の外部処理にも、この回復待ちを適用しない。

### TUI 起動用の初回 exec の回復例外

汎用 TUI と oracle 調査 TUI の初回 exec が最終的に失敗した場合は、記録を保存して停止する。途中まで実行した依頼の再送を避けるため、cmoc による prompt の自動再投入を伴う retry・`codex exec resume`、およびそのための回復待ち・probe を適用しない。UUID を取得できても、自動で TUI へ移行しない。

この例外は、次の「最終的な成功と失敗の判断」を変更せず、他の非対話 workload の回復規約にも広げない。

### primary report の重要事項確認の回復境界

確認専用 call にも、本節の失敗分類、最終成功の確認、回復待ち・probe・再開を適用する。確認を終える場合の保存と最外側の終了結果には、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「確認の停止・失敗と保存」「確認結果と終了結果の分離」を適用する。

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

probe の設定取得と、一時障害の確認に必要な設定継承は、`{{cmoc-root}}/spec/app_spec/codex_model_provider.md` の「回復確認 probe の設定例外」を正本とする。

quota availability probe の正確な prompt 文面、prompt part の選択、workload 固有の起動パラメータ、およびその選択理由は、`{{cmoc-root}}/reference/src/oracle/acp_builder/common/quota_probe.py` の `build_quota_availability_probe_request` へ委譲する。回復確認の目的、成功条件、待機・再開の判断は本書が所有し、builder または generated prompt へ委譲しない。

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

- 再開対象の session ID は、本書の「非対話 call の会話 ID の取得」に従って、停止した Codex call の stdout JSONL から取得する。同じ agent call で既に特定できた元の session ID は保持し、後続 call で再取得できないことだけを理由に未取得扱いにしない
- session ID を取得できた場合は、その session を `codex exec resume` で復元し、停止した呼び出しと同じ prompt、同じ設定で実行する
- session ID を取得できない場合は、同じ prompt と設定で再実行する
- session ID があるのに再開できない場合は、新しい session へ自動で切り替えず、失敗として終了処理へ移る。ただし、再開用 CLI 呼び出しの失敗が quota または対象の一時障害なら、再分類して回復待ちへ戻る

Structured Output の補正には、本書の「同じ session での出力補正」と「補正 turn の実行条件」を優先する。補正の session を特定できない場合を、通常の作業呼び出しの再実行で代替してはならない。

再開後も、最終的な成功・失敗の判断と出力検証を省略しない。quota または対象の一時障害が再発した場合は、改めて分類した理由で待機へ戻る。

#### 中断と終了処理

ユーザー中断の対象と優先関係は、`{{cmoc-root}}/spec/app_spec/subcommand_interruption.md` の「対象」と「共通動作」に従う。回復待ちを導入したことだけを根拠に、中断対象外のサブコマンドへ正常中断を追加してはならない。

primary report の確認中の取消は、同文書の「重要事項確認の取消」に従う。これはサブコマンドの本命処理に正常中断を追加するものではない。

待機対象外の失敗または再開不能で続行を断念する場合は、`{{cmoc-root}}/spec/app_spec/error_handling.md` の「エラー分類」と「エラー終了の確定」に従う。ただし、確認専用 call には本書の「primary report の重要事項確認の回復境界」を優先する。終了時の commit、rollback、部分成果、および state の扱いは各 workload の正本を維持し、共通の回復処理で一律に変更しない。特に、`{{cmoc-root}}/spec/app_spec/sub_command/oracle_edit.md` の「終了と差分」に対する自動 rollback を追加してはならない。

#### 表示と記録

待機理由、継続、次回確認、理由変更、復旧後の再開、および待機終了の console 表示は、`{{cmoc-root}}/spec/app_spec/console_and_file_log.md` の「進行通知」に従う。各 probe とその結果、呼び出しとの対応、および待機時間を含む経過は、同仕様の「診断記録」に従う。

### 未確定事項

次の事項は、採用済みの回復待ち方針から区別して未確定のまま残す。

- 一時障害の確認間隔。5 分は暫定候補であり、確定値ではない
- capacity 以外の具体的な診断集合と厳密な対応表。HTTP 503、接続断、応答タイムアウトは追加候補であり、個別診断の採否は未確定とする。対象範囲の境界は「一時障害で失敗した場合」に従う
- probe の設定継承を、一時障害の確認を含まない既存 quota 待機全体にも適用するか。確定済みの例外と理由変更時の適用範囲は、`{{cmoc-root}}/spec/app_spec/codex_model_provider.md` の「回復確認 probe の設定例外」に従う
- 中断対象外サブコマンドの長期待機を終了する操作と、そのときの成果の扱い。正常中断の対象を追加するには個別仕様の変更が必要であり、既存の終了・差分規則は維持する

一方、合意した失敗分類を認識する方法、probe の無応答を判定する具体時間、待機の細かな調整、代表 probe の選定、およびログの具体的な項目・文言は、確定済みの振る舞いを満たす範囲で実装裁量とする。この裁量によって、上記の未確定事項を確定済みの人間判断として扱ってはならない。

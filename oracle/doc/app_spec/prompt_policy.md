
# prompt policy

## 概要

- cmoc が agent call に渡す prompt の責務、情報量、文面管理、および構築規定を定める。
- 本書は、cmoc の意味仕様と agent 向け prompt 文面を別の正本として管理する境界を定める。

## 正本と実行時生成物の責務境界

### 意味仕様の正本

- cmoc の要求、判断基準、および責務を定義する正本は、cmoc 開発者が読む oracle doc とする。
- prompt に含まれない事項を、cmoc の意味仕様に存在しない事項として扱ってはならない。
- prompt、prompt builder、または生成済み prompt だけから cmoc の意味仕様を逆算してはならない。
- agent call に意味上の判断基準を適用する場合は、対応する oracle doc にその基準を定義する。

### prompt 文面の正本

- 子 agent に実際に渡す正確な prompt 文面は、人間が所有してレビューする `{{cmoc-root}}/oracle/src/oracle/prompt_builder` および `{{cmoc-root}}/oracle/src/oracle/acp_builder` の oracle src で管理する。
- prompt builder は、agent 向け文面と起動パラメータの構築定義である。cmoc の意味仕様の唯一の正本ではない。
- oracle doc は意味と責務を定義し、oracle src はその agent call に必要な正確な表現を構築する。oracle doc に prompt 文面をそのまま複製してはならない。

### 実行時生成物

- `AgentCallParameter.prompt`、生成済み完全 prompt、その skeleton、および editor input は実行時生成物であり、正本ではない。
- log に保存された生成済み prompt または editor input を、意味仕様または prompt 文面の編集元として扱ってはならない。

## prompt に含める情報

- prompt は、個別 agent call の遂行に必要な情報を選択して伝える指示とする。正本仕様または cmoc 開発者向け仕様書の代替にしてはならない。
- prompt へ文言を追加する場合は、その agent call の遂行に必要な理由を説明できなければならない。
- agent が参照可能な情報は、必要に応じて参照先または `INDEX.md` routing を示し、本文を網羅的に複製してはならない。
- 子 agent の判断に不要な背景、設計理由、実装事情、および網羅的な仕様説明を含めてはならない。
- 作業に必要な定義、権限制約、作業範囲、完了条件、および出力契約は保持する。
- 単純な短文化または固定の削減率を目的に、必要な情報を削ってはならない。

## prompt 文面の所有と受け渡し

- prompt 文面の執筆と変更は oracle src で行い、realization implementation に独自の文面判断を委ねてはならない。
- `AgentCallParameter.prompt` は、原則として完全 prompt 本文とする。
- realization implementation は、oracle src が構築した prompt 本文の保存、意味を変えない機械的変換、および受け渡しだけを担ってよい。
- realization implementation は、prompt 本文に指示を独自に追加、要約、補完、翻訳、または仕様化してはならない。
- 正本仕様の意味を agent へ伝える場合も、その agent call の遂行に必要な表現だけを oracle src の prompt 文面に置く。

## cmoc 固有契約と installed skill の責務境界

- cmoc の agent call が解釈に必要とする契約の意味は、関連する oracle doc に定義する。各 agent call に必要な表現は、cmoc が所有する oracle src から動的 prompt へ注入する
    - cmoc 固有の概念
    - file access
    - `INDEX.md` routing
    - 出力契約
    - agent call 固有契約
    - cmoc の状態遷移または完了判定が解釈する判断基準
- installed skill は任意の追加規定として利用してよい
- installed skill の有無によって、cmoc の各サブコマンドが agent に要求する意味または判定基準を変えてはいけない
- cmoc 固有契約と installed skill が競合する場合は、cmoc 固有契約を優先する
- 言語、framework、tool、および対象 repository 固有の開発手順を cmoc が網羅することは目的としない
- このため、対象 repository 固有の手順は、repository が追跡する任意の文書、設定、script、または skill から取得してよい
- 対象 repository 固有の手順の配置先を `{{work-root}}/.agents/skills` に限定してはいけない
- Windows toast 通知と prompt または installed skill の責務境界は、`{{cmoc-root}}/oracle/doc/app_spec/windows_toast_notification.md` を正本とする

## 規定を決定論的に注入する

### prompt policy の定義

prompt policy は、cmoc が agent の判断または操作を制約するために選択して注入する instruction の総称とする。構築方法や分類の違いによって別の概念名を設けてはならない。

### policy block と flag の一対一対応

- `build_complete_prompt` の各 policy flag は、対応する 1 個のトップレベル `StructDoc` だけを制御する。
- 対応する policy block は、flag が `True` なら 1 回追加し、`False` なら追加しない。
- ある flag の値を根拠として、別の flag を有効化してはならない。

各 flag が所有する policy block を次に示す。

- `oracle_and_realization_basic`: oracle／realization の分類と基本概念
- `oracle_policy`: oracle authority と oracle file の作成・変更・レビュー規定
- `oracle_investigation_policy`: oracle authority と oracle file の読み取り専用調査規定
- `realization_policy`: oracle authority と realization 規定
- `oracle_review_policy`: finding basis と oracle review 規定
- `apply_review_policy`: oracle authority、finding basis、apply review 規定
- `conflict_resolution_policy`: oracle authority と conflict 解消規定
- `editor_handoff_policy`: editor handoff 規定
- `realization_oracle_reference_policy`: realization code から oracle file path を参照する規定
- `index_entry_policy`: INDEX entry 規定
- `routing_policy`: INDEX routing 規定

### policy の選択と注入

- agent call ごとに必要な全 policy block は、対応する `build_*_parameter` 関数が `build_complete_prompt` の固定引数として明示的に選択する。
- builder による選択は、対応する oracle doc の意味仕様を実現するものであり、選択した prompt part だけを判断基準の正本にしてはならない。
- policy block の結合、重複除去、Policy ID または group ID による衝突検査、および ID による並べ替えを行ってはならない。
- 複数の有効な policy block に同じ文面が含まれる場合は、その文面を各 block 内へ残したまま出力する。
- 各 policy builder は、自身が出力する完全な本文を、その builder 内のリテラルとして直接記述する。
- 共有文面を含む policy 文面を `policy/definitions.py` へ一元定義してはならない。
- 規定の選択に installed skill、設定による任意切替、または追加の agent call を使用してはいけない
- `cmoc tui` は、適用条件を明記した cmoc の基本規定を固定で注入する
- `cmoc tui` のオリジナルプロンプトに応じて規定を選択する agent call を行ってはいけない
- repository の参照が必要な agent call だけに routing policy を注入する。入力された情報だけを参照する agent call には注入しない。
- prompt part の有効化によって、その文面が参照しない cmoc 固有概念を一律に追加してはならない。
- indexing agent call は、対応する index entry instruction を固定で注入する。

共通 prompt part が伝える意味仕様の参照先を次に示す。

- oracle file と realization file の分類、責務、および適合性は、`{{cmoc-root}}/oracle/doc/app_spec/misc_spec.md` とする。
- file access mode と詳細な制限は、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` とする。
- `INDEX.md` の entry と routing は、`{{cmoc-root}}/oracle/doc/app_spec/indexing.md` とする。
- oracle review の所見成立条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/oracle_review.md` とする。
- session join の conflict 解消条件は、`{{cmoc-root}}/oracle/doc/app_spec/sub_command/session_join.md` とする。
- human feedback の報告基準は、`{{cmoc-root}}/oracle/doc/app_spec/feedback_observation.md` とする。

## 人間向け feedback instruction を共通注入する

- 共通 instruction の正確な文面は、`{{cmoc-root}}/oracle/src/oracle/prompt_builder/policy/feedback_reporting.py` の構築定義で管理する。
- `build_complete_prompt` は、同文面を全 agent call へ無条件に 1 回だけ注入する
- 個別の `build_*_parameter` 関数、個別 prompt、または個別 Structured Output schema に同じ reporting instruction を追加してはならない
- feedback field を持たない既存 Structured Output の意味と受理条件を変更してはならない

## Structured Output の出力契約

Structured Output の機械的な受理条件は、schema と宣言済みの決定論的事後条件だけで定義する。

### schema の責務

- 使用可能な JSON Schema で表現できる条件は schema に置く
- schema が定義する条件には、field、型、必須性、列挙値、配列要素数、入れ子、および field 間の構造的な組み合わせを含める
- schema の field description は、field の意味と構造を説明する範囲に留める
- schema で表現できる条件を個別 prompt または決定論的事後条件へ重複させてはいけない

### 決定論的事後条件の責務

- 実行時状態を必要とするため schema で表現できない条件だけを、決定論的事後条件にする
- 実行時状態を必要とする条件には、agent call が実際に変更した path 集合との照合や、入力された ID 集合への参照を含める
- 各決定論的事後条件の意味と機械的な受理基準は、対応する workload の oracle doc に定義する。
- 対応する `build_*_parameter` 関数は、同条件の正確な agent 向け文面を初回 prompt 内の一箇所に置く
- 機械的に検証する各条件は、初回応答前に agent が読み取れる形で宣言する
- validator は oracle doc が定義する条件を実装し、prompt 文面から受理条件を逆算してはならない。
- 同じ agent 向け文面を schema、複数の個別 prompt、または prompt part に重複させてはいけない

### 受理条件の境界

- cmoc は、JSON parse の成否、schema validation、および宣言済みの決定論的事後条件以外の条件で Structured Output を拒否してはいけない
- prompt が要求する意味的な品質は、schema または宣言済みの決定論的事後条件に含まれる場合だけ機械的な受理条件として扱う
- 補正 turn で新しい受理条件を追加してはいけない
- prompt、schema、および validator の矛盾を出力補正の retry で隠してはいけない

## `summary` と `goal` の責務境界

動的な作業記述の責務境界を次のとおり定める。

- `build_complete_prompt` は、agent call 固有の動的な指示として `summary` と `goal` を受け取る。
- `build_complete_prompt` は、独立した `role` を受け取らない。
- `summary` は、agent の担当、主作業、対象、および作業範囲を定義する。
- 担当を明示する必要がある場合は、`summary` の先頭に記載する。
- `goal` は、agent call の終了時に満たされるべき状態を定義する。
- `goal` には、成果物、出力契約、整合性、検証済み状態、および維持すべき非変更状態のうち、完了後に判定できる条件を記載する。
- 「何を、どの対象へ行うか」は `summary` に置く。
- 「完了時に何が成立していなければならないか」は `goal` に置く。
- 同じ要求を `summary` と `goal` の両方へ重複して記載してはならない。
- 作業手順、参照方法、および完了判定ではない禁止事項は、目的に対応する個別の prompt part に置く。
- `cmoc tui` の自由形式オリジナルプロンプトを解析し、`summary` と `goal` へ意味分類する追加の agent call を行ってはならない。

## agent call に渡す prompt を構築する

- agent call の初回入力は、`{{cmoc-root}}/oracle/src/oracle/acp_builder/**/*.py` で定義されている `build_*_parameter` 関数で動的に構築する
- 動的構築された `AgentCallParameter.prompt` は、意味内容を変更せず agent call 側に渡す。realization file 側で加工してはならない
- エディタ入力を使用する agent call は、`{{cmoc-root}}/oracle/doc/app_spec/prompt_editor_input.md` とサブコマンド固有仕様に従い、抽出済みのオリジナルプロンプトから `AgentCallParameter.prompt` を構築する
- Structured Output の補正 prompt には、`{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の出力補正规定を例外として適用する

## 記法

### ベース記法

- プロンプトのベース記法は Markdown とし、採用する Markdown 方言は GitHub Flavored Markdown（GFM）とする
- 以下で定めるプレースホルダとプロンプト上の参照関係は、GFM に加える cmoc 固有の記法とする

### プレースホルダ

- プレースホルダは、`{{repo-root}}` のように名前を二重波括弧で囲って表記する
- root path placeholder の意味は `{{cmoc-root}}/oracle/doc/app_spec/codex_exec_rule.md` の path context に従い、具体的な値は `{{cmoc-root}}/oracle/src/oracle/other/path_model.py` の `AgentCallPathContext` で構築する
- 個別の prompt part は、自身の文面で参照する root path placeholder の定義を、同じ `AgentCallPathContext` から取得して `PlaceholderMap` として返す
- 個別の prompt part は、`{{work-root}}` または `{{repo-root}}` の値を独自に解決してはならない
- 個別の prompt part が path に応じて文面を変える場合は、`build_complete_prompt` と同じ call-scoped path context を明示的に受け取る
- `build_complete_prompt` は、call-scoped path context の root 定義と各 prompt part の `PlaceholderMap` を統合し、最終 prompt では placeholder ごとに 1 個の定義を出力する
- 複数の prompt part が同じ placeholder 名と同じ値を要求する場合は、1 個の定義へ統合する
- 同じ placeholder 名へ異なる値を登録しようとした場合は、後勝ちで上書きせず prompt 構築を失敗させる

### プロンプト上の参照関係

- 参照される対象は、次の XML タグ風の記法で囲う

    ```xml
    <cmoc_block id="target-1">
    ...
    </cmoc_block>
    ```

- 対象への参照は、次の XML タグ風の記法で表す

    ```xml
    <cmoc_ref target="target-1"/>
    ```

- `cmoc_block`、`id`、`cmoc_ref`、`target` は固定の名前とし、`target-1` は参照先を対応付ける可変値とする
- 動的なプロンプト構築では、`cmoc_block` を `StructBlock` で表し、`cmoc_ref` は参照元のプロンプト文字列内に直接記述する
- レンダリング済みの文字列を子にする場合、その文字列は事前のレンダリングで参照関係の検査を完了しているものとし、外側の構造では不透明な内容として再検査しない
- Markdown へのレンダリング時に、各 `cmoc_ref` の参照対象が構築結果内に一つだけ存在することを検査し、参照対象の欠落、`cmoc_block` の `id` 重複、または不正な `cmoc_ref` 記法を検出した場合はプロンプト構築を失敗させる

## 言語

### 原則

- Codex CLI で取り扱う自然言語的な部分は、原則として日本語とする
- e.g.
    - 入力プロンプト
    - 作業レポート
    - レビューレポート
    - INDEX.md の Summary / Read this when / Do not read this when
    - エラーの説明・次に取るべきアクション
    - Codex CLI によるレビュー結果・調査結果の文章部分
    - ...

### 例外

- 個別の仕様に言語指定がある場合はそちらに従う
- 個別の仕様として識別子が規定されている場合はそちらに従う
    - e.g. Structured Output の schema として定義されているキー名
- 元々が英語のワードは、英語のままで良い
    - e.g. コード識別子、ファイルパス、コマンドライン、JSON schema のキー、ログ原文、引用文、…
- LLM 内の思考言語 (e.g. reasoning 時の言語) のように、人間が直接読む想定ではない部分は自由にして良い

# `basic.py`

## Summary
- AIコーディングエージェント呼び出しのパラメータ型と、ファイルアクセスモードなどの呼び出し設定を定義する。
- 呼び出し種別、アクセス制御、初回プロンプト、Structured Output schema、実行時の作業ディレクトリ、MCP handoff と indexing preflight の設定を扱う。
- エージェント呼び出しを構築・実行する実装のうち、基本的なパラメータ表現と設定項目の入口となる。

## Read this when
- エージェント呼び出しの設定項目や、その型・既定値・ファイルアクセスモードを確認したいとき。
- 呼び出しパラメータを生成または受け渡す処理を変更する前に、基本データ構造を確認するとき。
- Structured Output schema の指定、cwd、editor input handoff MCP、indexing preflight の有効化を扱うとき。

## Do not read this when
- 特定の builder がどのような値を組み立てるかだけを確認したい場合は、該当する builder 実装を直接読む。
- ファイルアクセスモードの正本仕様や Codex CLI sandbox との対応を確認したい場合は、参照先の仕様文書を直接読む。
- インデクシングの実行条件・タイミングの意味仕様を確認したい場合は、indexing の正本仕様を直接読む。

## hash
- 543b7fb62130cc282e6ae2c0cb1534f9fa2f7f24016c73d5013bc00d99a04aaa

# `feedback`

## Summary
- feedback issue の同一性判断と remediation に関する agent call の入出力契約、および起動パラメータ定義への入口。

## Read this when
- feedback issue の正規化・同一性判断・remediation agent call の出力形式や起動条件を確認するとき
- 同一性判断用 schema、prompt 構築、remediation の安全な修正・検証条件を横断して確認するとき

## Do not read this when
- feedback observation の受付・送信や候補 issue の収集・絞り込みそのものを確認したいとき
- remediation 対象の realization 実装、oracle file、または同一性判断ロジックの本体を直接確認したいとき
- INDEX.md のルーティング情報だけを確認したいとき

## hash
- 4233d6d48e0e4c6bc63d9fdfbba2e91b914293377ca8a3d4812ec56c032d7723

# `indexing`

## Summary
- 対象ディレクトリは、INDEX.md 用エントリー生成 agent call に関する実装と、その出力形式を定義するスキーマを扱う。
- スキーマ定義は、要約・読む条件・読まなくてよい条件を必須の文字列配列として指定する。
- 実装は、対象パスや完全な読み取り専用 prompt、構造化出力スキーマ、agent の作業ディレクトリ、indexing preflight 設定を組み立てて呼び出しパラメータを返す。

## Read this when
- INDEX.md 用エントリー生成の仕組みを変更・追跡するとき。
- 生成 agent call の prompt 構成、対象パス解決、読み取り専用設定、構造化出力スキーマ、作業ディレクトリ、preflight 設定の関係を確認するとき。
- 生成結果の JSON 構造や必須項目、および指定された出力形式への適合を確認するとき。

## Do not read this when
- 対象ファイルやディレクトリそのものの実際の責務を調べるとき。
- INDEX.md のルーティング内容やエントリー生成用 prompt の規則を確認するとき。
- 一般的な prompt 完成処理や path context の実装だけを確認したいときは、対応する共通実装を直接読む。

## hash
- 4d4c2433d75dca8bbb16c25f34731f6b7bd567719a957176b6c409d81f98ffc8

# `oracle`

## Summary
- `cmoc oracle` 向けの agent 起動パラメータ定義をまとめた正本ソース群。oracle 編集・調査の prompt、ファイルアクセス境界、作業ディレクトリ、入出力引き継ぎ、indexing 実行条件を構築する。
- 編集系は `edit`、調査系は `investigation`、レビュー系は `review` 以下へ進むための入口。

## Read this when
- `cmoc oracle edit` または `cmoc oracle investigation` の agent 起動条件、prompt 構成、oracle 読み書き境界を変更・確認するとき。
- oracle builder の編集・調査・レビュー機能の下位実装へ進む入口を判断するとき。

## Do not read this when
- 個別の編集 prompt 実装だけを確認したい場合は `edit` 以下へ直接進むとき。
- 調査 TUI の起動パラメータだけを確認したい場合は `investigation` 以下へ直接進むとき。
- レビュー処理の具体的な判定・列挙・統合を確認したい場合は `review` 以下へ直接進むとき。

## hash
- 2d228d51b405864438ceed1b72041f4ec08ca667739a6d0da891de160a62f50f

# `quota_probe.py`

## Summary
- Codex CLI の利用可能性を確認する quota availability probe の prompt と agent call パラメータを構築する定義。
- 読み取り専用・短い単発応答・追加調査なしの probe 条件を設定し、再帰的な indexing preflight を無効化する。

## Read this when
- Codex CLI の quota 回復確認用 agent call の prompt、アクセスモード、起動条件を確認または変更するとき。
- quota probe が実行する最小限の確認内容や indexing preflight の扱いを確認するとき。

## Do not read this when
- 通常の quota 管理ロジックや利用量計算を調べるとき。
- 一般的な agent call パラメータや prompt 構築の仕様を確認する場合は、共通の builder 定義を直接読むとき。

## hash
- 1ac746647bce56257d4ec7e41e2b7113802e8e2926f32e10699b404067da3ad6

# `realization`

## Summary
- `apply` は、指定した commit 範囲の oracle file 変更を realization file に追従させる agent call の起動条件・権限・差分判定を確認する入口。
- `refactor` は、refactor fork の commit 差分の要約と、指定 realization file の調査・修正・検証を行う agent call の契約と実行条件を確認する入口。

## Read this when
- oracle file の commit 間変更を realization に反映する agent call の prompt、起動パラメータ、linked worktree、実行前 indexing、差分取得失敗時の扱いを確認するとき。
- refactor fork の差分要約、変更分類、レビュー対象の調査、realization の修正・検証、または各 agent call の出力契約を確認するとき。

## Do not read this when
- 実際の Git 差分取得、fork の実行、realization file の具体的な編集、または個別の変更内容・レビュー結果を調べるとき。
- 共通 prompt 構築、AgentCallParameter の一般仕様、oracle 要求・realization 実装そのもの、または構造化文書レンダリングを直接調査するとき。

## hash
- 31b82bb17ffbff96848c92cef4fdbb63127a7fd62e30023fe68f1a68d6bd01ad

# `session`

## Summary
- session join の merge conflict marker 解消に使うエージェント呼び出し定義。競合対象ファイルの実パス、編集権限、適用するポリシー、indexing preflight の扱いをまとめる。

## Read this when
- session join の競合解消で、対象ファイルの prompt への渡し方や、解消エージェントの実行条件を確認するとき。
- conflict 解消後にも oracle・realization などの規定を適用する呼び出し設定を確認するとき。

## Do not read this when
- 通常の merge 処理や session join 以外のサブコマンドにおけるエージェント呼び出し条件を確認するとき。
- 共通の prompt 構築規則や共通パラメータの定義を確認するとき。

## hash
- 458cbb17539bf5bea207315042fa9cc6c0cfdb291d43cc29b17d06e511cd52cc

# `tui`

## Summary
- `cmoc tui` 用の Codex CLI TUI 起動パラメータを構築する実装。ユーザー入力を完全プロンプトへ組み込み、リポジトリ書き込み権限・エディタ入力引き渡し・事前インデックス処理などの起動設定をまとめる。

## Read this when
- `cmoc tui` の起動パラメータ、プロンプト構築、エディタ入力引き渡し設定を変更・確認するとき
- ACP Builder のTUI起動処理の正本実装への入口を探しているとき

## Do not read this when
- TUI起動後のCLI実行やユーザーインターフェース表示の詳細を調べるとき
- TUIパラメータの利用側やテストの具体的な挙動だけを確認したいとき

## hash
- 935a8554a3ac0eaa0977f1851d84446d2f935386510e75f6f68934c30a0fa572

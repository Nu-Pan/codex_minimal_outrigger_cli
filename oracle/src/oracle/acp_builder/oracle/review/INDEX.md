# `enumerate_finding.json`

## Summary
- 対象スキーマと関連する oracle review 仕様を確認しました。明白な論理矛盾や実装不能な制約は見つかりませんでした。

## Read this when
- oracle review の所見列挙出力を扱うとき。

## Do not read this when
- 所見列挙以外の oracle review 処理を確認するとき。

## hash
- 3c851fade3f048b47c7dec3c065395d99fbadaea6bda723c7ae63ba3b9020225

# `enumerate_finding.py`

## Summary
- oracle review の新規所見列挙用 agent call の prompt と起動パラメータを構築する定義。レビュー対象 oracle file、関連所見、隔離 worktree の文脈を受け取り、完全な prompt と Structured Output schema を設定した AgentCallParameter を返す。
- `build_complete_prompt` にレビューの目的、既知の関連所見、oracle の読み取り・レビュー・ルーティング規則を組み込み、対象パスと oracle ルートを動的に解決する。

## Read this when
- `cmoc oracle review` の新規所見列挙フローで、agent call の prompt 内容や起動条件を確認・変更するとき。
- レビュー対象パス、関連所見、agent call の作業ディレクトリを使った prompt 構築を調べるとき。

## Do not read this when
- 新規所見の出力項目や JSON 形式そのものを確認するだけで、隣接する Structured Output schema を直接読む場合。
- レビュー実行時の所見判定ロジックや oracle file の内容を調べる場合は、対象のレビュー処理・oracle 文書へ直接進む。

## hash
- 048d6d21c64a773ed94fb442fe74f0d8ee2dd37742dde08d0dd5ec1146ac5913

# `judge_finding.json`

## Summary
- 対象は `verdict` と `reason` を必須とする判定結果用 JSON Schema です。

## Read this when
- 対象の判定結果形式を確認するとき。

## Do not read this when
- 判定対象の所見そのものを確認するとき。

## hash
- a024022fc7378f92b7df63be281522661d57e9b773f1d51db649dbcb5b673512

# `judge_finding.py`

## Summary
- このファイルは、`oracle review` における所見採否判定エージェントの呼び出しパラメータを構築する。所見・賛成理由・反対理由をプロンプトへ埋め込み、隔離済み review worktree を起点とした oracle 専用の読み取り条件、モデル設定、推論強度、構造化出力スキーマ、インデックス事前処理を含む `AgentCallParameter` を生成する。

## Read this when
- `oracle review` の所見を人間へ提示すべきか判定する agent call のプロンプトや起動パラメータを変更・確認するとき
- 所見本文と賛成・反対理由を判定用プロンプトへ渡す構築経路を確認するとき
- oracle 専用読み取り、review policy、routing policy、構造化出力スキーマの設定を確認するとき

## Do not read this when
- oracle review の判定結果の出力項目や JSON schema 自体を確認したいときは、同名の構造化出力スキーマを直接読む
- 所見のレビュー規則や仕様断片レビュー全般の判定基準を確認したいときは、この呼び出し構築ファイルではなく対応する oracle policy・review policy の正本を読む
- `AgentCallParameter` やプロンプト共通生成処理の一般仕様だけを確認したいときは、各共通定義を直接読む

## hash
- 4c2440ddf8db99a1d5ab1d1f670592e0cb684c3470a80274b0ff37df57d3e9cf

# `merge_finding.json`

## Summary
- 入力されたレビュー所見の重複や矛盾を整理するための編集操作を定義する JSON Schema。所見の削除・単一所見の置換・複数所見の統合を扱い、各操作で所見の重大度、見出し、根拠となる oracle file、整理理由を表現する。

## Read this when
- レビュー結果の所見リストを重複なく統合・整理する処理の入出力契約を確認するとき。
- 所見の削除、置換、統合に必要な構造や、統合後の所見情報を確認するとき。

## Do not read this when
- 個々のレビュー所見の内容や、所見の根拠となる仕様を確認したいとき。
- レビュー対象の実装や仕様そのものを調査したいとき。

## hash
- 2bc386bc0505b1b36badaa509c55df0cdad5af1e6ebb64dcc8bcb528fee4c1d2

# `merge_finding.py`

## Summary
- oracle review の所見リストを統合する agent call 用の prompt と起動パラメータを構築する。
- 所見本文を動的プロンプトへ埋め込み、重複・矛盾を解消する編集操作を Structured Output で列挙させる。十分に整合している場合は空配列を許容し、finding_id の入力集合に基づく事後条件も prompt に付加する。
- 隔離済み review worktree のパスコンテキスト、PURE_ORACLE_READ、oracle/review/routing 関連ポリシー、効率重視モデル、最大推論、Structured Output schema、indexing preflight などの agent call 設定を一括して返す実装入口である。

## Read this when
- oracle review で複数の所見を統合する agent call の prompt 文面や起動パラメータを確認・変更するとき。
- 所見リストの動的埋め込み、finding_id に関する事後条件、oracle-only のファイルアクセス設定、使用モデルや実行前 indexing の構成を確認するとき。

## Do not read this when
- 所見統合の出力形式そのものを確認する場合は、対応する Structured Output schema を直接読む。
- 一般的な prompt の共通構築規則や SD ノードのレンダリング仕様を確認する場合は、build_complete_prompt や struct_doc の実装・仕様を直接読む。
- oracle review 以外の agent call パラメータや、実際の所見編集処理を調べる場合は、それぞれの対象実装へ直接進む。

## hash
- 945e49e49716b24eb067e6c3a0be2e17c622de2bee69fbf4ddf42f3ac5ef5ae9

# `validate_finding_advocate.json`

## Summary
- 対象 JSON は、レビュー所見の妥当性を支持する新規理由を `reasons` 配列で返すための Structured Output schema を定義する。追加プロパティは禁止され、`reasons` は必須である。

## Read this when
- レビュー所見の妥当性を支持する理由を構造化出力として生成・検証するとき。

## Do not read this when
- レビュー所見の内容や妥当性判定ロジックを確認するとき。出力形式ではなく、関連するプロンプトまたは検証処理を直接読む。

## hash
- e375c55fcdef28f2b23f82065da03126e8885307b7b63ab505cb428574c5c73f

# `validate_finding_advocate.py`

## Summary
- 対象所見の妥当性を擁護するための oracle review 用エージェント呼び出しパラメータを構築する。finding、既知の擁護理由、既知の反証理由をプロンプトへ渡し、重複しない新規理由の列挙を依頼する。oracle review の prompt 生成、起動モデル・推論設定、Structured Output schema、隔離 worktree 起点のパスコンテキストを扱う実装への入口。

## Read this when
- oracle review で、特定の所見が妥当である理由を追加調査する prompt または agent call parameter の構築を確認・変更するとき
- finding と既知の擁護理由・反証理由を入力として、既存理由と重複しない理由を返す呼び出し経路を追うとき

## Do not read this when
- oracle review の反対側の理由列挙や、所見の妥当性判定そのものを確認するとき
- prompt 構築ではなく、共通の Structured Output schema や一般的な agent call 型定義を直接確認すべきとき

## hash
- 6e689110cb624f9411fa415ab7625c78999f0300eb8d648136cc062250970c6c

# `validate_finding_challenger.json`

## Summary
- 対象所見が妥当ではない新規理由は確認できません。

## Read this when
- 対象所見に対する妥当性検証結果の理由を扱う出力形式を確認するとき。

## Do not read this when
- 対象所見の内容そのものや、既知理由の定義を確認するとき。

## hash
- d784259c47bd99b2599523de5d28145bb4bfffd252b7f4d2042a1ed553270c85

# `validate_finding_challenger.py`

## Summary
- oracle review で、対象所見が妥当ではない理由を列挙する agent call の prompt と起動パラメータを構築する。所見、既知の肯定理由、既知の反証理由を prompt に埋め込み、重複しない新規理由または空配列を返すレビュー処理へ接続する。
- PURE_ORACLE_READ、最大推論、EFFICIENCY モデル、Structured Output schema、隔離 review worktree を指定した AgentCallParameter を生成する。oracle review 用の起動設定を確認・変更するときの入口である。

## Read this when
- oracle review の所見反証 agent call に渡す prompt 内容や入力項目を確認・変更するとき
- この agent call のモデル、推論強度、ファイルアクセスモード、schema、起動前 indexing 設定を確認・変更するとき
- finding と既知の advocate/challenger reasons がどのように review prompt に組み込まれるかを確認するとき

## Do not read this when
- レビュー所見そのものの妥当性や反証理由の内容を評価するときは、生成された agent call の対象仕様・レビュー文書を直接読む
- Structured Output の出力項目や JSON schema の定義だけを確認するときは、対応する schema ファイルを直接読む
- oracle review サブコマンド全体のディスパッチや、別種の review finding 用 prompt を調べるときは、それぞれの実装入口を読む

## hash
- 338f702a0ff11820a80d520179e3b57e405e43d4a6c40ed7d73e69296630bb1b

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
- `cmoc oracle review` の新規所見列挙に用いる agent call の prompt と起動パラメータを構築する関数。
- レビュー対象 oracle file と oracle ツリーの解決、関連する既知所見の dynamic input 化、oracle review・所見・routing policy の選択を一つの呼び出し設定にまとめる。
- 同階層の別 review builder ではなく、既知所見との重複を避けながら新規所見を列挙する処理の入口として読む。
- prompt の構成規則自体は `build_complete_prompt`、パスの call-scoped 解決は `AgentCallPathContext` と `resolve_real_path`、出力形式は隣接する Structured Output schema を直接読む。

## Read this when
- oracle review の新規所見列挙 call の prompt、参照範囲、既知所見入力、実行パラメータを確認または変更するとき
- レビュー対象 oracle file の placeholder 解決や agent call の cwd、preflight、model・reasoning 設定の連携を追うとき

## Do not read this when
- 所見の統合、擁護理由列挙、反論理由列挙など別の review 段階を確認したいとき
- 共通 prompt の構成規則を確認する場合は `build_complete_prompt` を、パス解決の一般仕様を確認する場合は `path_model` を直接読むとき
- Structured Output の項目や形式だけを確認したいときは、対応する schema を直接読む

## hash
- 43a8e435812cd28fb87c277cec9b77b8cd65e658fd9169e8c1bda6763c34251c

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
- 対象ファイルは、oracle review における所見採否判定エージェント呼び出しの定義入口です。所見・賛成理由・反対理由を埋め込んだ prompt と、判定用モデル、推論強度、oracle 専用読み取り、構造化出力 schema、preflight などの起動条件をまとめて構築します。
- oracle review の所見判定用 prompt の組み立てや起動パラメータ、またはその呼び出し条件を確認・変更するときに読むべき対象です。

## Read this when
- oracle review で個別所見を人間へ提示すべきか判定する処理を調べるとき
- 所見・賛成理由・反対理由を判定 prompt に渡す方法を変更するとき
- 所見判定エージェントのモデル種別、推論強度、ファイルアクセスモード、構造化出力、indexing preflight の設定を確認するとき

## Do not read this when
- 所見の内容を生成・レビューする処理そのものを調べるとき
- 判定結果の JSON schema の項目や形式だけを確認するときは、同じディレクトリの schema 定義を直接読むとき
- oracle review 全体のサブコマンド構成や、別種の agent call の prompt 構築を調べるとき

## hash
- 796bf460e847f3aaf191aabe74cda8e6d2ccda5f785573f7674c4be18f3630f4

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
- oracle review で収集した所見リストを、重複や矛盾が解消された編集操作へ統合するための AI エージェント呼び出しパラメータを構築する。所見本文を動的プロンプトへ埋め込み、oracle 専用の読み取り制約、レビュー方針、Structured Output schema、効率モデルの最大推論、事前インデックス検査を設定する。

## Read this when
- oracle review の所見マージ処理を変更・調査するとき
- 所見リストを入力として、既存 finding_id を参照する編集操作のプロンプトや起動条件を確認するとき
- oracle review 用 agent call のモデル、推論強度、ファイルアクセス、routing 前処理を確認するとき

## Do not read this when
- 所見の列挙・評価そのものの挙動を確認したいとき
- Structured Output の項目定義や検証規則だけを確認したいとき
- oracle review 以外の agent call パラメータ構築を直接調査するとき

## hash
- a546cd1651b078bf1fb5774431444e80f7a35da923df2b2416afccf8afad8be0

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
- oracle review における所見擁護担当エージェントの呼び出しパラメータを構築する。対象所見と既知の賛成・反対理由を prompt に埋め込み、新規かつ重複しない妥当性の理由を調査させるための設定をまとめる。

## Read this when
- oracle review で、特定の所見が妥当である追加理由を生成する prompt や agent call 設定を確認・変更するとき。
- 所見擁護呼び出しの oracle 専用読み取り範囲、効率モデルの最大推論、Structured Output schema、実行前 indexing preflight の指定を確認するとき。

## Do not read this when
- 所見が妥当でない理由の生成や、レビュー判定そのものを確認するときは、対応する challenger 実装または上位の review 実装を直接読む。
- 出力項目・型・形式だけを確認するときは、この構築定義ではなく隣接する Structured Output schema を直接読む。

## hash
- 1020fff26a412938f66723a9e614460c4af1af5f41c68bace89c87cc7b1942fb

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
- oracle review で個別のレビュー所見に対する「妥当ではない理由」を列挙する agent call パラメータを構築する。
- 所見と既知の賛成・反対理由を動的入力として prompt に組み込み、重複しない新規の反証理由、または理由がない場合の空配列を求める。
- oracle 専用の読み取り制約、レビュー・ルーティング方針、モデルと推論強度、Structured Output schema、実行前 indexing preflight などの起動設定を定義する。

## Read this when
- oracle review の所見について、妥当ではない理由を列挙する agent call の prompt や起動パラメータを確認・変更するとき
- finding と既知理由を入力する反証 prompt の構成や、oracle review 用 agent call の設定を調査するとき

## Do not read this when
- 反証理由の出力項目や JSON 形式だけを確認したいときは、対応する Structured Output schema を直接読む
- oracle review の別段階やレビュー所見そのものの判定ロジックを調べるときは、それぞれの専用実装・定義を直接読む

## hash
- a2139fe799e80b338c640193a14cf65f6793d115e15c3ade5a85aa09f1b1b662

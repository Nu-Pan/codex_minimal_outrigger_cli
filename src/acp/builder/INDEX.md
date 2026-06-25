# `apply`

## Summary
- `cmoc apply fork` の適用・レビュー工程で使う AI 呼び出しパラメータ群と、その入出力に使う構造化スキーマをまとめる領域。ファイル単位の所見列挙、所見リストの整理、所見に基づく realization file 修正、作業後の差分要約という一連のエージェント呼び出し条件を確認する入口になる。
- 各呼び出しでは、対象パスや git diff、所見リスト、個別所見を補助プロンプトに埋め込み、参照する標準、ファイルアクセス権限、モデルクラス、reasoning effort、Structured Output schema の選択を組み立てる。

## Read this when
- `cmoc apply fork` のレビュー・修正・レポート生成で、AI エージェントに渡す role、summary、goal、補助プロンプト、参照標準、ファイルアクセスモードを確認または変更したいとき。
- ファイル単位の所見列挙、集約済み所見リストの改善、個別所見への修正作業、git diff からの変更要約という各段階の呼び出し条件を追いたいとき。
- apply fork の所見一覧や変更要約が、どの Structured Output schema に従い、どの粒度の情報を保持するかを確認したいとき。
- レビュー所見を重複・矛盾・False-Positive の除去を経て作業可能な順序に整理する prompt、または所見本文を修正担当エージェントへ渡す prompt を調整したいとき。

## Do not read this when
- `cmoc apply fork` のサブコマンド登録、CLI 引数解析、branch 作成、git コマンド実行、差分取得などの実行フロー本体を調べたいとき。
- 完全プロンプトの共通組み立て処理、構造化 markdown の描画、path keyword の定義、AgentCallParameter やモデル種別などの共通型定義を変更したいとき。
- oracle file、realization file、各種 standard の本文そのものを確認したいとき。
- 実際の変更対象ファイルの内容、個別の修正コード、またはテスト実装を調べたいとき。

## hash
- e857dc5a93020e28075d60a291c6eed21cd3384dea8bfaed2c216d31657b670f

# `indexing`

## Summary
- 目次エントリー生成に必要な Structured Output schema と、その schema を使って AI 呼び出しパラメータを組み立てる実装を扱う領域。生成結果に含める意味情報の単位、対象本文を根拠にする制約、読み取り専用プロンプト、モデル設定、schema 指定までを確認する入口になる。
- 目次エントリーそのものの内容ではなく、目次エントリーを生成するための入力制約・出力制約・呼び出し設定を追うための実装まとまり。

## Read this when
- 目次エントリー生成で AI に渡す role、summary、goal、補助プロンプト、読み取り専用条件を確認または変更したいとき。
- 目次エントリー生成結果に求める意味情報の構造や必須要素を確認したいとき。
- 対象本文だけを根拠にし、既存の目次を根拠にしないという生成制約を確認したいとき。
- 目次エントリー生成用のモデル設定、reasoning effort、構造化出力 schema の指定、対象パスや対象本文の埋め込み処理を追うとき。

## Do not read this when
- 個別ファイルや個別ディレクトリの目次エントリー文面を確認または作成したいだけのとき。
- 目次探索順、読み進め方、正本仕様断片と実装ファイルの関係など、ルーティング運用全体の規則を確認したいとき。
- 実際の indexing サブコマンドの CLI 引数処理、ファイル走査、目次ファイルの読み書き処理を調べたいとき。
- 共通プロンプト構築、Markdown レンダリング、構造化ドキュメント部品など、目次エントリー生成呼び出しより下位または周辺の処理を詳しく調べたいとき。

## hash
- 3d74f86c0f07eeb37d348cf3ebd89582c24295b63d48819c6db3a347ad83f2dc

# `review`

## Summary
- レビュー系 AI 呼び出しの AgentCallParameter 構築と Structured Output schema をまとめる領域。現状は `cmoc review oracle` の oracle file レビューに特化しており、新規所見列挙、所見の肯定理由・反証理由の列挙、採否判定、所見リスト整理の各段階へ進む入口になる。
- 各段階では、対象 oracle file、対象所見、既知の関連所見、既知の肯定理由・反証理由、現状の所見リストなどを補助文脈として渡し、oracle file 読み取り専用アクセス、モデル種別、推論量、対応 schema を組み合わせた呼び出し設定を構築する。

## Read this when
- `cmoc review oracle` で、oracle file レビューのどの段階にどの AI 呼び出し設定や Structured Output schema を使うか確認したいとき。
- oracle file レビューで、新規所見、所見を妥当とする理由、所見を妥当ではないとする理由、所見の採否、所見リストの重複・矛盾解消操作の出力契約を確認したいとき。
- 対象 oracle file、関連所見、対象所見、既知の肯定理由・反証理由、現状の所見リストが、各レビュー用プロンプトへどう渡されるかを追いたいとき。
- review oracle 用プロンプトで使う役割、目標、oracle 標準・review oracle 標準、ファイルアクセスモード、モデル種別、reasoning effort、schema の対応関係を確認・変更したいとき。

## Do not read this when
- oracle file や realization file の基本概念、正本仕様断片としての一般原則、レビュー基準そのものを確認したいだけのとき。
- `cmoc review oracle` 全体の CLI 引数解析、サブコマンド登録、実行制御、結果の保存・集約・表示処理を調べたいとき。
- 汎用的な AgentCallParameter のデータ構造、共通プロンプト組み立て、構造化 markdown レンダリング、パス解決の実装詳細を調べたいとき。
- oracle file 本文の具体的な仕様内容や、個別の正本仕様断片そのものを読みたいとき。
- oracle file レビュー以外のレビュー処理、または review 以外のサブコマンドの AI 呼び出し設定を調べたいとき。

## hash
- 75efcf37f2080925b304bedbe32ffe2c4d2024d77fa1015d46cbf12e55023a85

# `session`

## Summary
- session 系サブコマンドから起動する AI エージェント呼び出しパラメータを組み立てる領域。現在は、session join で merge conflict marker 解消だけを担当するエージェントへ渡す model、reasoning、file access mode、complete prompt の構成を扱う。
- conflict 対象パスを work root 基準の実パスへ解決し、対象一覧、作業範囲、oracle file の例外的な最小編集許可、git add/commit 禁止などを prompt に埋め込む処理への入口。

## Read this when
- session 系サブコマンドが AI エージェントへ渡す AgentCallParameter の内容を確認または変更したいとき。
- session join の merge conflict marker 解消エージェントに渡る role、summary、goal、補助 prompt、file access mode、model、reasoning effort を確認したいとき。
- conflict 対象ファイル一覧が prompt にどう埋め込まれるか、実パス解決後の表示がどう作られるかを確認したいとき。
- merge conflict marker 解消に限定する指示、仕様改訂禁止、対象外ファイル編集禁止、oracle file の例外的な編集許可、git add/commit 禁止の文言を調整したいとき。

## Do not read this when
- session join の通常実行フロー、merge 実行、conflict marker 検出、join 後処理そのものを調べたいとき。
- complete prompt の共通組み立て、markdown rendering、AgentCallParameter や FileAccessMode などの型定義を調べたいとき。
- real path、work root、パスキーワードの定義、パス解決関数そのものの仕様を確認したいとき。
- merge conflict marker 解消ではない session 系の実行制御、CLI 引数、状態管理、または他サブコマンドの処理を調べたいとき。

## hash
- 9c349137de9dd93d9b9206760be2310b902102e349c94b45d6be693497c0ef57

# `tui`

## Summary
- AI Agent CLI/TUI が作業依頼を実行前に解析し、必要なファイルアクセス権限と参照すべき標準群を判定するための TUI 向け parameter resolve 領域。
- 元プロンプト、利用可能なアクセスモード、oracle・realization・review・ルーティング文書関連の標準断片を組み合わせ、読み取り専用・効率重視・中程度推論 effort・JSON schema 出力で判定させる呼び出し条件を扱う。
- 判定結果側では、選ばれた論理ファイルアクセス権限と、各標準文書を読む必要があるかどうかの理由付けを構造化して返すための期待形を定義する。

## Read this when
- TUI で受け取った作業依頼から、実行前にどの論理ファイルアクセス権限を選ぶべきか判定する処理を調べるとき。
- 作業依頼に対して、oracle・realization・review・ルーティング文書関連の標準を読む必要があるかどうかを構造化して判断する仕様を確認するとき。
- parameter resolve 用のプロンプトに、元プロンプト、アクセスモード一覧、標準仕様断片、出力 schema をどう含めるか確認するとき。
- 権限選択や標準参照要否の理由付けを、実装またはテストで検証するための期待形を確認するとき。

## Do not read this when
- TUI の画面表示、入力編集、イベント処理、対話 UI の挙動を調べたいだけのとき。
- 選定済みパラメータを使った AI Agent CLI/TUI のプロセス起動、実行結果表示、外部コマンド実行を調べたいとき。
- 個別の oracle file や realization file の責務、編集可否、品質基準そのものを確認したいとき。
- ルーティング文書エントリーの書き方や、INDEX.md の判断基準そのものを確認したいだけのとき。
- パス解決、完全 prompt の共通組み立て、基礎データ構造、またはファイルシステム操作の詳細を調べたいとき。

## hash
- a84d3339087bbe0063ec051eda69298c988f97dcac32b663d00328eefcf9ab94

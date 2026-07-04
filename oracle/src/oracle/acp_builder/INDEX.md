# `apply`

## Summary
- `cmoc apply fork` の fork 適用後処理で使う agent call parameter と Structured Output schema のうち、差分要約、実装レビュー所見、所見対応、変更要約に関わる正本仕様断片への入口。
- 変更要約 prompt、ファイル単位の所見列挙 prompt、検出所見を修正 agent に渡す prompt、それらの出力契約の対応関係を確認するための対象。

## Read this when
- `cmoc apply fork` の fork 適用後に、差分要約、実装レビュー所見、所見対応作業をどの agent call parameter と schema で扱うか確認するとき。
- 変更要約や所見列挙の Structured Output schema と、それを使う prompt 側の対応関係を確認したいとき。
- 所見を人間向けレビュー結果として報告し、その後 realization file 修正 agent に渡す流れの正本仕様断片を探すとき。

## Do not read this when
- `cmoc apply fork` の fork 作成、branch 操作、diff 取得、レポート保存、CLI 引数処理など、agent call parameter や出力契約以外の実行制御を調べたいとき。
- apply review standard、oracle standard、realization standard そのものの内容を確認したいとき。
- 共通の prompt builder、path placeholder 解決、markdown rendering、agent call parameter の汎用データ構造の実装を調べたいとき。

## hash
- b920e4220f40ac2f3a067739a1406492d5d59da75e3b0c07b8aa3fb42959711e

# `basic.py`

## Summary
- AI コーディングエージェント呼び出しに渡す基本パラメータの正本断片。論理的なモデルクラス、reasoning effort、ファイルアクセスモード、プロンプト、Structured Output schema、indexing preflight 実行有無、呼び出し時 cwd をまとめる。
- バックエンド固有のモデル名や reasoning effort 名への解決は realization 側の責務であり、ここでは cmoc 上の論理分類と agent call parameter の構造だけを定義する。

## Read this when
- agent call parameter の構造、必須項目、既定値を確認したいとき。
- モデル選択を MAINSTREAM、FLAGSHIP、EFFICIENCY、MINIMUM、LOCAL_SLM の論理分類として扱う根拠を確認したいとき。
- reasoning effort や file access mode を cmoc 上の論理値として扱う箇所を実装・テストするとき。
- indexing preflight を実行するか、または本命 agent call 自身が indexing の場合などにスキップするかを判断する処理を扱うとき。
- agent call の cwd が通常 work root になることを前提にする処理を扱うとき。

## Do not read this when
- バックエンドが実際に受理する具体的なモデル名や reasoning effort 名への変換規則を知りたいとき。
- 各 file access mode の詳細な許可・禁止ルールを確認したいとき。
- agent call の実行手順、外部コマンド起動、結果処理、リカバリ処理そのものを調べたいとき。
- Structured Output schema の中身や schema ファイルの配置規則を確認したいとき。

## hash
- 8937577d3ef4a8dfd56f187c34bf7e2f5cb8a4d365119260d9a62a36f6c8cf56

# `common`

## Summary
- oracle ACP builder の共通部品を定義する oracle src 群への入口。ACP builder の各生成処理で共有される状態、ルール、出力結果の正本仕様断片を扱う。
- 個別の builder 実装ではなく、builder 間で共有される概念や型の仕様を確認するためのまとまり。

## Read this when
- ACP builder 全体で共通して使う状態、ルール、結果表現の正本仕様断片を確認したいとき。
- ACP builder の複数領域にまたがる挙動を実装・テストへ反映する前に、共有概念の境界を確認したいとき。
- 下位要素のどれを読むべきか、共通部品の責務から絞り込みたいとき。

## Do not read this when
- 特定の builder の個別仕様だけを確認したいとき。
- realization code 側の実装詳細やテスト構成を確認したいとき。
- ACP builder と無関係な oracle src の仕様を探しているとき。

## hash
- e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# `indexing`

## Summary
- INDEX.md エントリー生成の出力契約と、`cmoc indexing` がその生成用 AI エージェント呼び出しを組み立てるための正本仕様断片を扱う。
- ルーティング文書作成担当の role、Structured Output schema、対象本文を根拠にする制約、読み取り専用実行、indexing preflight の再帰抑止などを確認する入口となる。

## Read this when
- `cmoc indexing` で INDEX.md 用エントリーを生成する AI 呼び出しの prompt、role、goal、出力 schema、補助文脈を確認または変更したいとき。
- INDEX.md エントリー生成結果が満たすべき JSON 構造や必須項目を確認したいとき。
- 既存 INDEX.md を読まず対象本文を根拠にする制約、ディレクトリ対象で直下目次内容を渡す前提、読み取り専用実行、preflight 再帰抑止の扱いを調べたいとき。

## Do not read this when
- 生成済み INDEX.md エントリーの具体的な内容だけを確認したいとき。
- INDEX.md のルーティング方針やエントリー記述品質基準を確認したいとき。
- 通常の agent call prompt 全体の組み立て規則、パスプレースホルダの意味、cmoc の実装・テスト・CLI 挙動を調べたいとき。

## hash
- 16f370dbf557a597dadee2272baed189fd6082a4d48e83e894e73e8cd6591785

# `review`

## Summary
- `cmoc review oracle` の oracle file レビューで使う agent call parameter と Structured Output schema の正本をまとめる領域。
- 新規所見の抽出、妥当理由・反証理由の収集、人間へ提示する採否判定、重複・矛盾の整理に関する prompt と出力契約を確認する入口。

## Read this when
- `cmoc review oracle` の所見生成、所見検証、採否判定、所見リスト整理に関する agent call parameter や Structured Output schema を確認したいとき。
- oracle file レビューで、既知所見や既知理由と重複しない新規所見・理由だけを返す契約を確認したいとき。
- レビュー所見の妥当理由、反証理由、採否理由、重大度、見出し、根拠 oracle file、整理理由の意味を確認したいとき。
- 複数のレビュー所見を削除・置換・統合・変更不要のどれとして整理するかの出力境界を確認したいとき。

## Do not read this when
- oracle file 全般の品質基準や、仕様断片として何を問題扱いするかの標準を確認したいとき。
- `cmoc review oracle` の CLI 実装、所見保存処理、表示整形、対象ファイル探索など、agent call parameter と応答 schema 以外の実装を確認したいとき。
- realization review や INDEX.md エントリー生成の prompt 正本を確認したいとき。
- prompt 部品の共通組み立て、path placeholder 解決、markdown rendering などの共通実装詳細を確認したいとき。

## hash
- db90413c6b74669c2f28f1de68efd2bf6ce8d8e4b9459915b2f9a25ddf535033

# `session`

## Summary
- `cmoc session join` の merge conflict marker 解消専用の agent call parameter を組み立てる正本実装領域。conflict 対象パス一覧、追加の oracle file 編集許可、prompt、モデル・推論強度・書き込み権限・preflight 抑制の設定へ進む入口。

## Read this when
- session join の conflict marker 解消用 agent 呼び出しで使う prompt、権限、モデル設定を確認したいとき。
- conflict 対象ファイル一覧を prompt に渡す方法を確認したいとき。
- conflict marker 解消時だけ oracle file 編集を許可する境界を確認したいとき。
- merge conflict marker 解消時に indexing preflight を実行しない理由や設定を確認したいとき。

## Do not read this when
- session join 全体の通常処理、merge 実行、run 管理、または conflict 検出の実装を探しているとき。
- prompt builder や agent call parameter 型そのものの一般仕様を確認したいとき。
- conflict marker 解消以外のサブコマンド用 prompt や agent 呼び出し設定を調べたいとき。

## hash
- 05750c849f9c614cc56312609e78a3780670c93bcd688abd8be0ad5c0e7688cf

# `tui`

## Summary
- `cmoc tui` の起動前後で使う AI エージェント呼び出しパラメータの正本仕様断片をまとめる領域。元プロンプトから実行条件を構造化する schema、パラメータ選定用 prompt の構築、TUI 起動時に complete prompt を保存して読ませる呼び出しパラメータ生成を扱う。

## Read this when
- `cmoc tui` でエディタ入力された元プロンプトが、role、summary、goal、file access mode、参照標準フラグ、Structured Output schema を含む実行パラメータ選定用 prompt にどう変換されるか確認したいとき。
- TUI 起動時に complete prompt がどこへ保存され、AI Agent CLI/TUI にその保存先を読ませる指示がどのように組み込まれるか確認したいとき。
- `cmoc tui` 用の AgentCallParameter に設定される model class、reasoning effort、file access mode、JSON 対応ファイル、実行可否フラグの正本値を確認したいとき。
- AI Agent CLI/TUI 向けプロンプト解決結果の JSON 形状、必須項目、許可されるファイルアクセスモード、各 standard を読む要否の判定項目を確認したいとき。

## Do not read this when
- `cmoc tui` 以外のサブコマンドで使う AI エージェント呼び出しパラメータを確認したいとき。
- complete prompt 全体の共通構成規則、各 standard フラグの意味、StructDoc 表現、placeholder 解決の詳細を確認したいときは、prompt builder 側の正本を読む。
- oracle file、realization file、file access mode、パスキーワード、repository root 解決そのものの定義を確認したいときは、それぞれの概念を定義する正本を直接読む。
- INDEX.md 用エントリーの書き方やルーティング文の品質基準だけを確認したいときは、index entry standard を直接読む。

## hash
- 0eb63b2bca7375ee59eaad337aacb96f81b03a7fb30fa4c62b03433a8a53bfec

# `apply`

## Summary
- `cmoc apply fork` 向け agent call parameter と Structured Output schema の正本仕様断片を扱う領域。
- 差分要約、ファイル単位の所見列挙、検出所見への対応に使う prompt、file access profile、モデル設定、出力契約への入口になる。

## Read this when
- `cmoc apply fork` で差分要約、実装レビュー所見の列挙、または所見対応を行う agent call の正本仕様断片を確認したいとき。
- apply fork 系の prompt、role、goal、file access profile、Structured Output schema、モデル種別、reasoning effort の対応関係を調べたいとき。
- fork 適用後の作業レポート、レビュー結果、修正担当 agent への入力形式を固定したいとき。

## Do not read this when
- `cmoc apply fork` の git 操作、branch 操作、fork 作成・適用・分岐制御など、実行フロー本体を確認したいとき。
- 個別ファイルの patch 内容、diff 生成手順、または realization file を実際に修正する実装本体を探しているとき。
- 汎用的な prompt 構築、path placeholder 解決、file access profile の共通実装、または apply fork 以外のサブコマンド用 agent call parameter を確認したいとき。

## hash
- 673f69f4daa00270bbe88bf40b772884405f5d71d7b7862fda45f87ba4efbae3

# `basic.py`

## Summary
- AI コーディングエージェント呼び出しに渡す論理的なパラメータを定義する。モデル選択の意図、reasoning effort、ファイルアクセスプロファイル、プロンプト、Structured Output schema の有無をまとめるための正本仕様断片である。

## Read this when
- agent call の入力パラメータ構造を確認・変更する必要があるとき。
- cmoc 上の論理的なモデルクラスや reasoning effort の意味を確認したいとき。
- バックエンド固有のモデル名へ解決する前段で、呼び出し意図として何を保持するかを判断するとき。
- Structured Output を要求する呼び出しと要求しない呼び出しで、どの情報を持たせるか確認するとき。

## Do not read this when
- バックエンドが実際に受理する具体的なモデル名への変換ロジックを探しているとき。
- ファイルアクセスプロファイルそのものの定義や権限モデルを確認したいとき。
- agent call の実行手順、プロセス起動、結果取得、エラー処理を調べたいとき。
- プロンプト本文の生成規則や Structured Output schema の内容そのものを確認したいとき。

## hash
- e886ae687801796363b54053325a5865afd84537ec3d8afe8b8573e4bbb2fbfa

# `indexing`

## Summary
- INDEX.md エントリー生成に関する oracle src を置くディレクトリ。出力 Structured Output schema と、`cmoc indexing` 用 agent call parameter を組み立てる prompt 正本を扱う。

## Read this when
- INDEX.md 用エントリー生成の出力契約と、`cmoc indexing` が AI へ渡す prompt・schema・対象本文の組み立てを確認したいとき。
- ルーティング文書作成担当向けの出力単位、必須項目、agent call parameter の構築内容を確認したいとき。
- INDEX.md エントリー生成結果を検証する実装やテストで、期待する JSON 構造や呼び出し設定を確認したいとき。

## Do not read this when
- 個別対象について実際にどのような要約や読む条件を書くべきかを判断したいとき。
- INDEX.md のルーティング方針やエントリー記述品質の基準そのものを確認したいとき。
- 一般的な agent call parameter、complete prompt 組み立て、path placeholder、file access profile、cmoc の CLI 挙動を確認したいだけのとき。

## hash
- 720e943787b23230f0e55b2be58f98d22f27a323402acf05f920aaf24ed7f13f

# `review`

## Summary
- `cmoc review oracle` の oracle file レビューで使う agent call parameter と Structured Output schema をフェーズ別に定義する oracle src 領域。
- oracle file からの新規所見列挙、所見の擁護・反証、人間提示可否の判定、重複・矛盾する所見リスト整理に関する正本仕様への入口になる。
- レビュー対象、既知所見・既知理由、file access profile、モデル設定、出力 schema など、レビュー用 AI 呼び出し契約を確認するための下位要素を集めている。

## Read this when
- `cmoc review oracle` の所見列挙、所見検証、採否判定、所見マージに関する agent call parameter や出力 schema を確認したいとき。
- oracle file レビューで、既知所見や既知理由との重複を避けて新規の所見・擁護理由・反証理由を返す仕様を追いたいとき。
- レビュー用 agent に oracle と INDEX だけを読ませ、realization file を読ませないアクセス制御や placeholder の扱いを確認したいとき。
- レビュー所見の重大度、見出し、根拠、理由、採否理由、整理理由を Structured Output 上でどう扱うか確認したいとき。

## Do not read this when
- `cmoc review oracle` 以外のサブコマンドや、oracle file 以外を対象にした review 用 agent call parameter を確認したいとき。
- CLI の実行制御、結果表示、ファイル編集、テスト追加など、レビュー用 AI 呼び出し契約の外側にある realization 側の実装だけを確認したいとき。
- file access profile、path placeholder、complete prompt rendering、AgentCallParameter などの共通部品そのものの仕様を確認したいとき。
- oracle file 全般の品質基準や仕様断片として何を問題扱いするかの標準を確認したいとき。

## hash
- 40782a22ce9c28e94d0a222836bc5d4f7bd07f726a2735a0c019a72a6eb1c8c6

# `session`

## Summary
- session join で merge conflict marker を解消するための agent call 仕様への入口。complete prompt に含める対象パス一覧、作業範囲、ファイルアクセス権限、禁止事項の構成意図を扱う。

## Read this when
- session join の merge conflict marker 解消用 agent call の役割、goal、許可される編集範囲を確認したいとき。
- conflict marker 解消作業で oracle file の編集を例外的に許可する条件を確認したいとき。
- merge conflict 解消用 prompt に渡す対象ファイル一覧や file access profile の構成意図を確認したいとき。

## Do not read this when
- 通常の session join 処理や git 操作全般の実装を確認したいとき。
- merge conflict marker の検出方法や conflicted path の収集処理を確認したいとき。
- complete prompt の共通組み立て仕様、構造化ドキュメント表現、パス解決の詳細を確認したいとき。

## hash
- 2eb2c54bd30fdee8dbc8b8e753a5396411407a27b2051f6974c990c09dae96d3

# `tui`

## Summary
- `cmoc tui` が AI Agent CLI/TUI を起動するための正本仕様断片を扱うディレクトリ。元プロンプトから解決済み実行パラメータを選ぶ処理、TUI 起動時の agent call parameter 構築、対応する JSON Schema をまとめて確認する入口になる。
- TUI の agent call に渡すモデルクラス、推論強度、ファイルアクセスプロファイル、complete prompt、role・summary・goal、oracle・realization・INDEX.md へのアクセス権、各 standard の読解要否を扱う。

## Read this when
- `cmoc tui` の起動時に、ユーザー入力プロンプトから AI Agent CLI/TUI の実行パラメータがどう解決され、agent call parameter へ渡るかを確認したいとき。
- TUI 起動で使う complete prompt、モデルクラス、推論強度、保存先、ファイルアクセスプロファイル、参照すべきプロンプト指示の組み立てを確認したいとき。
- 解決済み実行パラメータの JSON 形状、oracle file・realization file・INDEX.md へのアクセス権、各 standard セクションの読解要否を確認したいとき。

## Do not read this when
- TUI 以外のサブコマンドにおける agent call parameter 構築や実行パラメータ解決を確認したいとき。
- complete prompt の共通部品、AgentCallParameter、ModelClass、ReasoningEffort、PlaceholderMap などの汎用定義そのものを確認したいとき。
- 個別の standard 本文、oracle file・realization file・INDEX.md の定義、ファイルアクセス属性やパスモデルそのものを確認したいとき。

## hash
- 58cf084b043ff80cfd6793e16d9bf8d03e293a11f16a34d6295129717f9fa2e9

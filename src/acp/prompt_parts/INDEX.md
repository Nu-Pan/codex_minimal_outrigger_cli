# `apply_review_standard.py`

## Summary
- oracle file の内容を realization file に適用してレビューする際、何を所見として列挙すべきかを定義する prompt part を構築する。
- oracle file と realization file の明確な不整合、oracle file の仕様断片の隙間の扱い、realization file 単体で明らかな致命的問題を、所見として扱う条件と扱わない条件に分けて規範化する。
- review 適用処理に渡す構造化文書として、所見抽出の判断基準をまとめる入口になる。

## Read this when
- oracle file を realization file に適用するレビューで、どの差分や問題を所見として列挙すべきか確認したいとき。
- oracle file に明記されていない実装差を、仕様不一致として扱うべきか、AI の裁量範囲として許容すべきか判断したいとき。
- realization file だけを見て明らかなバグや致命的問題を、oracle file との不整合がなくても所見に含めるべきか確認したいとき。
- apply review 系の prompt part で、所見列挙の規範文書を生成する処理を調べたいとき。

## Do not read this when
- oracle file や realization file の基本定義そのものを確認したいだけのとき。
- レビュー結果の出力形式、CLI 引数、ファイル入出力、永続状態など、所見列挙の判断基準以外の実装を調べたいとき。
- prompt part の構造化文書変換の共通実装や、Standard・Requirement・StructDoc のデータ構造を調べたいとき。
- 特定の oracle file と realization file の実際の差分内容をレビューしたいだけで、所見として扱う基準はすでに分かっているとき。

## hash
- e133daa45b3519f0636741a148c7a50932c55ddcb2268fd31b894309d8914729

# `complete_prompt.py`

## Summary
- agent call に渡す完全なプロンプトを、基本情報、ファイルアクセス制限、ルーティング規則、任意追加プロンプト、各種標準プロンプト片から組み立てる realization。
- 標準プロンプト片の注入フラグ間の依存関係を補正し、要求された標準に必要な前提情報も含まれるようにしてから、順序付きの構造化文書リストとして返す。

## Read this when
- agent call 用の完全なプロンプト全体に、どの基本セクションや標準セクションが含まれるかを確認・変更したいとき。
- oracle、realization、review、INDEX エントリーなどの標準プロンプトを注入する条件や、フラグ間の依存関係を変更したいとき。
- 補助プロンプトを完全プロンプト内のどの位置へ差し込むか、または基本プロンプトとパターンプロンプトの結合順序を確認したいとき。

## Do not read this when
- 個々の標準プロンプト片の本文内容を確認・変更したいだけのときは、それぞれの構築関数を定義している対象へ直接進む。
- ファイルアクセス制限やルーティング規則そのものの文言・構造を確認・変更したいだけのときは、それぞれの専用構築対象へ直接進む。
- 構造化文書のデータ構造や表現方法を確認・変更したいだけのときは、その型を定義している基盤側へ進む。

## hash
- a75d0bc93639f37242cb338330a8ecfabfac107542c7ddf559d1cb5af09ee098

# `file_access_rule.py`

## Summary
- AI エージェントへ渡すファイル読み書き制約のプロンプト断片を、読み書きモードに応じて構築する実装。作業ルートを解決し、各モードごとに禁止対象となるツリーや例外領域を本文化して構造化文書として返す。
- readonly、oracle のみ参照、実装書き込み、oracle 書き込み、リポジトリ書き込みといったアクセス方針の違いを、プロンプト本文へ反映する責務を持つ。

## Read this when
- AI エージェントへ提示するファイル読み書き規則の文面、見出し、またはモード別の禁止範囲を変更したいとき。
- FileAccessMode の各プリセットが、作業ルート、oracle、.agents、memo に対してどの読み書き制約を出力するか確認したいとき。
- アクセス制約プロンプトを構成する StructDoc の生成箇所や、作業ルート解決結果の埋め込み方を確認したいとき。

## Do not read this when
- 作業ルートなどのパス概念そのものの定義や解決規則を調べたいだけのとき。
- FileAccessMode の列挙値そのものの定義、追加、命名を調べたいとき。
- oracle file と realization file の概念定義や編集責任の一般原則を確認したいだけのとき。
- 生成されたプロンプトを実際にどの会話や実行処理へ組み込むかという上位の組み立てを調べたいとき。

## hash
- db0fc49fb61d10f97527b34036907aed97b5e1937342f90d873ad29113eab551

# `index_entry_standard.py`

## Summary
- `INDEX.md` のエントリーが満たすべき規範を、構造化文書として生成する実装。
- エントリーを、読むべき対象へのルーティング情報として機能させること、対象内容に根拠を持たせること、機械的に補える情報を意味情報へ混ぜないことを扱う。
- 同階層の個別プロンプト部品のうち、エントリー本文そのものではなく、エントリー作成時に従う標準・要求事項を確認する入口になる。

## Read this when
- `INDEX.md` 用エントリーの品質基準、書くべき情報、書いてはいけない情報を確認したいとき。
- エントリー生成プロンプトや標準文書の出力内容を変更し、ルーティング条件・対象責務・読む必要の境界に関する規範を調整したいとき。
- 生成されたエントリーが詳細説明に寄りすぎていないか、対象外の責務を広げていないか、機械的識別情報を混ぜていないかを判断したいとき。

## Do not read this when
- 特定の対象ファイルやディレクトリについて、実際の `INDEX.md` エントリー文面を作成・確認したいだけのとき。
- `INDEX.md` の全体構造、保存場所、更新手順、またはルーティング文書の生成フローを調べたいとき。
- 構造化文書の基礎型、標準・要求事項を文書へ変換する汎用処理、または個別の出力 schema の実装を確認したいとき。

## hash
- 6bd02c846be1c449991613bbb0c157e301247a3eca7dbdd185daee6a8ed291af

# `oracle_and_realization_basic.py`

## Summary
- oracle file と realization file の定義・役割・下位概念を説明する prompt part を構築する。
- oracle を人間所有の正本仕様断片、realization を oracle の人間意図を具体化する AI 編集対象として区別し、doc/src/test/ancillary などの分類も扱う。
- AI が oracle と realization の責務境界、編集主体、生成方向、配置範囲を説明するための基本知識文書を組み立てる入口になる。

## Read this when
- oracle file と realization file の違い、編集責任、正本仕様としての扱いを確認したいとき。
- oracle doc、oracle src、oracle test、realization implementation、realization test、realization ancillary などの下位概念の位置づけを説明する prompt part を調べるとき。
- AI が編集してよい対象と、人間だけが編集する正本仕様断片の境界を prompt に含める処理を確認したいとき。
- oracle から realization が生成されるという方向性や、その逆を禁止する前提を扱う prompt 構築箇所を探すとき。

## Do not read this when
- oracle や realization の基本概念ではなく、個別コマンド、個別ワークフロー、入出力 schema の詳細仕様を調べたいとき。
- StructDoc のデータ構造そのもの、path 解決の実装、または prompt part の合成基盤を調べたいとき。
- oracle file の記述品質基準、realization file の実装品質基準、INDEX.md エントリー作成基準そのものを確認したいとき。
- 特定の oracle file や realization file の本文内容を確認したいとき。

## hash
- 7fb24b76411aa0683093210e417504277f8b3a53b3eae87d572cc33114bb3882

# `oracle_review_standard.py`

## Summary
- `cmoc review oracle` で oracle file をレビューする際に、所見として列挙すべき問題の判定基準を構築する realization implementation。fatal 所見、minor 所見、所見にしてはいけないものの境界を `StructDoc` として返す。
- 正本仕様断片同士の明確な矛盾や、AI の裁量では解消不能な実装不能性を fatal として扱う条件を定義する。
- 日本語上の誤り、誤字脱字、用語不統一、表記揺れ、typo など、正本仕様の内容変更ではなく表記上の単純な問題を minor として扱う条件を定義する。
- oracle file の具体的な記述だけから問題と言い切れない推測、好み、一般的なベストプラクティス、実装方針の複数可能性、自然に補える仕様の隙間を所見にしない境界を定義する。

## Read this when
- `cmoc review oracle` のレビュー所見生成で、fatal と minor の分類基準や、所見対象外にすべき境界を確認したいとき。
- oracle file の矛盾、実装者裁量では解けない仕様問題、単純な表記問題をどの severity として扱うか実装する、または変更するとき。
- oracle file レビューで、仕様の隙間・推測・好み・ベストプラクティスを根拠に所見を作ってよいか判断する制御ロジックを確認したいとき。
- レビュー用プロンプト部品として、所見列挙の規範文章を生成する処理の責務を確認したいとき。

## Do not read this when
- oracle file の一般的な定義、realization file との関係、または正本仕様断片全体の原則を確認したいだけのとき。
- oracle review の出力 schema、CLI 引数、入出力処理、保存処理、実行フローを確認したいとき。
- 通常の code review、テストレビュー、実装品質レビューの基準を探しているとき。
- 特定の oracle file 本文そのものをレビューしたいだけで、レビュー所見の分類基準や対象外条件を変更しないとき。

## hash
- ab3eb5c2538a06817a434195965c0149789258fb6673c9b0d337f1356b2a2246

# `oracle_standard.py`

## Summary
- oracle file が従うべき記述規範を、単一の構造化文書として構築する prompt part。人間の認知負荷削減、正本仕様断片としての扱い、未定義部分の許容、総文字数最小化、矛盾禁止、実装から仕様への逆流禁止、用語統一、命名、oracle 優先、goal/non-goal の境界をまとめて扱う。
- 各規範は背景・要求・判断例を持つ Standard として定義され、oracle file の記述品質や仕様判断の基準を生成する入口になる。

## Read this when
- oracle file の書き方、量、責務境界、正本仕様断片としての扱いに関する prompt 本文を確認したいとき。
- oracle file に何を書くべきか、何を AI 裁量や既存実装・既存テストへ委ねるべきかの判断基準を確認したいとき。
- oracle file 間の矛盾、用語・命名の統一、ベストプラクティスより oracle file を優先する判断、goal/non-goal の書き分けを扱う変更をするとき。

## Do not read this when
- realization file 自体の品質、分割、抽象化、テスト、依存関係、公開面の増減に関する規範だけを確認したいとき。
- 特定の oracle file が述べる個別機能仕様や CLI 挙動の詳細を知りたいとき。
- 構造化文書、Standard、Requirement のデータ構造や変換処理そのものを調べたいとき。

## hash
- 38fa4254d5bced70a5687d3dd439ed3fe9333af980e02dfdf27f38cc7ac692d5

# `realization_standard.py`

## Summary
- realization file の品質基準を StructDoc として組み立てる prompt part。総文字数の最小化、高品質化、コメント、責務分割、既存実装整理、抽象化、公開面、テスト、依存関係、完了時点検までを、相互参照される一つの規範集合として扱う。
- 生成される文書は、実装担当 AI が realization code と test と ancillary を追加・変更・削除するときに、現行仕様に必要な最小構成、責務境界、不要な重複や旧仕様の排除を判断するための基準になる。
- 各 Standard は独立した個別設定ではなく、realization file 全体を小さく保ちながら保守しやすくするための統合された品質規範として読む対象である。

## Read this when
- realization file の実装品質、肥大化抑制、不要実装の削除、責務分割、抽象化、コメント方針、公開面や依存関係の追加可否を判断したいとき。
- 実装・テスト・補助ファイルを追加する前後に、既存実装との重複、旧仕様向け経路、未使用要素、削除・統合余地を確認する基準が必要なとき。
- realization file が大きい、複数責務を含む、または分割すべきか統合すべきかを、文字数だけでなく凝集性や同時に読む文脈から判断したいとき。
- コメントや docstring に、コードから読み取りにくい意図・根拠・不採用方針・対応する oracle file path をどこまで残すべきか判断したいとき。
- 新しい関数・クラス・モジュール・CLI 引数・設定項目・環境変数・出力項目・状態ファイル・外部依存・補助スクリプトを増やす根拠が十分か確認したいとき。
- realization test の追加や整理について、外部挙動や制御ロジックの検証に絞れているか、重複テストや過大な fixture を避けられているか確認したいとき。

## Do not read this when
- oracle file 自体の書き方、正本仕様断片の粒度、人間の認知負荷、未定義部分の扱い、実装から仕様への逆流禁止など、oracle 側の基準を確認したいとき。
- 個別の prompt part がどのように連結されるか、StructDoc 全体のレンダリングや標準変換の仕組みを確認したいだけのとき。
- 特定機能の CLI 挙動、状態ファイル形式、出力 schema、パスモデルなど、cmoc の個別仕様や個別実装の詳細を調べたいとき。
- 対象が生成する品質基準を読むのではなく、基準に従って実際の realization code を修正・実装する具体箇所を探しているときは、その機能を担う実装本文へ進む。
- INDEX.md エントリーの生成規則やルーティング文書の書き方だけを確認したいとき。

## hash
- 95b76e4c75574d6c0dd870cd2bd0dfd1bb385d137af3edd1e8db8ea91f07899d

# `routing_rule.py`

## Summary
- INDEX.md を使って必要な本文へ進むためのルーティング規則を組み立てる prompt part。INDEX.md の位置づけ、読み進め方、読む対象を選ぶ判断基準を、構造化文書として返す。
- 作業対象が推定できる場合は近い階層の案内から読み始め、推定できない場合は作業ルートの案内を起点にする、という探索方針を扱う。

## Read this when
- AI agent が作業前にどの本文を読むべきかを選ぶための規則を確認したいとき。
- INDEX.md を本文の代替ではなく、同階層の対象へ進むための案内として扱う方針を確認したいとき。
- Read this when や Do not read this when を使って読む対象を優先・除外する判断基準を確認したいとき。
- 案内だけで判断できない場合に候補本文を読んで根拠確認する流れを確認したいとき。

## Do not read this when
- 個別の INDEX.md エントリー内容や特定ファイルの要約を知りたいだけのとき。
- 作業ルートの解決方法そのものやパスモデルの詳細を確認したいとき。
- StructDoc の実装、レンダリング、文書構築 API の詳細を調べたいとき。
- oracle file と realization file の関係や編集責務の一般規則を確認したいとき。

## hash
- 06f407d5b0119ff702fe64bdc56d89e93721c2aa5919a2c07a1b0bed90a0bb33

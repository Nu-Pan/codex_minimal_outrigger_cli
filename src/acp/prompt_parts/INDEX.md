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
- agent call に渡す完全なプロンプトを、基本プロンプト、ファイルアクセス規則、ルーティング規則、任意の補助プロンプト、必要に応じて注入する標準プロンプト群から組み立てる realization。
- oracle、realization、review、apply review、index entry などの標準プロンプト指定に応じて、依存する基礎情報も自動的に有効化し、最終的な StructDoc の列として返す。

## Read this when
- agent に渡すプロンプト全体の構成順、必ず含まれる基本要素、任意に追加される標準要素の条件を確認したいとき。
- oracle_standard、realization_standard、review_oracle_standard、apply_review_standard、index_entry_standard の指定が、どの前提プロンプトを連鎖的に含めるかを調べたいとき。
- agent call 用プロンプト生成に、新しい標準プロンプト断片や依存関係のある注入条件を追加・変更したいとき。

## Do not read this when
- 個別の標準プロンプト断片そのものの文面や内容を確認したいだけのとき。
- ファイルアクセス規則やルーティング規則の本文、またはそれらの生成ロジックを確認したいとき。
- StructDoc のデータ構造や文書表現の基礎実装を調べたいとき。

## hash
- a75d0bc93639f37242cb338330a8ecfabfac107542c7ddf559d1cb5af09ee098

# `file_access_rule.py`

## Summary
- AI エージェントに提示するファイル読み書き規則のプロンプト断片を、読み書きモードごとの箇条書き本文として組み立てる実装。
- 作業ルート、正本仕様領域、エージェント設定領域、メモ領域に対する読み書き禁止条件を、指定されたモードに応じて切り替えて構造化文書として返す。
- 無効な読み書きモードが渡された場合は例外を出し、正常時はモード名を含む見出しと本文を持つプロンプト部品を生成する。

## Read this when
- ファイルアクセス制限をAI向けプロンプトにどう表現するかを確認または変更したいとき。
- 読み取り専用、正本仕様読み取り、実装書き込み、正本仕様書き込み、リポジトリ書き込みの各モードで、どの領域を読み書き禁止にするかを確認したいとき。
- ファイルアクセス制限の見出し文言、本文の箇条書き、または読み書きモードと出力内容の対応を変更したいとき。
- 読み書きモードの列挙値を追加・変更した結果、このプロンプト部品側の分岐対応が必要か確認したいとき。

## Do not read this when
- 実際のファイルアクセス制御をOS権限、サンドボックス、CLI実行環境で enforcement する処理を探しているとき。
- 作業ルートやパス別名の定義・解決規則そのものを確認したいとき。
- 読み書きモードの列挙値定義や型の責務を変更したいだけのとき。
- 生成された構造化文書の汎用的な表現形式や整形 helper の実装を確認したいとき。

## hash
- 56135f072e38a0bbdaceaecad937924fbb82d0916d1a45dec37f07cbea3a841d

# `index_entry_standard.py`

## Summary
- 読む対象を選ぶためのエントリーに含めるべき意味情報と、含めてはいけない機械的・過剰な情報の境界を定める規範文章を生成する。
- エントリーは本文の代替ではなく、対象の責務、読む条件、読まなくてよい条件を本文に根拠のある範囲で示すためのものとして位置づける。

## Read this when
- 読む対象を選ぶためのエントリーに、どの程度の説明や条件を書くべきかを確認したいとき。
- エントリーが対象本文の詳細説明になっていないか、対象外の責務まで広げていないかを判断したいとき。
- 機械的に補える識別情報や出力形式の説明を、ルーティング用の意味情報から除外すべきか確認したいとき。

## Do not read this when
- 個別の対象について実際のエントリー文面だけを作る場合で、従うべき規範がすでに分かっているとき。
- エントリー生成の全体手順、入出力制御、ファイル探索、保存処理などの実装を確認したいとき。
- 対象本文そのものの仕様や実装内容を理解したいとき。

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
- `cmoc review oracle` で oracle file をレビューする際に、検出した問題をどの severity の所見として扱うか、または所見にしないかを判定するための規範文章を組み立てる実装。
- fatal 所見、minor 所見、所見対象外の境界を `Standard` と `Requirement` の構造で定義し、レビュー用プロンプト部品として利用できる `StructDoc` を返す。
- 正本仕様断片の矛盾や実装者裁量では解消不能な問題は fatal、表記揺れや typo など単純な表記問題は minor、oracle file の記述だけでは問題と言い切れない推測・好み・一般論は所見にしない、という判断基準を集約している。

## Read this when
- `cmoc review oracle` のレビュー観点、severity 分類、所見を出す条件や出さない条件を確認したいとき。
- oracle file 間の矛盾、実装不能な仕様、typo・表記揺れ・助詞抜けなどをどの種類の所見として扱うかを実装側で調整するとき。
- レビュー用プロンプトに渡す規範文章の構造、タイトル、背景、要求、判断例を変更したいとき。
- oracle file の記述だけを根拠に所見を作るべきか、実装者裁量で自然に補える隙間として扱うべきかの境界を確認したいとき。

## Do not read this when
- oracle file そのものの正本仕様を確認したいとき。この対象は正本仕様ではなく、正本仕様断片を具体化した実装である。
- レビュー結果の出力 schema、保存形式、CLI 引数、サブコマンド処理など、レビュー実行全体の入出力や制御フローを確認したいとき。
- `Standard`、`Requirement`、`StructDoc` のデータ構造や変換処理そのものを確認したいとき。
- oracle file 以外の realization code に対する一般的な品質基準やテスト方針を確認したいとき。

## hash
- ab3eb5c2538a06817a434195965c0149789258fb6673c9b0d337f1356b2a2246

# `oracle_standard.py`

## Summary
- oracle file が従うべき記述規範を StructDoc として構築する prompt part。人間の認知負荷を節約しながら、正本仕様断片としての疎さ、未定義部分の扱い、文字数最小化、矛盾禁止、実装から仕様への逆流禁止、用語・命名の統一、oracle file 優先、goal と non-goal の境界をまとめて扱う。
- 各規範は背景・要求・判断例を持つ Standard 群として定義され、oracle file の記述品質や仕様断片の扱いを AI に判断させるための標準文書へ変換される。

## Read this when
- oracle file の書き方、分量、責務境界、正本仕様断片としての扱いに関する prompt 本文を確認・変更したいとき。
- oracle file と実装の優先関係、未定義部分の許容範囲、既存実装から仕様へ逆流させてよいかどうかの判断基準を確認したいとき。
- oracle file の用語統一、命名、論理矛盾、goal と non-goal の書き分けに関する基準を prompt に含める必要があるとき。
- oracle standard の StructDoc 生成内容や、Standard/Requirement を使った規範文書の構成を確認したいとき。

## Do not read this when
- realization file の品質、分割、抽象化、依存関係、テスト肥大化など、実装側の規範だけを確認したいとき。
- 特定の CLI 挙動、設定、状態ファイル、出力 schema などの個別仕様を探しているとき。
- StructDoc、Standard、Requirement そのもののデータ構造や変換処理の実装を確認したいとき。
- oracle file の本文そのものを編集・確認したいとき。正本仕様断片の内容確認は対応する oracle 側の本文を直接読む。

## hash
- 38fa4254d5bced70a5687d3dd439ed3fe9333af980e02dfdf27f38cc7ac692d5

# `realization_standard.py`

## Summary
- realization file の品質基準を StructDoc として組み立てる prompt part。規模最小化、責務分割、コメント、抽象化、公開面、テスト、依存関係、完了時点検をまたぐ一連の Standard をまとめ、実装担当 AI に realization code を最小で保守しやすく保つための規範集合を渡す。
- 対応する oracle file を根拠にした realization standard 全体の本文生成を担い、各 Standard が相互参照されるため単一の prompt 本文として読む前提になっている。

## Read this when
- realization file や realization test を追加・変更・整理する際に、文字数削減、重複排除、旧仕様削除、責務境界、コメントの要否、抽象化の妥当性、公開面や依存関係の増加抑制を判断したいとき。
- ACP の prompt parts のうち、実装成果物に求める品質基準や完了前チェックを生成する箇所を確認・変更したいとき。
- realization standard の StructDoc に含める要求、背景、判断例の内容や順序を確認したいとき。

## Do not read this when
- oracle file 一般の責務、人間と AI の編集責任、正本仕様断片の扱いを確認したいだけのとき。
- realization standard 以外の prompt part、ACP 通信処理、CLI コマンド、状態管理、または個別機能の実装挙動を調べたいとき。
- Standard や Requirement のデータ構造、StructDoc への変換処理そのものを確認したいとき。

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

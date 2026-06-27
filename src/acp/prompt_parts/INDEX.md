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
- 読むべき対象を選ぶための案内文に求める規範を構築する。対象の責務、読む条件、読まなくてよい境界を、本文内容に根拠を持つ意味情報として書くことを中心に扱う。
- 機械的に補える識別情報や出力形式の説明を避け、同階層の他対象ではなくその対象へ進む理由が分かる案内にするための基準を提供する。

## Read this when
- 読むべきファイルやディレクトリを選ぶための案内文の品質基準を確認したいとき。
- 案内文に、対象の責務、読む条件、読まなくてよい境界をどの程度書くべきか判断したいとき。
- 案内文へ本文詳細、推測した用途、機械的な識別情報を混ぜてよいか迷うとき。

## Do not read this when
- 対象本文そのものの実装仕様や業務仕様を確認したいとき。
- 構造化された出力の項目や型など、出力形式そのものを確認したいとき。
- 案内文ではなく、正本仕様断片や実装ファイル全般の保守方針を確認したいとき。

## hash
- b54587eb91f7806813f5f74538810d9eb38e85afe29266102e7914efd92457a1

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
- oracle file レビューで所見を列挙するときの判定基準を構築する実装。fatal 所見、minor 所見、所見にしない対象の境界を、標準文書として返す役割を持つ。
- oracle file が正本仕様断片であることを前提に、明確な仕様矛盾や実装者裁量では解消不能な問題だけを fatal とし、表記上の単純誤りを minor とし、仕様の隙間や好みだけに基づく指摘を除外するための判断入口になる。

## Read this when
- oracle file レビュー用プロンプトで、どの問題を fatal 所見・minor 所見・対象外として扱うかを確認したいとき。
- 仕様断片同士の矛盾、実装者裁量では解けない問題、typo や表記揺れをレビュー所見として分類する処理を変更するとき。
- oracle file だけを根拠にできない推測、一般的なベストプラクティス、仕様の未定義部分を所見から除外する境界を確認したいとき。

## Do not read this when
- oracle file レビューの出力形式、コマンド実行、入出力データ構造を確認したいだけのとき。
- oracle file そのものの正本仕様や、特定の oracle file の内容を確認したいとき。
- 一般的な realization code の品質基準、テスト方針、ファイル分割方針を確認したいとき。

## hash
- 42b4af4f840656900d48442980fdf6a31093b0c28f75027968f7c1e3ffed6db7

# `oracle_standard.py`

## Summary
- oracle file が従うべき記述規範を、prompt 用の StructDoc として構築する実装。人間の認知負荷削減、正本仕様断片としての扱い、未定義部分の許容、文字数最小化、矛盾禁止、実装から仕様への逆流禁止、用語統一、命名、ベストプラクティスより oracle file 優先、goal と non-goal の境界といった Standard 群をまとめて返す。
- 各規範は背景・要求・判断例を持つ Standard として定義され、oracle file の記述方針を AI に渡すための prompt 本文へ変換される。

## Read this when
- oracle file の書き方、分量、責務境界、正本仕様断片としての扱いを AI prompt にどう含めるか確認したいとき。
- oracle file レビューや生成で、人間が判断すべき事項と AI 裁量で補ってよい事項の境界規範を調べたいとき。
- oracle file の未定義部分、実装差、仕様間矛盾、用語統一、命名、goal/non-goal の扱いに関する prompt part を変更・確認したいとき。
- oracle standard 全体を StructDoc として組み立てる実装や、Standard から StructDoc への変換呼び出しを確認したいとき。

## Do not read this when
- oracle file ではなく realization file の品質、分割、抽象化、テスト、依存関係に関する規範だけを確認したいとき。
- 個別 CLI 機能の仕様、入出力形式、状態ファイルのライフサイクルなど、具体的なプロダクト挙動を調べたいとき。
- Standard、Requirement、StructDoc のデータ構造や変換関数そのものの実装を確認したいとき。
- prompt part を呼び出す側の結合順序、CLI への組み込み、最終 prompt 全体の構成を確認したいとき。

## hash
- 3cb87c0f690a0b702207cfcea1449cf09f9316cde3224a4974090c1664748792

# `realization_standard.py`

## Summary
- realization file の品質基準を StructDoc として構築する prompt part。realization file の最小化、高品質化、コメントと docstring、意味上のまとまり、既存実装整理、抽象化、公開面・状態、テスト、依存関係・補助ファイル・生成物、変更完了時点検に関する Standard 群を 1 つの規範集合として返す。
- 各基準は相互参照される前提で同じ prompt 本文にまとめられており、実装担当 AI に realization code/test/ancillary を肥大化させず、現行仕様に必要な最小構成へ保つ判断基準を渡す入口になる。

## Read this when
- realization file の品質・肥大化抑制・削除統合・責務分割に関する prompt 本文を確認または変更したいとき。
- 実装担当 AI に渡す realization standard の生成内容、Standard の並び、要求レベル、判断例を確認したいとき。
- realization code、test、ancillary の追加時に、重複排除、コメント方針、抽象化、公開面、依存追加、完了時点検をどう指示しているか確認したいとき。
- 16,000 文字を超える単一 prompt part として保持している理由を、責務境界・凝集性・読み取り文脈の観点から確認したいとき。

## Do not read this when
- oracle file の基本原則や oracle standard の正本仕様そのものを確認したいとき。
- 特定の CLI 挙動、状態ファイル、パスモデル、コマンド実装など、プロダクト機能の実装詳細を調べたいとき。
- StructDoc、Standard、Requirement のデータ構造や変換処理そのものを変更したいとき。
- realization standard 以外の prompt part、または prompt 全体の組み立て順序や上位の呼び出し側だけを確認したいとき。

## hash
- 1d5dc5166879d84c847123e9bed648a85433dcac69d0448d4157bd04db2b959d

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

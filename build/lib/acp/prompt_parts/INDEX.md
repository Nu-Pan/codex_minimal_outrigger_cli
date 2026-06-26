# `apply_review_standard.py`

## Summary
- oracle file の正本仕様断片を realization file に適用してレビューする際、どのような差分や問題を所見として扱うかの規範文章を組み立てる。
- 明確な oracle file と realization file の不整合、oracle file にない仕様の隙間だけを根拠にしない判断、realization file 単体で明らかな致命的問題の扱いを定義する。
- Requirement と Standard から StructDoc を生成する prompt parts の一部であり、apply review における所見列挙基準の入口になる。

## Read this when
- oracle file と realization file を照合するレビューで、何を所見として列挙すべきかを確認したいとき。
- oracle file に明記されていない挙動を realization file の問題として扱ってよいか判断したいとき。
- realization file だけを見て明らかなバグや致命的問題を、oracle file との直接不整合がなくても所見に含めるべきか確認したいとき。
- apply review 用の規範文書生成処理や、所見判定基準の文言を変更・検証するとき。

## Do not read this when
- oracle file や realization file の基本定義そのものを確認したいだけのとき。
- StructDoc、Standard、Requirement のデータ構造や変換処理の実装詳細を調べたいとき。
- レビュー結果の出力形式、CLI コマンド、ファイル走査、入出力処理など、所見判定基準以外の apply review 実装を調べたいとき。
- 特定の oracle file と realization file の実際の不整合内容を調査したいとき。

## hash
- 8084bdb3ce48e798cad1515dc50a8d5c7d66c417ec7d2d32494a4d68d6b43799

# `complete_prompt.py`

## Summary
- agent call に渡す完全なプロンプト文書列を組み立てる実装。基本プロンプト、ファイルアクセス規則、ルーティング規則、任意の追加プロンプトを並べ、指定された標準プロンプトの依存関係を補正して必要な標準文書を追加する。
- prompt_parts 配下の個別ビルダー群を統合する入口であり、呼び出し側が role・summary・goal・アクセス制限・補助文書・標準注入フラグを指定して、一貫した StructDoc リストを得るための場所。

## Read this when
- agent に渡す最終的なプロンプト構成、標準プロンプトの注入順序、または注入フラグ間の依存関係を確認・変更したいとき。
- oracle standard、realization standard、review/apply/index entry standard などの標準プロンプトを、どの条件で完全プロンプトに含めるかを追いたいとき。
- ファイルアクセス規則、ルーティング規則、任意追加プロンプトが完全プロンプトのどの位置に入るかを確認したいとき。

## Do not read this when
- 個々の標準プロンプト本文の内容や文言を確認・変更したいだけのとき。その場合は各標準プロンプトを構築する個別ビルダーを直接読む。
- ファイルアクセス規則やルーティング規則そのものの詳細を確認したいだけのとき。その場合はそれぞれの規則を構築する対象を読む。
- StructDoc 型自体の構造や振る舞いを確認したいとき。この対象は StructDoc を利用するだけで、型定義は扱わない。

## hash
- 4ef4cf1eb1c3e35bc79da3ea62130616f441048603de51c70addf5a6c9271d4e

# `file_access_rule.py`

## Summary
- AI エージェントに提示するファイル読み書き規則の文書断片を、読み書きモードのプリセットごとに組み立てる実装。
- 作業ルート、oracle、.agents、memo に対する読み書き可否をモード別の箇条書き本文にし、対応する見出し付き構造文書として返す。

## Read this when
- ファイルアクセスモードごとに、エージェントへ渡される読み書き禁止・許可のプロンプト本文を確認または変更したいとき。
- readonly、pure oracle read、realization write、oracle write、repo write の各モードで、work root、oracle、.agents、memo の扱いがどう分岐するかを調べたいとき。
- ファイルアクセス規則のプロンプト見出しや本文生成が、モード値とどのように対応しているかを確認したいとき。
- 不正なファイルアクセスモードに対するエラー処理の入口を確認したいとき。

## Do not read this when
- 実際の work root 解決規則やパスキーワードの定義を調べたいだけなら、パスモデル側を読む。
- ファイルアクセスモードの列挙値そのものや型定義を変更したいだけなら、アクセスモード定義側を読む。
- 構造文書の表現形式、整形、空白除去の実装を調べたいだけなら、構造文書や整形 helper 側を読む。
- oracle file と realization file の概念定義や所有責任を確認したいだけなら、正本仕様側の該当文書を読む。

## hash
- db8145f4c6d6b7f4b2e797ede7f67ab126aa55eef3f8d85b1d17bf629f233dee

# `index_entry_standard.py`

## Summary
- 読むべき対象を選ぶための案内文が満たすべき規範を、構造化された規範文書として組み立てる実装である。
- 対象の責務は、案内文を本文の代替ではなくルーティング情報として扱うこと、対象内容に根拠を限定すること、機械的に補える識別情報を意味情報へ混ぜないことを規定する入口になる。

## Read this when
- 読むべき対象を判断するための案内文に、どの程度の意味情報を書くべきか確認したいとき。
- 案内文の生成・検証・修正で、読む条件、対象の責務、読まなくてよい境界をどう表現するか確認したいとき。
- 案内文に対象本文の詳細、推測上の責務、機械的な識別情報を含めてよいか判断したいとき。

## Do not read this when
- 案内文の規範ではなく、特定の対象について実際に生成された案内文の内容を確認したいとき。
- 構造化文書を表す基礎データ型や、規範文書への変換処理そのものを調べたいとき。
- 対象本文の仕様や実装詳細を理解したいだけで、案内文の書き方・品質基準を扱わないとき。

## hash
- 9948bdff6712106ea91119db4a9fbd06529bf36046318db4e3adb5863e9c5fb0

# `oracle_and_realization_basic.py`

## Summary
- oracle file と realization file の基本概念を説明するプロンプト部品を構築する実装。
- oracle file の定義、正本仕様断片としての役割、oracle doc・oracle src・oracle test の位置づけを扱う。
- realization file の定義、oracle file を具体化する非正本ファイルとしての役割、実装・テスト・補助ファイルの下位概念を扱う。

## Read this when
- oracle file と realization file の境界、所有者、編集責任、生成方向を確認したいとき。
- oracle doc、oracle src、oracle test、realization implementation、realization test、realization ancillary などの下位概念を区別したいとき。
- 作業対象が正本仕様断片なのか、AI が編集する実現ファイルなのかを判断するための基本説明を確認したいとき。
- プロンプトに含める oracle と realization の基本知識の構成や文言を確認したいとき。

## Do not read this when
- 個別の oracle standard、realization standard、index entry standard の詳細要求を確認したいだけのとき。
- 具体的な CLI 挙動、テスト方針、設定値、パス解決処理など、oracle file と realization file の基本分類以外を調べたいとき。
- oracle や realization の概念説明ではなく、特定機能の実装箇所やテスト箇所へ直接進むべきとき。

## hash
- fe33761da72ba70e8745a65b7ba3562e83c07ac65605f824a71f3fadb8996a03

# `oracle_review_standard.py`

## Summary
- `cmoc review oracle` で oracle file をレビューするときに、所見を列挙する判断基準を構築する実装。
- fatal、minor、所見にしない条件をそれぞれ `Standard` と `Requirement` で定義し、レビュー用の規範文章としてまとめる。
- 正本仕様断片同士の矛盾、実装者の裁量では解消できない問題、表記上の単純誤り、oracle file だけでは問題と言い切れない事項の扱いを確認する入口になる。

## Read this when
- `cmoc review oracle` がどのような問題を fatal 所見として扱うべきか確認したいとき。
- oracle file の誤字、表記揺れ、日本語上の単純な問題を minor 所見として分類する基準を確認したいとき。
- レビュー所見を作る際に、仕様の隙間、推測、好み、一般的なベストプラクティスだけを根拠にしてよいか判断したいとき。
- レビュー用の規範文章がどのような構造化文書として生成されるかを実装側から確認したいとき。

## Do not read this when
- oracle file そのものの正本仕様内容を確認したいときは、対象の oracle file を直接読む。
- レビュー結果の出力形式、CLI 引数、保存先、実行フローを確認したいだけのときは、それらを扱うコマンド実装や仕様を読む。
- 一般的な realization code の品質基準やテスト肥大化の抑制基準を確認したいときは、該当する realization standard を読む。
- 単に構造化文書や `Standard`、`Requirement` の汎用データ構造を確認したいときは、それらの定義元を読む。

## hash
- 1404f2566c5a97fa55822658a9003371e37b786d40ea67b3c81e64c0d013c436

# `oracle_standard.py`

## Summary
- oracle file が従うべき規範文章を StructDoc として構築する実装であり、人間の認知能力の節約、正本仕様断片としての扱い、未定義部分の許容、文字数最小化、矛盾禁止、実装から仕様への逆流禁止、用語・命名の統一、oracle file 優先、goal と non-goal の境界記述を標準化する。
- oracle standard の各項目を Standard と Requirement の集合として定義し、構造化文書へ変換して返す入口になっている。

## Read this when
- oracle file の記述方針、正本仕様断片としての扱い、人間と AI の責任境界を生成されるプロンプト部品上で確認したいとき。
- oracle standard に含まれる規範項目、背景、要求、判断例を実装上どのように StructDoc 化しているか確認したいとき。
- oracle file の過剰記述、未定義部分、論理矛盾、用語・命名、ベストプラクティスとの優先関係に関するプロンプト文面を変更・検証したいとき。

## Do not read this when
- realization file の実装品質、テスト肥大化、依存関係、補助ファイル、公開面の増加抑制に関する標準を確認したいだけのとき。
- oracle file と realization file の定義や配置、正本と具体化物の基本関係だけを確認したいとき。
- StructDoc、Standard、Requirement、または構造化文書への変換処理そのものの汎用実装を調べたいとき。

## hash
- 0a349edcd2226daeb977cfec784977f7ba675274ecc1267c01a68e304d36871a

# `realization_standard.py`

## Summary
- realization file に求める品質基準を StructDoc として組み立てる prompt part。実装・テスト・補助ファイルの肥大化抑制、重複削除、責務境界に沿った分割、抽象化・公開面・依存追加の抑制、変更完了時の整理確認といった、AI が realization code を扱う際の基準群を定義している。
- oracle file ではなく、oracle 側で定義された realization standard を実行時に扱える構造化文書へ変換するための実装であり、各基準は背景・要求・判断例を持つ。

## Read this when
- realization file の最小化、重複排除、旧仕様実装の削除、責務境界による分割・統合に関する prompt part の内容を確認したいとき。
- AI 実装者に渡す realization code の品質基準、コメント・docstring・抽象化・共有 helper の扱い、公開面や永続状態の追加条件を確認したいとき。
- realization test、fixture、外部依存、補助スクリプト、生成物の追加や削除に関する基準が、構造化文書としてどう組み立てられているか確認したいとき。
- realization standard の文言を生成するコード側の定義と、StructDoc への変換呼び出しを確認したいとき。

## Do not read this when
- oracle file の編集方針、正本仕様断片の書き方、人間と AI の責任境界を確認したいだけのとき。
- INDEX.md エントリーそのものの作成基準やルーティング文書の書き方を確認したいとき。
- 個別の CLI コマンド、永続状態操作、パスモデル、Git 操作など、cmoc の具体的なプロダクト挙動を実装している箇所を探しているとき。
- StructDoc、Standard、Requirement、standard_to_struct_doc のデータ構造や変換ロジック自体を確認したいとき。

## hash
- 8863a0f211c617e6e94e9ec938e0d908aa82d4193ae83c3629d3d2e5d5028d50

# `routing_rule.py`

## Summary
- INDEX.md を本文選択のための案内として扱い、作業開始時や下位階層へ進む時にどの階層の INDEX.md を読むか、判断できない場合に本文で根拠確認する流れ、Read this when / Do not read this when による優先判断をまとめたプロンプト断片を構築する。
- 作業対象領域に近い INDEX.md を起点に候補を絞り、対象領域が推定できない場合だけ work root の INDEX.md を起点にする、という読み進め方の規則を扱う。

## Read this when
- エージェントに対して、INDEX.md を使って必要な本文へ進むためのルーティング規則を提示するプロンプト部分を確認・変更したいとき。
- INDEX.md を本文の代替ではなく同階層の対象へ進む案内として扱う、という利用方針の文面を確認したいとき。
- 作業開始時、下位ディレクトリへ進む時、INDEX.md だけでは判断できない時の読み進め方に関する生成文面を確認したいとき。
- Read this when と Do not read this when を使った読む対象の優先・除外判断の説明文を確認したいとき。

## Do not read this when
- 個別の INDEX.md エントリーそのものの生成規則や品質基準を確認したいだけのとき。
- パス概念や work root の解決方法そのものを確認したいとき。
- StructDoc の構造やレンダリング仕様を確認したいとき。
- 実際のファイル探索処理、INDEX.md の読み込み処理、またはルーティング判定の実装ロジックを確認したいとき。

## hash
- d8e006c47095d5110437cb8a851dee23ad97b314657531a3d570f52d146f8443

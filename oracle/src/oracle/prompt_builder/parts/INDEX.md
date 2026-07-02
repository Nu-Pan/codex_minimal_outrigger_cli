# `apply_review_standard.py`

## Summary
- oracle file の内容を realization file に適用する際、レビューで何を所見として列挙するかの規範文章を組み立てる部品。
- oracle file と realization file の明確な不整合、仕様断片の隙間を理由にした過剰な指摘の禁止、realization file 単体で明らかな致命的問題の扱いを定義する。
- 所見の根拠を oracle file の仕様と realization file の実装の対応関係に置きつつ、oracle file に未定義な部分や単なる品質改善提案を所見から外す境界を確認する入口になる。

## Read this when
- oracle file の仕様を realization file に適用するレビューで、どの差分や問題を所見として扱うべきか判断したいとき。
- oracle file に明記されていない挙動を、仕様違反として指摘してよいか迷うとき。
- realization file だけを見るとバグに見える問題を、oracle file との不整合ではない所見として扱えるか確認したいとき。
- レビュー所見に、どの oracle file の仕様とどの realization file の実装が不整合なのかという根拠を求める規範を確認したいとき。
- 一般的なベストプラクティス、実装上の不要要素、旧仕様の残骸をレビュー所見に含める境界を確認したいとき。

## Do not read this when
- oracle file や realization file の基本概念そのもの、所有責任、配置場所を確認したいだけのとき。
- レビュー所見の出力形式、プロンプト全体の組み立て順、placeholder の具体的な差し込み処理を調べたいとき。
- 特定の CLI 機能、状態ファイル、パスモデル、テスト方針など個別仕様の内容を確認したいとき。
- 単なるコード品質改善やリファクタリング方針を調べたいだけで、oracle file 適用レビューの所見判定に関係しないとき。
- INDEX.md エントリーの書き方やルーティング文書の一般規範を確認したいとき。

## hash
- 65d7fa95504cb9bc06a0d024ca7d982b73ca5f845e6611f760e0fa13c4ed7433

# `file_access_rule.py`

## Summary
- AI エージェントへ注入するファイル読み書き規則のプロンプト断片を、アクセスモードごとの deny list として構築する oracle src。
- リポジトリ外、管理領域、AGENTS、INDEX、memo などの共通禁止事項を基礎に、oracle file と realization file の読み書き可否をモード別に切り替える。
- 戻り値として、work-root プレースホルダ値と、モード名を含む構造化ドキュメントを返す。

## Read this when
- ファイルアクセス規則プロンプトの生成内容、禁止対象、またはモード別の oracle file / realization file の扱いを確認・変更したいとき。
- READONLY、PURE_ORACLE_READ、REPO_WRITE、PURE_ORACLE_WRITE、REALIZATION_WRITE、NO_RULE の意味や生成される規則文の差分を確認したいとき。
- アクセス規則文面で work-root プレースホルダをどう解決し、構造化ドキュメントへ渡しているかを確認したいとき。

## Do not read this when
- パス概念そのものの定義や work-root の意味を確認したいだけなら、path model の定義を読む。
- アクセスモードの列挙値や型定義を確認したいだけなら、アクセスモードを定義している基礎モジュールを読む。
- プロンプト断片を結合する全体フローや他のプロンプト部品との関係を確認したい場合は、プロンプト構築側の呼び出し元を読む。

## hash
- b548e5a8e0c45f60ce59f882c2f2b9c0ef11281d931d928566ddd7667b712cfe

# `index_entry_standard.py`

## Summary
- 読む対象を選ぶためのエントリーが満たすべき規範を生成する部品。対象本文を読む前に読むべきか判断できる情報を書くこと、対象内容に根拠を持つこと、機械的に補える識別情報を意味情報へ混ぜないことを定める。
- ルーティング文書の各エントリーに求める責務、読む条件の境界、書いてはいけない過剰な詳細や推測の範囲を確認する入口になる。

## Read this when
- ルーティング文書のエントリー生成やレビューで、何を要約し、何を読ませる条件として書くべきか判断したいとき。
- エントリーが対象本文への案内として適切か、本文の代替説明になっていないかを確認したいとき。
- 対象内容から根拠を持って言える範囲と、推測で広げてはいけない範囲を確認したいとき。
- 機械的に分かる識別情報や出力形式の説明を、エントリーの意味情報に含めてよいか判断したいとき。

## Do not read this when
- ルーティング文書そのものの生成処理、整形処理、ファイル探索処理の実装詳細を調べたいとき。
- 特定の対象本文について、実際にどの要約や読む条件を書くかを判断したいだけで、そのエントリー規範自体を確認する必要がないとき。
- 正本仕様断片全体の基本原則、実装側ファイルの品質基準、テスト方針など、ルーティング文書エントリー以外の規範を確認したいとき。

## hash
- 5f8da15178f7c840797a82586fbfa750e0e43c1dfad56a32a5ec9355f591b037

# `oracle_and_realization_basic.py`

## Summary
- oracle file と realization file の定義、責務境界、下位概念を説明する prompt 部品を構築する。
- 人間が所有する正本仕様断片と、AI が編集する具体化ファイルの違いを扱うため、oracle/realization の基本用語を参照する入口になる。

## Read this when
- oracle file と realization file の違い、所有者、編集責任、生成方向を確認したいとき。
- oracle doc、oracle src、oracle test、realization implementation、realization test、realization ancillary などの下位概念を確認したいとき。
- work tree 内のファイルが oracle 側か realization 側かを分類する条件を確認したいとき。

## Do not read this when
- oracle/realization の分類ではなく、個別の標準や品質要求を確認したいとき。
- path placeholder の解決方法や root path の意味そのものを確認したいとき。
- StructDoc や placeholder map の汎用的な組み立て方だけを確認したいとき。

## hash
- 58452b0f1e52b84af71900f085977504ccad9f29c858d2fd7a8a64d5ed7c58f9

# `oracle_review_standard.py`

## Summary
- `cmoc review oracle` が oracle file をレビューして所見を列挙する際の判定規範を構築する。fatal 所見、minor 所見、所見にしないものの境界を、正本仕様断片同士の矛盾・実装者裁量で解消不能な問題・表記上の単純誤り・oracle file だけでは問題と言い切れない事項に分けて定義する。

## Read this when
- `cmoc review oracle` のレビュー観点として、どの問題を fatal 所見または minor 所見に分類するか確認したいとき。
- oracle file の矛盾、実装者裁量では解消不能な仕様問題、日本語上の誤り、typo、用語の不統一を所見として扱う条件を確認したいとき。
- 仕様の隙間、実装方針の複数性、好み、一般的なベストプラクティスだけを根拠に所見を作ってよいか判断したいとき。

## Do not read this when
- `cmoc review oracle` の CLI 引数、入出力形式、ファイル探索、実行フローなど、所見分類以外の実装詳細を確認したいとき。
- oracle file そのものの一般原則、realization file の実装品質基準、または INDEX.md エントリー生成基準を確認したいだけのとき。
- 特定のレビュー結果の保存形式、表示形式、JSON schema、または他の prompt 部品との結合方法を確認したいとき。

## hash
- a83d32e646c0e234ec9b344c7fa0e9f23db19d26f6f6cd2967c613962abf93c3

# `oracle_standard.py`

## Summary
- oracle file が従うべき基本規範を StructDoc として構築する対象。人間の認知負荷の節約、正本仕様断片としての扱い、未定義部分の許容、文字数最小化、論理矛盾の禁止、実装から仕様への逆流禁止、用語・命名の統一、oracle file 優先、goal/non-goal 境界の記述といった規範群を定義する。
- prompt builder が出力する oracle standard 文書の根拠であり、oracle file の書き方・保守方針・仕様断片としての境界を確認する入口になる。

## Read this when
- oracle file に書くべき内容と AI 裁量に任せてよい内容の境界を確認したいとき。
- oracle file を小さく保つ、重複を避ける、未定義部分を許容する、矛盾を避けるといった規範を確認したいとき。
- oracle file と既存実装・既存テストの関係、特に実装から仕様へ逆流させてよいかを判断したいとき。
- oracle file 内の用語統一、命名、ベストプラクティスより oracle file を優先する判断、goal と non-goal の書き分けを確認したいとき。
- oracle standard の StructDoc 生成内容や、各 Standard/Requirement の構成を変更・確認したいとき。

## Do not read this when
- realization file の実装品質、テスト肥大化、依存追加、公開面増加など、実装側の規範だけを確認したいとき。
- oracle file と realization file の定義や配置上の分類だけを確認したいとき。
- 特定コマンドの入出力仕様や個別機能の正本仕様断片を探しているとき。
- INDEX.md エントリーの生成規範そのものを確認したいとき。
- StructDoc、Standard、Requirement、PlaceholderMap などのデータ構造や変換処理の実装詳細を確認したいとき。

## hash
- 79ba7326ddbddb60db66b8f2f933f29644dbd962fdc5dad23a17e7c3890e1ba2

# `realization_standard.py`

## Summary
- realization file 全般の規範文書を構築する対象。realization file、realization code、realization test、補助ファイルの肥大化抑制、品質、コメント、分割統合、抽象化、公開面、依存、変更完了時の整理確認に関する標準をまとめて扱う。
- 実装担当 AI が現行仕様を満たす最小で保守しやすい realization を作るための判断基準を生成する入口であり、コード追加・テスト追加・依存追加・公開面追加の前後に確認すべき規範を束ねる。

## Read this when
- realization file の総量を減らす方針、重複実装や旧仕様向け実装の削除、不要なテストや補助ファイルの整理について確認したいとき。
- realization code の責務分割、コメントや docstring に残すべき意図・根拠、過度な圧縮や将来用抽象化の禁止条件を確認したいとき。
- realization file の分割・統合判断、8,000 文字や 16,000 文字を超えるファイルの扱い、巨大ファイルを放置しない基準を確認したいとき。
- 新しい関数・クラス・モジュール・共有 helper を追加する前に、既存実装の修正や統合で足りるか、共通化してよい重複かを判断したいとき。
- CLI 引数、サブコマンド、設定、環境変数、出力項目、状態ファイルなどの公開面や永続状態を増やしてよい条件を確認したいとき。
- realization test の追加・整理で、外部挙動や制御ロジックを検証する範囲、重複テストや過大 fixture の抑制を確認したいとき。
- 外部依存、補助スクリプト、テンプレート、生成物、キャッシュ、ログ、一時ファイルを realization として追加・管理してよいか判断したいとき。

## Do not read this when
- oracle file 自体の責務、正本仕様断片の扱い、人間判断と AI 裁量の境界など、oracle 側の一般規範を確認したいだけのとき。
- パスキーワードや oracle file、realization file の基本定義だけを確認したいときは、基本概念を定義する文書を読む方が直接的である。
- 特定の CLI 挙動、出力 schema、状態ファイル形式、個別コマンド仕様など、具体的なプロダクト仕様を探しているとき。
- realization の実装ファイルやテストファイルそのものを修正するために、対象コードの現在構造や既存テストを調べたいだけのとき。
- INDEX.md エントリーの書き方やルーティング文書の規範だけを確認したいとき。

## hash
- 70a575ce2ed7c73343dade21db24a5f3956c5da825f8ee42f4cfa22d2ff5a5ec

# `routing_rule.py`

## Summary
- INDEX.md を本文の代替ではなく読む先を選ぶ案内として扱うための、プロンプト用ルーティング規則を構築する部品。
- 作業開始時に近い階層のルーティング情報から読み進め、判断できない場合だけ候補本文を確認する、という探索順序と判断基準を定義する。

## Read this when
- AI が作業前にどの文章・ファイルへ進むべきかを判断するためのプロンプト規則を確認したいとき。
- INDEX.md の Summary、Read this when、Do not read this when をどのように使って読む先を選ぶかを確認したいとき。
- 対象領域が推定できる場合とできない場合で、どの階層のルーティング情報から読み始めるかを確認したいとき。
- ルーティング情報と本文が食い違う可能性がある場合に、どちらを根拠として扱うかを確認したいとき。

## Do not read this when
- 個別ファイルや個別ディレクトリの具体的なルーティングエントリー内容を確認したいだけのとき。
- パス語彙や work root の解決規則そのものを確認したいとき。
- StructDoc やプレースホルダー展開の汎用的な仕組みを確認したいとき。
- oracle file と realization file の定義や責務分担を確認したいとき。

## hash
- 8f80f160290402887206332cf110cee5e25abf56ea8f64c2e77b4a7ecb246732

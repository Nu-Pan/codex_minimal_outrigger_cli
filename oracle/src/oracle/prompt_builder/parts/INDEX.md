# `apply_review_standard.py`

## Summary
- oracle file に対する realization file の追従要否・所見・修正を判断するための規範コレクションを構築する。共通の oracle 権威・所見根拠に加え、apply review 固有の判断基準をまとめる入口である。

## Read this when
- oracle file と realization file の適合性をレビューするとき
- realization の追従要否、既解決状態、修正対象を判断するための prompt 構築を確認するとき

## Do not read this when
- apply review 以外の規範選択や prompt 部分を確認するとき
- 具体的な規範本文の定義だけを確認したいときは、個別の standard 定義へ直接進む

## hash
- 29e3fc51416862b8771eb3faf6c7138c181338e38bf612c72414a17f96819d2e

# `common_standard.py`

## Summary
- 複数用途で共有する `StandardGroup` の構成定義を提供する。oracle・realization file の扱いに適用する標準グループと、所見・修正対象の判断に適用する標準グループを確認する入口である。

## Read this when
- oracle・realization file を扱う際に、適用する標準グループの構成を確認するとき
- 所見や修正対象を判断する際に、finding basis の標準グループの構成を確認するとき

## Do not read this when
- 個々の標準の具体的な内容を確認するときは、標準定義を直接読む場合
- StandardGroup の一般的な実装や型の仕様を確認するときは、定義元を直接読む場合

## hash
- 41b1cbc3a20e26282638025bf101d011a87a2664216193a374a7aee316ae96cd

# `conflict_resolution_standard.py`

## Summary
- `cmoc session join` の conflict marker 解消時に適用する instruction 文面の構築定義。oracle と realization の意味を保つ conflict 解消規範を、標準グループとして選択・収集する入口。

## Read this when
- `cmoc session join` の conflict 解消用 instruction の構成や適用範囲を確認するとき。
- conflict 解消時に oracle / realization の意味を保持する標準グループの選択を確認するとき。

## Do not read this when
- conflict 解消規範の具体的な内容や、両方の branch を保持する要件を確認するとき。これらは選択される conflict resolution standard の定義へ直接進む。
- `cmoc session join` の conflict 解消以外の instruction 文面や標準構成を確認するとき。

## hash
- f44a82a0edc28e5e359598a4145df3a6c58e68e68bf4e06435d05fdf83089da5

# `feedback_reporting_standard.py`

## Summary
- 全 agent call に共通する、人間向け feedback 報告規範の prompt 部分を構築する。作業外の人間対応で再発防止・浪費削減・意図確定につながる問題だけを報告対象とし、専用 MCP tool による報告後も本来の作業を継続するための標準文面を提供する。

## Read this when
- 全 agent call 共通の feedback 報告ルールや、人間への問題報告用 prompt の生成処理を確認・変更するとき。

## Do not read this when
- 個別 agent call の作業内容や、feedback 保存先の実装を直接確認したいとき。通常の作業内で解決済みの問題や、単なる改善提案を扱うとき。

## hash
- b8637771d4871133e4db01d49c7e6d05f105f213e4d5b819003338d42385066c

# `file_access_rule.py`

## Summary
- agent のファイルアクセスモードに応じた読み書き制限文面を構築する。リポジトリ外、予約領域、oracle/realization file などの禁止規則を共通規則とモード別に組み立て、パス用プレースホルダー定義と構造化文書を返す。
- アクセス規則の生成ロジックや FileAccessMode ごとの制限を確認・変更するときの実装入口であり、実際のファイルアクセス設定や各 oracle/realization file の内容を確認する対象ではない。

## Read this when
- ファイルアクセスモードの追加・変更・検証が必要なとき
- agent 向けの読み書き制限文面、パス境界、oracle/realization file の扱いを調査するとき
- file access rule の戻り値やプレースホルダー定義の生成元を確認するとき

## Do not read this when
- 特定の oracle file や realization file の本文・仕様・実装を調査するとき
- Codex CLI の sandbox 実行規則そのものを確認するときは、対応する正本仕様を読むべきである
- INDEX.md のルーティング情報だけを更新・確認するとき

## hash
- 74be481ba7fd0c5e8a88245c84d926f1893af482cffed83164591005ff59be85

# `index_entry_standard.py`

## Summary
- INDEX.md 用エントリー生成時に適用する規範群を選択する標準コレクションを構築する。
- エントリーのルーティング、本文に基づく根拠、意味情報の扱いに関する標準をまとめ、生成規則を確認する入口となる。

## Read this when
- INDEX.md 用エントリーの生成規則や適用標準を確認するとき。
- エントリー標準の選択範囲を変更するとき。

## Do not read this when
- 個別標準の詳細を確認するときは、各標準定義を直接読む。
- INDEX.md の既存内容を確認するときは、対象の INDEX.md を直接読む。
- エントリー標準の選択と無関係な prompt builder の処理を調べるとき。

## hash
- d23d22e6166934c598bd5203e79e6975c05315d82c2dc118ffc93159f434c7e9

# `oracle_and_realization_basic.py`

## Summary
- 対象ファイルは、oracle と realization の定義・役割・下位分類を、動的な work-root 定義を用いて構築するプロンプト部品です。呼び出し元へは PlaceholderMap と StructDoc の組を返し、oracle/realization の基本説明を組み立てる入口になります。

## Read this when
- oracle と realization の基本概念を説明するプロンプト生成や、その文面・構造を変更または確認するとき。
- AgentCallPathContext からルート定義を取得し、StructDoc とプレースホルダーの組を返す処理を追跡するとき。

## Do not read this when
- 特定の oracle 文書や realization 実装の内容そのものを調べるとき。
- プロンプト部品の選択・組み合わせだけを調べるときは、該当する prompt builder の呼び出し元を直接読む。

## hash
- 3ebaefdba6473a30c6510a47642027979a34061132dd26b4472f8c5c11321d7d

# `oracle_review_standard.py`

## Summary
- oracle review の全段階で共有する所見判定規範を構築する。所見の列挙・統合・検証・採否判定に関する標準群を選択し、所見成立の基礎規範と oracle review 固有の規範をまとめた標準コレクションを返す。

## Read this when
- oracle review における所見判定規範の構成や、共有される標準群を確認・変更するとき。

## Do not read this when
- oracle review の個別標準の具体的な判定内容だけを確認したいときは、各標準定義を直接読む。
- 所見成立の基礎規範だけを確認したいときは、共通標準群の定義を直接読む。

## hash
- 49ce591233470c0d04becdb629013b582be1c30f010782087d89bc9a02626259

# `oracle_standard.py`

## Summary
- oracle file の作成・変更・調査・レビューを扱う agent call に適用する規範の集合を構築する。共通の権限規範と、oracle file 固有の根拠・意図と欠落・逆算禁止・整合性と検索性に関する規範をまとめるため、oracle 向け標準の選択や適用範囲を確認する入口となる。

## Read this when
- oracle file を扱う agent call にどの標準群を適用するか確認または変更するとき
- oracle file 向け instruction の標準構成や適用範囲を調査するとき

## Do not read this when
- 個別の標準規範の本文や詳細な要求を確認したいときは、各 standard 定義を直接読む
- oracle file 以外の agent call に適用する標準構成を確認するとき

## hash
- afb6960336a99a57c832b4edf43e73ca8c05adede1e1d5a940eff12f055f16ad

# `realization_oracle_reference_rule.py`

## Summary
- realization code から参照すべき oracle file path をコメントへ記載する規則を、agent call のパス文脈から構築する関数。placeholder map と構造化文書を返し、realization 実装時の oracle 参照ルールをプロンプトへ組み込む。

## Read this when
- realization code の作成・変更時に、対応する oracle file path をコメントへ記載する規則を確認したいとき。
- agent call の root placeholder 定義と、realization oracle reference rule の構造化文書生成方法を確認したいとき。

## Do not read this when
- realization code の具体的な実装内容やテスト方法を確認したいとき。
- oracle file の仕様本文や、プロンプト構築の別ルールを直接確認したいとき。

## hash
- 79789b9f78302eb267516c71cb34589e6f94c8b1408c4e2b2d5a691b9dbe0124

# `realization_standard.py`

## Summary
- realization file の作成・変更・リファクタ・レビュー時に適用する標準群を選択し、oracle authority standard group と realization standard group を含む StandardCollection を構築する。
- realization standard group には、oracle 適合性、現行仕様限定、リポジトリ検証の三つの規範をまとめる。

## Read this when
- realization file に関する agent call の instruction 文面や適用規範の構成を変更・レビューするとき
- realization file 向けの標準コレクションを構築する責務を確認するとき

## Do not read this when
- 個別の realization standard の内容や適用条件を確認したいとき
- oracle authority standard group の定義を直接確認したいとき
- realization file 自体の実装やテストの内容を確認したいとき

## hash
- 277f72a8edb9f33de8db05bb6bd6fc2f141abc77b016a5835742f214c5f85d76

# `routing_rule.py`

## Summary
- INDEX.md を使った本文へのルーティング規則を構築するプロンプト部品。作業対象に近い INDEX.md から読み始め、Summary・Read this when・Do not read this when で候補を絞り、必要な本文へ進む手順を定義する。下位階層の INDEX.md の利用と、INDEX.md より本文を優先する判断も扱う。

## Read this when
- INDEX.md の読み進め方や、関連する本文を routing 情報で絞る仕組みを確認するとき。
- プロンプトへ埋め込む routing rule の内容や、work-root の参照方法を変更するとき。

## Do not read this when
- 特定の INDEX.md の既存エントリーや本文を確認したいとき。
- routing 以外のプロンプト部品の生成規則を確認したいとき。

## hash
- 2ebd20e0c920860904622c216abda854150d36a13101df2052f3da03e5389295

# `standard_definitions.py`

## Summary
- 全用途で共有する Standard 定義の正本を集約し、oracle、realization、finding、review、conflict resolution、INDEX エントリーに関する要求・禁止事項を標準識別子付きで提供する。複数の prompt や検証処理が共通の標準文面を参照する際の入口となる。

## Read this when
- 共有 Standard の文面、標準識別子、要求・禁止事項を追加・変更・確認するとき
- 複数の作業領域にまたがる標準要求の優先関係や適用範囲を確認するとき
- prompt 生成や検証処理が利用する標準定義の全体像を確認するとき

## Do not read this when
- 特定の oracle file、realization file、test、または INDEX.md の具体的な内容だけを確認するときは、対象本文を直接読む
- Standard の実装クラスや個別の prompt 組み立て処理だけを調査し、共有標準文面の意味を確認する必要がないとき
- リポジトリ固有の実行手順や実装挙動を確認するときは、対応する手順書・realization file・test を読む

## hash
- 1396aa69a38eda5f350b17d0120d4c4c3f32719bcbcfd6c341dc84be02fdf575

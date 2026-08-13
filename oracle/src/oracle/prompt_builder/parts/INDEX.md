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
- 複数用途で共有する StandardGroup の構成定義をまとめる。
- oracle・realization file を扱う時の oracle authority 標準群と、所見・修正対象の判断時に用いる finding basis 標準群を構成するエントリーである。

## Read this when
- oracle・realization file を扱う際に、適用する oracle authority 標準群の構成を確認したいとき。
- 所見・修正対象の判断時に、適用する finding basis 標準群の構成を確認したいとき。
- oracle authority 標準群について、基本標準のみの構成と、oracle authority no reverse flow 標準を追加した構成の違いを確認したいとき。

## Do not read this when
- StandardGroup の個別標準の本文や詳細な判定基準を確認したいとき。
- 標準そのものの定義を確認したいときは、参照されている standard_definitions の対象へ直接進む。

## hash
- a65023fc8999435be18fdde6c8828d78e926bbb047de44a0cad74de7e7e78460

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
- 全 agent call に共通する、人間向け feedback 報告の判定基準と報告手順を構築する。現在の作業外の人間対応で再発防止・反復的浪費の削減・人間意図の確定が可能な問題を MCP feedback tool へ報告するための共通入口である。

## Read this when
- agent call 共通の human feedback 報告ルールを変更・確認するとき
- feedback を報告すべき問題の範囲や、報告後の継続方針を確認するとき

## Do not read this when
- 個別の prompt builder 部品や、feedback 内容そのものの保存形式だけを調べるとき
- 通常の workload 内で解決済みの問題や、根拠のない改善案を扱うとき

## hash
- bd6497bee29a5aa1d0f35d0423869b24d79127d4e61d1ea8097504d0e1ffa08b

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
- oracle と realization の分類境界、および両者の役割を定義する基本説明文を構築する。
- oracle 側では oracle doc・oracle src・oracle test、realization 側では realization code・implementation・test・ancillary の下位概念を整理する。
- call-scoped context から work-root の定義を取得し、説明文中のプレースホルダーへ渡す処理を含む。

## Read this when
- oracle file と realization file の分類規則や責務を確認するとき。
- oracle doc/src/test と realization implementation/test/ancillary の区分を確認するとき。
- oracle と realization に関する基本説明文の生成経路を変更・調査するとき。

## Do not read this when
- oracle と realization の分類や基本概念を扱わず、別の prompt_builder part を直接確認すべきとき。
- 具体的な分類アルゴリズムやテスト実装を確認する場合に、対応する実装・テスト対象へ直接進めるとき。

## hash
- 7d70bb60c470aff3275d9de18ec27d6b68d9da9fab51e7cf7a7608aa58964008

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
- oracle file を扱う agent call 向けの instruction 文面を構築する標準コレクションを提供する。
- 作成・変更・レビュー用には権威性、編集根拠、意図と空白、逆算推論禁止、実装制約、一貫性と検索可能性に関する規範を選択する。
- 読み取り専用調査用には、権威性、逆算推論禁止、定義済み事項と未定義事項に関する規範だけを選択する。
- 各標準コレクションはキャッシュされ、共通の authority standard group または authority core standard group と用途別グループを組み合わせて返される。

## Read this when
- oracle file の作成・変更・レビューに適用する標準コレクションの構成や選択範囲を確認するとき
- oracle file の読み取り専用調査に適用する標準コレクションの構成や選択範囲を確認するとき
- oracle file 向け agent call の instruction 文面で、作業用途に応じた標準グループの選択を追跡するとき

## Do not read this when
- 個別の oracle 規範本文を確認したいときは、ここではなく各標準定義の対象を直接読むべきである
- StandardCollection や StandardGroup の一般的な構造・実装を確認したいときは、ここではなくそれらの定義元を直接読むべきである
- oracle file の具体的な作成・変更・レビュー手順そのものを確認したいときは、ここではなく該当する規範または手順の対象を読むべきである

## hash
- 68f044ddde2f93779e774f515c2348ef0b2e7018cde02032fe3ffec24e698b19

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
- 標準文面をコード上の定義として一元管理し、oracle の権威性・仕様調査、realization の適合、レビュー、conflict 解消、INDEX エントリー作成など、cmoc の判断規則を共有する入口。個別の標準内容を確認・変更する作業ではこの定義を読む。

## Read this when
- oracle file と realization file の優先関係、正本仕様からの逸脱防止、未定義事項の扱いを確認するとき
- realization の実装・テスト・設定を現行仕様へ適合させる方針を確認するとき
- oracle review、修正対象の選定、conflict marker 解消、INDEX.md エントリー生成の判定基準を確認するとき

## Do not read this when
- 特定の oracle file の具体的な仕様だけを確認する場合
- 対象の実装挙動やテスト手順を直接確認する場合
- 標準定義や、それが定める判断・レビュー基準を変更しない通常の作業

## hash
- 783ad1286864e56c69ef0557a9544f0acedadab8ff8cda12dabe779da6ab4197

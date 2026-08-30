# `basic.py`

## Summary
- プロンプト生成で共通利用するプレースホルダ対応表の型 `PlaceholderMap` を定義する標準モジュール。プレースホルダ名から置換先の文字列またはパスを対応付けるための入口であり、具体的なプロンプト構築処理を確認する対象ではない。

## Read this when
- プレースホルダの対応関係を表すデータ構造の型定義や、文字列・`Path` を含む置換値の仕様を確認したいとき。
- プロンプト関連コードで共通の型エイリアスの定義元を特定したいとき。

## Do not read this when
- プロンプトの生成手順、テンプレート展開、置換処理の実装を調べるときは、実際のプロンプト構築モジュールを直接読む。
- プレースホルダ対応表の型定義に関係しないプロンプト仕様やCLI挙動を確認するとき。

## hash
- 526fb2d3d3f5fd312f3f1cc48c630d59e91568f38d6ac0d09bc5241792eb1e18

# `complete_prompt.py`

## Summary
- agent 向け完全 prompt の構築を担当する定義。基礎規定、選択式の各種 policy、caller 指定の目的・追加文面、placeholder 定義を所定の順序で統合し、構造化された prompt として返す。

## Read this when
- agent call に渡す完全 prompt の構成順序や、各 policy の有効化、placeholder 定義の統合規則を変更・確認するとき。
- prompt builder の caller 指定文面と基礎規定・目的・動的情報の結合方法を確認するとき。

## Do not read this when
- 個別 policy の本文や、oracle・realization・file access など単一の規定の内容だけを確認したいとき。
- prompt の利用側や、構造化文書の一般的な表現形式だけを変更・確認するとき。

## hash
- 99b849f5be5a81f6ca755b30623e449e7694532c5899c9a63b31f8ba77744780

# `editor_input.py`

## Summary
- ユーザー入力用エディタに注入する初期テキストを構築する関数を定義する。使い方・記入の目安と、完全プロンプトのテンプレートをHTMLコメントブロック内にMarkdownとして埋め込み、後続エージェントへ渡す入力ファイルの初期状態を生成する。

## Read this when
- エディタ経由で後続AIエージェントへ渡すプロンプト入力ファイルの初期文面や、完全プロンプトの埋め込み形式を確認・変更するとき。
- 初期テキストの説明見出し、記入指針、HTMLコメントによる非表示化の構築処理を調べるとき。

## Do not read this when
- プロンプト全体のテンプレート内容や置換規則そのものを確認したい場合は、完全プロンプトのテンプレート定義を直接読む。
- 構造化文書ノードの定義やMarkdownレンダリング仕様を確認したい場合は、struct_docの実装を直接読む。

## hash
- 801c5e31f4bbfc2b036f94ce9ef77536f12136fe02cba369a4f477b5b6150d35

# `parts`

## Summary
- oracle と realization の基本概念・責務・下位分類・ファイル分類条件をプロンプトに組み込む関数。対象ディレクトリにある基本概念の入口。

## Read this when
- oracle file と realization file の役割や編集主体、正本仕様との関係を確認するとき。
- oracle doc・src・test、realization implementation・test・ancillary の区分を確認するとき。
- ファイルが oracle、realization、uncategorised のどれに分類されるか、パス・git ignore・.git による条件を確認するとき。

## Do not read this when
- 個別の oracle 文書、実装、テスト、補助ファイルの内容や詳細仕様を確認したいときは、対応する対象を直接読む。
- プロンプト部品の共通構築方法や、INDEX.md の生成・探索規則だけを確認したいとき。

## hash
- 11fdebe915f6bc100905ce43e60b6e379d88ab51f3caa587627a16810c95f172

# `policy`

## Summary
- conflict_resolution.py は session join の merge conflict 解消結果に適用する policy を構築し、両マージ元の oracle file の意図・挙動の保持と、両立不能な事項の報告方針を定める。
- editor_input_handoff.py は明示選択された active な prompt editor input へ完成済み content を handoff する際の要求条件、報告、失敗時の扱い、直接書き込み禁止を定める。
- feedback_reporting.py は全 agent call 共通の human feedback 報告 policy を構築し、報告手段と禁止事項を定義する。
- file_access.py は FileAccessMode ごとの agent 向けファイルアクセス規定を構築し、各 mode の deny-list、パス placeholder、保護領域の扱いを定める。
- index_entry.py は INDEX.md エントリー生成用 policy を構築し、責務・読む条件・境界・禁止事項など routing 情報の判断基準を定める。
- oracle.py は oracle file 向け policy を構築し、oracle doc と oracle src の責務分担、委譲、優先関係、未定義事項の扱いを示す。
- oracle_findings.py は oracle file の所見判定 policy を構築し、根拠、fatal・minor の分類、重複報告禁止を定める。
- realization.py は realization file を扱う agent call 向け instruction と policy を構築し、oracle file を正本仕様断片として扱う規定を組み立てる。
- realization_findings.py は oracle file と realization file の適合性調査向け所見 policy を構築し、要求と挙動の不整合や明確な致命的問題を修正対象とする基準を定める。
- routing.py は AgentCallPathContext から routing 用 placeholder と policy header を構築し、INDEX.md による routing 方針を agent prompt に組み込む。

## Read this when
- session join の conflict 解消方針や editor input handoff の実行条件を確認するときは、それぞれの対象から確認を始める。
- agent call 共通の human feedback 報告規定を確認・変更するときは feedback_reporting.py を読む。
- agent call のファイルアクセス mode ごとの制限を確認するときは file_access.py を読む。
- INDEX.md エントリー生成方針や routing 情報の記載基準を確認するときは index_entry.py を読む。
- oracle file の責務分担・優先関係・委譲や所見判定基準を確認するときは oracle.py または oracle_findings.py を読む。
- realization file 向け instruction や oracle・realization 適合性の所見基準を確認するときは realization.py または realization_findings.py を読む。
- AgentCallPathContext を起点とする routing policy の placeholder・header 構築を確認するときは routing.py を読む。

## Do not read this when
- oracle file、realization file、INDEX.md、feedback 報告、routing の意味仕様そのものを確認したい場合は、各 policy の構築元ではなく参照先の正本仕様を直接読む。
- 実際の oracle file や realization file の内容、CLI の具体的な実装、agent call の実行処理を確認する場合は、これらの policy builder ではなく該当する実装・仕様対象へ直接進む。
- PlaceholderMap、SDHeader、SDPolicy の一般的な実装詳細だけを調べる場合は、このディレクトリを読む必要はない。

## hash
- e393a95785f0bf8a6fcb279b6c36222345b30f838e7ff67acc1325aac33081f7

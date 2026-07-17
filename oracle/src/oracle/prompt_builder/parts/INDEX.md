# `apply_review_standard.py`

## Summary
- oracle と realization の適用レビュー基準を構築する正本ソース。明確な仕様不整合、仕様断片の隙間だけでは問題にしない境界、realization 単独で明らかな致命的問題を所見として扱う条件を、背景・要求・例として定義し、構造化文書へ変換する。

## Read this when
- oracle file と realization file の整合性レビュー基準を確認・変更するとき
- 所見として扱う不整合、仕様の未定義部分、致命的実装問題の判断境界を確認するとき
- apply review standard の構造化プロンプト生成処理を変更するとき

## Do not read this when
- 個別の oracle file や realization file の実装内容そのものを調査するとき
- レビュー基準ではなく、CLI やプロンプト生成の別領域を変更するとき

## hash
- 66324f5c139ac3f4e08c85133ecc275307f13f81fc2f01d6dabf8f18813b1e46

# `file_access_rule.py`

## Summary
- ファイル読み書きモードごとのアクセス規則プロンプトを構築する。リポジトリ外、保護対象ツリー、oracle file、realization file などの deny ルールをモードに応じて組み立て、プレースホルダーと構造化文書を返す。ファイルアクセス規則やプロンプト生成処理を変更・調査する際の入口。

## Read this when
- FileAccessMode ごとの読み書き禁止範囲を確認・変更するとき
- ファイルアクセス規則プロンプトの生成内容、プレースホルダー、StructDoc の返却を調査するとき
- READONLY、PURE_ORACLE_READ、REPO_WRITE、PURE_ORACLE_WRITE、REALIZATION_WRITE、NO_RULE の挙動を確認するとき

## Do not read this when
- CLI の個別コマンドや実際のファイル操作の実装を調査するとき
- アクセス規則以外のプロンプト部品や oracle の定義を直接確認するとき

## hash
- 810849959c6a3099a77a4ddf2a6a173946fe3058e81f6a5869a6fa07e928a8fb

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
- oracle file と realization file の定義・役割・下位概念を構築する prompt builder の一部。oracle、realization の責務境界と配置先を説明する StructDoc を返す。

## Read this when
- oracle file と realization file の分類、責務、配置先を確認するとき
- oracle と realization に関する基本説明文の生成処理を変更・調査するとき

## Do not read this when
- 個別の oracle doc・src・test の仕様や実装を確認したいとき
- prompt builder 全体の構成や、基本説明以外の prompt 部品を確認したいとき

## hash
- 52d5324d5a026e9a98b5f944af4b667e19d4b114dd9cf1e66a40c111d3521ea6

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
- `oracle file` に関する規範文面のうち、標準そのものを組み立てる入口。`oracle` の役割や文量・未定義許容・用語統一・命名など、oracle 側の記述方針をまとめて確認したいときに読む。
- 同じ `parts` 配下でも、`oracle` と `realization` の基本概念、`INDEX.md` のルーティング規則、レビューやアクセス規則を確認したいだけなら別の部品を読む方が直接的。

## Read this when
- `oracle file` に書くべき規範や、oracle 側の記述方針を確認したいとき。
- oracle 向けの標準文面を生成・調整したいとき。
- 人間の認知負荷を抑える、正本仕様断片として扱う、未定義部分を許容する、用語や命名を統一する、といった oracle 側の判断基準を見直したいとき。

## Do not read this when
- `oracle` と `realization` の定義や責務境界そのものを確認したいときは、基本概念を説明する部品を読む。
- `INDEX.md` の読み方やルーティング規則を調整したいときは、ルーティング規則の部品を読む。
- レビュー基準、ファイルアクセス規則、realization 側の標準を確認したいときは、それぞれの専用部品を読む。

## hash
- ecb88e6faf0a7d7142d91d60afea5298c5d40c9412e5d111a5d9fd2c281bb8db

# `realization_standard.py`

## Summary
- realization file 全般の規範を組み立てる部品。総文字数の抑制、旧仕様向け実装や重複の整理、コメントや docstring に残す意図、責務分割、抽象化の追加条件、公開面・永続状態・テスト・補助ファイルの増加抑制を見直すときに読む入口になる。

## Read this when
- realization file の量を減らしたい、重複実装や旧仕様向け実装を整理したい、不要なテストや補助ファイルを削減したいとき。
- realization code の責務分割、コメントや docstring に残すべき意図・根拠、過度な圧縮や将来用抽象化を避ける基準を確認したいとき。
- realization file の分割・統合、巨大ファイルの扱い、追加した実装を既存実装と統合できるかを判断したいとき。
- CLI 引数、設定、環境変数、出力項目、状態ファイルなどの公開面や永続状態を増やしてよい条件を確認したいとき。
- realization test の追加・整理で、外部挙動や制御ロジックを検証する範囲、重複テストや過大 fixture の抑制を確認したいとき。
- 外部依存、補助スクリプト、テンプレート、生成物、キャッシュ、ログ、一時ファイルを realization として追加・管理してよいか判断したいとき。

## Do not read this when
- oracle file 側の責務、正本仕様断片の扱い、人間判断と AI 裁量の境界を確認したいだけのとき。
- oracle / realization の基本定義だけを確認したいときは、より基礎的な概念説明を読む方が直接的なとき。
- 特定の CLI 挙動、出力形式、状態ファイル形式、個別コマンド仕様など、具体的なプロダクト仕様を探しているとき。
- realization の実装ファイルやテストファイルそのものを修正するために、対象コードの現在構造や既存テストを調べたいだけのとき。
- INDEX.md エントリーの書き方やルーティング文書の規範だけを確認したいとき。

## hash
- b10977f2789953a75c714c9f4a1ae906418b2486ade30a9924be347e91bcea1f

# `routing_rule.py`

## Summary
- `INDEX.md` を使って次に読む本文を選ぶための案内文を組み立てる。ルーティング方針の骨格を返すだけで、本文そのものは持たない。

## Read this when
- `INDEX.md` の扱い方や、どの階層の文書を読むべきかという案内文を作るとき。
- ルーティング規則の文面を、他の案内文の部品と組み合わせて出力するとき。

## Do not read this when
- `INDEX.md` 自体の内容を編集・評価したいとき。
- 個別機能の仕様本文や実装内容を直接扱いたいとき。

## hash
- ddd2f19bf69e9acb2b20d1ec6b21626a93b9a6e9084ac2f96671c8981ca6e029

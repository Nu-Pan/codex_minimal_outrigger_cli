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
- `FileAccessMode` ごとのファイル読み書き規則文面を組み立てるための入口。`READONLY` / `PURE_ORACLE_READ` / `REPO_WRITE` / `PURE_ORACLE_WRITE` / `REALIZATION_WRITE` / `NO_RULE` の差分や、`repo-root` / `work-root` の扱いを変えるときに読む。
- アクセス規則そのものの言い回し、禁止対象の境界、`NO_RULE` の特例、またはこのルールをプロンプトへ差し込む前提を確認したいときに参照する。

## Read this when
- ファイルアクセスモードの追加・削除・意味変更を行う。
- oracle file と realization file のどちらを読み書き禁止にするか、あるいは `INDEX.md` / `AGENTS.md` / `memo` / `.git` / `.agents` / `.codex` の扱いを変える。
- `repo-root` と `work-root` が一致しない場合の例外や、`NO_RULE` のような特殊モードの挙動を確認したい。
- ファイルアクセス規則の文面を他のプロンプト部品へ流用する、または表示名を変える。

## Do not read this when
- アクセス規則の文面は変えず、呼び出し側でどのモードを選ぶかだけを変える。
- プロンプト全体の構成順や、他の `StructDoc` 部品の内容だけを調整する。
- 実ファイルの権限設定やサンドボックスそのものの実装を変えるだけで、この規則文面を直す必要がない。
- `FileAccessMode` 自体の定義や、それを選ぶ上位ロジックだけを確認したい。

## hash
- fc5c5177c1f988299e100dcbdcd5e8008cbc9fda34d9c5e552fdc64279733fb6

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
- `oracle` と `realization` の基本区分を定義する説明部品です。人間が責任を持つ正本仕様断片と、AI が具体化する実装・補助ファイルの境界を確認したいときに読む入口です。
- `oracle file` / `realization file` の定義、役割、下位概念を最小限に整理しており、用語の混同や責務の取り違えを避けるための基礎参照として使います。

## Read this when
- `oracle file` と `realization file` の違いを確認したいとき。
- oracle 側に書くべきことと、realization 側に実装すべきことの境界を揃えたいとき。
- `oracle doc` / `oracle src` / `oracle test` や `realization implementation` / `realization test` / `realization ancillary` の分類を確認したいとき。

## Do not read this when
- 既に対象ファイルの役割と置き場所が明確で、個別の仕様本文へ直接進めるべきとき。
- 特定の実装内容、CLI 挙動、設定値、テスト内容などの詳細を知りたいときは、この基礎説明ではなく該当する具体の oracle 側本文を読むべきです。

## hash
- f077d5d9668061293d7908155b6eee427999097f2244076edc9501534f706b86

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

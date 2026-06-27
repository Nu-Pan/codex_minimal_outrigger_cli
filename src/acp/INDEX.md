# `builder`

## Summary
- AI エージェント呼び出しに渡す AgentCallParameter を、用途別の complete prompt、補助入力、file access mode、model/reasoning、Structured Output schema 参照として組み立てる builder 群をまとめる領域。
- 対象は、apply fork の変更要約・所見列挙・所見対応、indexing の目次エントリー生成、review oracle の所見列挙・検証・採否・整理、session join の conflict marker 解消、TUI の実行パラメータ解決など、AI に何を依頼し、どの制約と出力契約で呼び出すかを定義する処理である。
- 実際の CLI 制御、git 操作、ファイル更新、レビュー結果の保存、目次ファイルの描画や永続化ではなく、各機能が AI 呼び出しへ渡すプロンプトと呼び出し条件を確認するための入口になる。

## Read this when
- cmoc の各機能が AI エージェントを呼び出す際の prompt、補助文脈、アクセス権限、モデル区分、推論量、Structured Output schema の対応関係を調べたいとき。
- apply fork、indexing、review oracle、session join、TUI parameter resolve のいずれかで、AI に渡す作業目的・禁止事項・標準文脈・入力データがどう complete prompt に組み込まれるか確認したいとき。
- 特定フェーズの出力 schema と、その schema を参照する AgentCallParameter 構築処理を対応づけて確認したいとき。
- AI 呼び出しの file access mode が readonly、pure oracle read、realization write などのどれに設定されるか、またその権限が prompt 上の作業範囲とどう対応するかを追いたいとき。
- 新しい AI 呼び出し builder を追加または既存 builder を変更する前に、同種の呼び出し定義の責務分割や schema 参照の置き方を確認したいとき。

## Do not read this when
- CLI サブコマンドの引数解析、実行順序、状態管理、git branch 操作、merge 実行、ファイル列挙、保存、表示など、AI 呼び出し前後の制御フローだけを調べたいとき。
- AI が返した構造化結果を実際に適用する処理、レビュー結果や目次情報を永続化する処理、または markdown として描画する処理を調べたいとき。
- complete prompt の共通構築規則、StructDoc や render 処理、path model、AgentCallParameter、FileAccessMode などの基礎型そのものを調べたいとき。
- oracle file、realization file、review standard、apply review standard、index entry standard など、builder が参照する標準文脈の本文や一般規約を読みたいだけのとき。
- 個別の AI 呼び出しではなく、対象コマンドの利用者向け仕様、実際の実装修正箇所、またはテストだけを直接確認したいとき。

## hash
- 2fa7d3217c15a26c90e074c17bfdf5257f83b909cb8438de8523b0f8a4d778ee

# `prompt_parts`

## Summary
- AI agent に渡すプロンプトを構成する標準部品群を扱う領域。基本概念、ファイルアクセス制限、ルーティング規則、oracle/realization/review/INDEX エントリーの各標準を、構造化文書として組み立てる実装への入口になる。
- 個別の標準部品だけでなく、それらを完全な agent call 用プロンプトへ結合する処理も含むため、prompt 全体にどの規範や前提情報が注入されるかを追う起点になる。

## Read this when
- AI agent に提示する標準プロンプト片の種類、責務、生成箇所を俯瞰して、どの部品を読むべきか選びたいとき。
- oracle file、realization file、review、INDEX エントリー、ファイルアクセス制限、ルーティング規則などの規範文書が、prompt part としてどこで構築されるか探したいとき。
- agent call 用の完全なプロンプトに標準部品を追加・削除・並べ替えしたい、または標準部品の注入条件や依存関係を確認したいとき。
- 個々の標準文書の本文内容を変更する前に、対象となる prompt part を同階層の中から選びたいとき。

## Do not read this when
- StructDoc、Standard、Requirement など、構造化文書や規範オブジェクトそのものの型・変換処理を調べたいとき。
- CLI コマンド、状態ファイル、パス解決、入出力 schema など、プロンプト標準部品以外のプロダクト挙動を調べたいとき。
- 特定の oracle file や realization file の本文内容をレビュー・実装したいだけで、AI に渡す標準プロンプトの生成処理を確認する必要がないとき。
- 実際のサンドボックス enforcement、OS 権限、外部プロセス実行など、プロンプト上の規則文ではなく実行環境側の制御を調べたいとき。

## hash
- 9ec459022b577d6bbc9dbc5638a2f59b1b6b5ce27dda098f7f9659bb4b90d1f4

# `doc`

## Summary
- cmoc の開発規約と品質検査の手順を定める文書群。開発環境の構築、設計・コーディング、テスト実装、検査実行の判断はここから確認する。
- cmoc のアプリケーション仕様を定める中心的な文書群。セッション、run の隔離、Codex CLI 連携、ファイル分類、ログ、フィードバック、インデクシングなどの挙動を確認する入口。
- CLI サブコマンドごとの仕様を定める文書群。特定のコマンドの引数、前提条件、実行順序、終了処理を確認するときに進む。
- 現在の仕様では採用しなかった設計案と、その判断理由を記録する文書群。現行挙動の実装条件を調べる入口ではなく、設計判断の背景や代替案を確認するときに参照する。
- branch、session、run、oracle、realization の関係を含む、cmoc の開発・実行運用に関する正本仕様を横断的に参照するための文書集合。

## Read this when
- cmoc の正本仕様を全体または複数領域にまたがって調査するとき
- 開発規約、アプリケーション仕様、サブコマンド仕様のどこから読み始めるべきか判断するとき
- 仕様変更や実装変更が、運用規則・Codex CLI 連携・状態管理・ファイル分類のどの領域に影響するか確認するとき
- 採用されなかった設計案の背景や、現行仕様に至った判断理由を確認するとき

## Do not read this when
- 特定の実装関数やテストケースの挙動だけを確認したいとき
- 特定のサブコマンドの詳細が既に分かっている場合は、そのサブコマンド仕様へ直接進むとき
- 開発環境の構築や検査手順だけが必要な場合は、開発規約内の該当文書へ直接進むとき
- 現行仕様ではなく不採用案の背景を調べる必要がない場合は、代替案の文書群へ進まないとき

## hash
- 3d9d6449eb8713e51521d556232dccc06dfddd2d8ada983e75aa4f1008e028c7

# `src`

## Summary
- cmoc の正本ソース実装と JSON スキーマのルート。agent 向け完全 prompt、各種ポリシー、oracle／realization の分類・ルーティング、ACP 呼び出しパラメータ、INDEX エントリー生成、oracle 編集・調査、realization 反映・レビュー、feedback 処理、session 競合解消、TUI 起動、入力引き継ぎ、Markdown 構造化表現、パス・設定・文書参照モデルを扱う。
- prompt_builder は完全 prompt と、oracle／realization、ファイルアクセス、routing、feedback、INDEX エントリー、editor input handoff などの agent 向け規定文面を組み立てる入口。
- acp_builder は各 cmoc サブコマンドの agent 呼び出し条件を構築する入口で、作業対象、アクセスモード、cwd、Structured Output、indexing preflight、各種編集・調査・反映・レビュー経路を定義する。
- other、editor_input_handoff、feedback は、複数機能で共有する構造化 Markdown、パス・設定・文書参照モデル、エディタ入力本文、feedback 報告入力の正本実装とスキーマを提供する。

## Read this when
- cmoc が agent に渡す完全 prompt、個別ポリシー、またはそのプレースホルダー統合の実装を確認・変更するとき。
- cmoc サブコマンドの ACP 呼び出し条件、ファイルアクセス境界、作業ディレクトリ、Structured Output、indexing preflight を確認するとき。
- oracle／realization の編集・調査・反映・レビュー、INDEX エントリー生成、feedback 処理、session 競合解消などの agent 呼び出し経路を横断して調べるとき。
- 共有される構造化 Markdown、パス解決、設定型、文書参照、editor input handoff、feedback 入力契約の実装を確認するとき。

## Do not read this when
- 単一サブコマンドの具体的な実装詳細だけを調べる場合は、該当する acp_builder 配下の個別モジュールを直接読む。
- agent に渡す個別ポリシー本文だけを確認する場合は、prompt_builder/policy または prompt_builder/parts の該当モジュールを直接読む。
- INDEX エントリーの出力形式や生成 call の詳細だけを確認する場合は、acp_builder/indexing の実装とスキーマを直接読む。
- 構造化 Markdown、パス解決、設定、文書参照など共有基盤の個別挙動だけを確認する場合は、other 配下の該当モジュールを直接読む。
- 正本の意味仕様そのもの、実際の realization 実装・テスト、または上位のサブコマンド実行制御を調べる場合は、対応する oracle/doc、src、test、または呼び出し側を直接読む。

## hash
- 584d89c4fcdd4acaef279d777e948ec97938b7a72a6693ee9f8e029234f9c75f

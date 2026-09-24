# `acp_builder`

## Summary
- 各 agent call に渡す prompt と呼び出しパラメータを組み立てる実装群で、共通の呼び出し情報やファイルアクセスモードと、用途ごとの設定を定義する。
- INDEX エントリー生成、feedback issue の処理、oracle の調査・編集、realization の追従・レビュー、run/session の統合、汎用 TUI、利用可能性確認の各フローへ進む入口となる。

## Read this when
- 複数のフローに共通する agent call parameter やファイルアクセスモードの扱いを調べる、または変更するとき。
- 特定の呼び出し定義の所在がまだ分からず、用途別の構成を見渡したいとき。
- 利用可能性確認用の短い agent call の構築を調べるとき。

## Do not read this when
- 単一フローの prompt や出力契約だけを調べる、または変更する場合は、そのフロー専用の下位項目へ直接進む。
- 共通 prompt の合成や描画そのものを調べる、または変更する場合は、呼び出し定義の集まりではなく共通の prompt 構築実装へ進む。

## hash
- c71f5671f6889d06ed99c5b574653624091dcae5e63e2ac52793b8292c2bd1fe

# `editor_input_handoff`

## Summary
- editor input handoff の MCP 入出力契約と、handoff 本文・ガイドの構築定義を担う正本ソースの入口です。
- handoff 全体の運用仕様から参照される、契約と生成内容の詳細を確認する場所です。

## Read this when
- handoff MCP の入力説明や受理条件、結果形式を確認・変更するとき。
- 項目別入力と送信元情報からの本文生成や、受信先ガイドの構築を確認・変更するとき。

## Do not read this when
- target の登録・有効期間、処理手順、失敗時の扱いなど、handoff 機能全体の仕様を確認するときは、その機能の仕様書を直接読んでください。
- agent に渡す handoff instruction の利用条件・送信手順・責務を確認するときは、その instruction の文面定義を直接読んでください。

## hash
- a2a1263148e18bfbd7bc09d014034824d810a0f333b5cb8c958c0676e6ec0ee8

# `feedback`

## Summary
- 定義するのは feedback observation の agent 提出入力契約で、tool discovery と受け入れ検査が共通して参照する。

## Read this when
- feedback observation の提出データが満たす構造や制約を確認・変更するとき。
- reporter と collector で共有する入力検査の契約を確認するとき。

## Do not read this when
- 報告対象の判断基準や収集・保存の動作を確認するときは、feedback observation の正本仕様を読む。
- agent 向け報告指示の文面や prompt への配置を確認するときは、その生成を担う prompt builder を読む。

## hash
- 709d2b0ca7660b1772a43fe8fdaed710d40142564511ba28a435a49b6776aa67

# `other`

## Summary
- 共通のデータモデルと変換処理を担い、構造化文書の Markdown 化、agent call のパスと root placeholder の解決、cmoc 設定モデル、文書参照の表現と Markdown 化を扱う。

## Read this when
- 構造化した文書要素の Markdown 表現や整形処理を変更・調査するとき。
- agent call の作業ルートや root placeholder の導出・解決を追うとき。
- リポジトリごとの cmoc 設定モデルや Codex 呼び出し設定の既定値を変更するとき。
- 文書参照のデータ表現やインライン・一覧形式の描画を変更するとき。

## Do not read this when
- 特定の処理で使う Codex 呼び出し引数やプロンプト内容の組み立てを追うときは、その生成処理を直接読む。
- プロンプトの規定や部品の構成を変更するときは、プロンプト構築側を読む。
- 文書引き継ぎや feedback の個別ワークフローを変更・調査するときは、それぞれの処理を直接読む。

## hash
- 74fb243037b93c0e6495b1d7d9d0df359866098f1c8b0464e502986cad867055

# `prompt_builder`

## Summary
- agent call 向けの共通 prompt と policy 文面を構築し、呼び出しごとに選択・合成する。共有指示やその組み立てを変更するときの入口となる。
- 競合解消用 prompt と editor 起動前の案内も生成する。

## Read this when
- 共通 prompt の構成、placeholder の統合、または呼び出しごとに適用する共通 policy の選択を変更・追跡する場合。
- 共通 policy の指示文、競合解消用 prompt、または editor 起動前の案内の生成を変更・確認する場合。

## Do not read this when
- 特定の call の task、scope、追加入力だけが対象で、共通 policy やこの領域の prompt 生成に影響しない場合は、その call 固有の構築箇所から確認する。
- prompt の意味仕様の確認・改訂が目的の場合は、生成定義ではなく該当する正本仕様から確認する。

## hash
- 1854014e850c201f3ca4769bab51e91f3b70526fae4c67a0ffa1c39fb937eeae

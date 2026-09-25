# `acp_builder`

## Summary
- agent call 共通のパラメータとファイルアクセスモードを定義し、用途別 builder が prompt と起動条件を組み立てる。
- quota 確認、競合解消、TUI、feedback、oracle 調査・編集、realization の追従・refactor、index entry 生成に関する call 定義への入口となる。

## Read this when
- agent call の共通パラメータやアクセスモード、cwd、editor input handoff、自動 indexing の設定を追加・変更するとき。
- 複数の用途別 call 定義を横断して、prompt の構成や起動条件を確認するとき。

## Do not read this when
- 特定の用途の call 定義だけを変更・調査するときは、該当する下位項目から確認するとき。
- 複数 call で共有される prompt の共通構成そのものを変更するときは、共通 prompt の定義から確認するとき。

## hash
- 32e3ce8b6606dd870c5204976ef7df3a0c38eb6b932f6236835c45d00c4be590

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
- cmoc の処理を横断して使う設定値、agent call 起点のルート・パス表現、および文書参照のデータ構造を扱う。
- 構造化された文書ノードの Markdown 描画と文書参照の表現も提供する。これらの共通モデルや変換を変更するときの入口となる。

## Read this when
- 開発対象リポジトリごとの設定値や Codex call の設定モデルを変更するとき。
- ルートプレースホルダー、agent call の作業場所から導く repository/work root、またはパスの解決・変換を調べるとき。
- 構造化文書の Markdown 描画、文書参照のデータ形式や表示を変更するとき。

## Do not read this when
- 特定のコマンドや処理フローの手順・制御・プロンプトを変更し、ここにある共通モデルや表現形式が関係しないときは、その機能の実装へ進む。
- 正本仕様の意味を確認または変更するときは、実装モデルではなく該当する仕様文書を直接読む。

## hash
- 74fb243037b93c0e6495b1d7d9d0df359866098f1c8b0464e502986cad867055

# `prompt_builder`

## Summary
- agent call 向けの構造化 prompt を組み立て、共通規定の選択、追加文面の配置、置換値の統合を行う。置換値の衝突は拒否する。
- ファイルアクセス、oracle と realization の扱い、文書 routing、所見、競合解消、editor handoff などの共通規定と、競合解消用 prompt や editor 入力案内の構築を担う。

## Read this when
- 完全 prompt の構成順、規定の選択方法、追加文面の配置、置換値の扱いを変更するとき。
- 複数の共通規定の組み立て方や、競合解消・editor 入力案内の prompt 構築を変更するとき。

## Do not read this when
- 単一の規定文面や案内の構築だけを変更するときは、該当する個別の構築部から確認する。
- 規定の正本上の意味を確認・変更するときは、対応する oracle 仕様から確認する。この領域は prompt 構築を担い、意味仕様の正本ではない。

## hash
- 5fadab1e726f1afe2064ca83e1542da0c95435a368d7541880f5f7b0f228cd6e

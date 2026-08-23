# `basic.py`

## Summary
- prompt part を完全な prompt へ組み立てる際の構築時専用 placeholder map の型を定義する。root path は AgentCallPathContext から取得し、placeholder key は二重波括弧を含めない形式に限定する。

## Read this when
- prompt builder の構築時専用 placeholder map の型定義や、placeholder key・root path の扱いを確認するとき
- AgentCallPathContext から取得した root path を含む prompt 構築用マップのインターフェースを確認するとき

## Do not read this when
- prompt part の完全 prompt への組み立て処理そのものを確認するとき
- 実行時の placeholder 展開や、prompt builder の他の責務を確認するとき

## hash
- 563a0b94655174bae2949ce3035ae21cbc92afbbc44a8699713b9ca3909647d2

# `complete_prompt.py`

## Summary
- 選択された各種ポリシー、補助プロンプト、動的な対象情報、placeholder 定義を所定の順序で統合し、agent call 用の完全な構造化 prompt を構築するモジュール。prompt の構成順、各 flag と policy block の対応、placeholder 定義の衝突検査・統合を担う。

## Read this when
- agent call に渡す完全 prompt の構成順や、summary・goal・static/dynamic prompt の配置を変更・確認するとき
- oracle／realization、routing、index entry、feedback、file access などの policy block をどの条件で含めるか確認するとき
- path context 由来および補助 prompt 由来の placeholder 定義を統合する処理を変更・確認するとき

## Do not read this when
- 個別 policy の文面や、その policy が参照する規定だけを確認したいときは、対応する policy builder を直接読む
- prompt の構造化データ型や header/tag block の仕様だけを確認したいときは、oracle.other.struct_doc を直接読む
- agent call の path context や file access mode の定義自体を確認したいときは、対応する oracle.other または oracle.acp_builder の定義を直接読む

## hash
- 3dc55fd487fec0bcbeee6fa4876db64ce73fe7090c68a02bb53d2d7b42a6742a

# `editor_input.py`

## Summary
- エディタ経由のユーザー入力ファイルに注入する初期テキストを構築する関数を定義する。使い方・記入の目安・完全プロンプトの差し込み位置を HTML コメントブロックとして生成する。
- 完全な prompt skeleton は引数で受け取り、SDHeader、SDTagBlock、render_sd_node_as_markdown を用いて初期表示文面へ整形する。

## Read this when
- エディタ経由で受け取るユーザープロンプトの初期表示文面や、その HTML コメント形式の案内を変更・調査するとき。
- prompt template の `{{original-prompt-here}}` 位置へ入力内容を配置する前段の初期テキスト生成を確認するとき。
- SD ノードから Markdown を構築し、完全 prompt skeleton を初期テキストへ埋め込む処理の入口を確認するとき。

## Do not read this when
- 完全 prompt skeleton の内容や、各 build_*_parameter が所有するプロンプト構築責務を確認するときは、対象の利用側実装を直接読む。
- 入力ファイルの lifecycle、保存記録としての扱い、original prompt の確定処理を確認するときは、これらを担当する実装や仕様を直接読む。
- 後続 AI エージェントへ渡される最終プロンプト全体の仕様や編集後入力の読み出し処理だけを確認したいとき。

## hash
- c8c082720f8435ba6ee9983056596264a1030e9e0a0e4f07aa978f8c6ecdff1c

# `parts`

## Summary
- 対象ファイルは、oracle・realization・uncategorised file の基本概念と分類条件を root 定義に基づくパス付き説明として prompt に組み込む prompt builder part。分類説明を生成・変更・確認する際の入口であり、個別ファイルの責務や分類文面の正本仕様そのものを扱う対象ではない。

## Read this when
- oracle と realization の基本的な役割、下位分類、分類条件を prompt に組み込む処理を調べるとき
- oracle file・realization file・uncategorised file の分類説明を生成する part の責務を確認するとき
- root の work-root 定義を call-scoped context から取得し、説明文中のパス表現へ反映する処理を確認するとき

## Do not read this when
- oracle・realization の分類文面そのものの正本仕様を確認または変更するとき
- 個別の oracle doc・oracle src・oracle test・realization implementation・realization test の具体的な責務や実装を調べるとき
- prompt builder の共通構造、PlaceholderMap、SDHeader などの一般仕様だけを確認するとき

## hash
- 265574b53cae1118dde88cb5f52298013c52b134bafcd4053f4a2c6500d02c13

# `policy`

## Summary
- prompt builder の policy 定義群を扱うディレクトリ。agent call に渡す共通・用途別の instruction、アクセス制約、所見基準、INDEX.md エントリー生成規定などの構築元を確認する入口であり、個別 policy の責務に応じて下位ファイルへ進む。

## Read this when
- agent call の prompt に組み込む policy の生成・変更経路を調べるとき
- 特定用途の instruction、ファイルアクセス制約、feedback 報告、所見判定、INDEX.md エントリー生成の責務を確認するとき
- 複数の policy 間の構造化ヘッダーや共通規定の接続を調べるとき

## Do not read this when
- ドメイン固有の正本仕様や個別 realization の具体的な実装を確認する場合
- SDHeader、SDPolicy、PlaceholderMap 自体の汎用仕様を確認する場合
- 生成済みの INDEX.md エントリーや INDEX.md の処理全体だけを確認する場合は、該当する正本または処理実装を直接読む

## hash
- f11c5e2100b41c0cc0e1c1aca09109e982439d9781d88c8d3250b04e3713c5b7

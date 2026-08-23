# `basic.py`

## Summary
- prompt part を完全な prompt へ渡すための構築時専用 map の型エイリアスを定義する。
- map のキーは二重波括弧を含まない文字列で、値は文字列または Path を扱う。
- prompt builder の基本的な placeholder 対応型を確認する入口であり、具体的な prompt 構築処理そのものは扱わない。

## Read this when
- prompt 構築時に使用する placeholder map の型や値の許容範囲を確認したいとき。
- prompt builder の基本型定義から関連する実装の参照先を判断したいとき。

## Do not read this when
- prompt の生成手順や placeholder の具体的な解決処理を確認したいとき。
- root path の取得元や AgentCallPathContext の詳細を確認したいとき。
- prompt builder 全体の設計規則や実行時の挙動を確認したいとき。

## hash
- 3084752b9e9d2f1826e83503205a4edc2ad9778be535ddc1db2870109a687ece

# `complete_prompt.py`

## Summary
- 選択された方針・補助文面・placeholder 定義を統合し、agent call 用の完全な構造化 prompt を構築するモジュール。prompt の固定部分から動的部分までの配置順と、各 policy builder の組み込み条件を管理する。
- prompt の基礎規定、選択された domain policy、補助 static/dynamic prompt、objective、placeholder 定義を、指定された順序で一つの prompt 配列へまとめる。
- placeholder は path context と各 builder の定義を統合し、同名で異なる値がある場合は衝突として拒否する。

## Read this when
- agent call 用 prompt の全体構成、policy flag と prompt block の対応、static／dynamic part の配置順を変更・確認するとき
- prompt に含める file access、routing、oracle／realization、findings、conflict resolution、INDEX entry 各方針の選択条件を確認するとき
- path context や補助入力から placeholder を統合し、同名定義の衝突を扱う処理を変更・確認するとき
- prompt builder の呼び出し結果や objective と placeholder definition の配置を調査するとき

## Do not read this when
- 個別の policy 文面そのものを確認・変更するときは、対応する oracle/src/oracle/prompt_builder/policy または parts の builder を直接読む
- prompt の構造化データ型や header／tag block の仕様だけを確認するときは、SDHeader、SDTagBlock、FileAccessMode、AgentCallPathContext の定義元を直接読む
- INDEX.md のルーティング規則や entry の内容だけを作成・確認するときは、この prompt 構築実装ではなく対象の INDEX.md と routing 規定を読む

## hash
- 9355896f8153dcde23358abe0075736c36908332d54018bb6bf05ea5820704d5

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
- oracle file と realization file の基本的な役割・分類・正本関係を定義する説明部品群。oracle doc／src／test、realization implementation／test／ancillary、uncategorised file の判定へ進むための基礎的な入口。

## Read this when
- oracle と realization の責務や正本関係を確認するとき
- oracle doc・oracle src・oracle test の区分を判断するとき
- realization implementation・realization test・realization ancillary の範囲を判断するとき
- uncategorised file の分類条件を確認するとき

## Do not read this when
- 個別の oracle 文書・実装・テストの内容を確認したいとき
- 個別の realization 実装・テスト・補助ファイルの具体的な挙動を確認したいとき
- prompt builder の別部品の責務や関数の呼び出し手順だけを確認したいとき

## hash
- 9b74e847341e38f27b590f4ed524667e2bd1c560a258360f4ca44047cdde7ece

# `policy`

## Summary
- prompt_builder の各 policy 実装を集約するディレクトリ。session join の conflict resolution、feedback reporting、file access、INDEX.md entry、oracle・realization、findings、routing など、agent call 用の SDHeader/SDPolicy と PlaceholderMap の構築責務を扱う。個別 policy の文面や適用条件を変更・確認する際の入口となる。

## Read this when
- agent call に組み込まれる共通または用途別 policy の構築責務、適用条件、要求・禁止事項、placeholder の生成を調査・変更するとき
- prompt builder が conflict resolution、feedback reporting、file access、routing、oracle、realization、findings、INDEX.md entry の各 policy をどのように構成するか確認するとき
- 複数の policy 実装にまたがる構造や、用途別 policy の選択・配置を確認するとき

## Do not read this when
- 個別 policy の正本仕様や domain 固有の判断基準を確認する場合は、対応する oracle または app_spec を直接読む
- 個別ファイル・ディレクトリの具体的な責務や内容を確認する場合は、このディレクトリの対象ファイルを直接読む
- 生成済み prompt 全体の構成、INDEX.md の意味要件、SDHeader・SDPolicy・PlaceholderMap の汎用仕様だけを確認する場合は、それぞれの共通実装または正本仕様を直接読む

## hash
- 0a8eaac4fe6218b74aa18472b27c5ee3ff74f3731aef4ba2407a5658729a2038

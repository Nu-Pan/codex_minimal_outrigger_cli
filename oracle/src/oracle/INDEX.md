# `acp_builder`

## Summary
- AI agent 呼び出しに共通する parameter と、各ワークフロー向けの prompt・アクセス制御・検索範囲・出力要件の組み立てを担う。
- 複数の CLI 操作や処理段階の呼び出し設定をまとめている。個別ワークフローの設定を追う場合は、その責務に対応する下位項目が入口となる。

## Read this when
- agent に渡す prompt や呼び出し条件、ファイルアクセス・文書検索の範囲、出力要件の定義を追加・変更・調査するとき。
- 複数のワークフローのうち、どの呼び出し設定が対象の処理段階を担うか調べるとき。

## Do not read this when
- ワークフローの規範的な要件や受け入れ条件を確認するとき。該当する正本仕様を直接参照する。
- agent の実行・起動処理や、共通 prompt 部品の実装だけを調べるとき。それぞれの担当実装へ進む。

## hash
- 278bac045c9404679d55347d8f0c82563d357b6f110d1d98b254261ff13e3650

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
- 複数機能で共有するモデルと変換ヘルパーをまとめる領域です。設定・文書検索のデータ、文書参照、構造化 Markdown、ルートパスと Git worktree を扱います。
- 個別機能の処理全体ではなく、これらのモデルやヘルパーの定義を調べる入口です。

## Read this when
- agent call のパスコンテキスト、ルートプレースホルダー、Git worktree のパス解決を調べるとき。
- 共有設定や文書検索の型・初期資材・MCP 入出力の定義を調べるとき。
- 文書参照の表記や、構造化した内容から Markdown を組み立てる処理を調べるとき。

## Do not read this when
- 特定機能の処理順序や検索結果の生成・失敗処理を追うときは、その処理を担う実装から確認してください。
- 文書検索や設定の意味、制約、未確定事項を確認するときは、対応する正本仕様から確認してください。

## hash
- 94f21c0d770bde31a1100bde5808222eaa28bf0d77331b91b2f7e1b209b471c0

# `prompt_builder`

## Summary
- 選択された共通規定や追加指示をまとめ、placeholder の定義を整合させて agent prompt を構築する層です。
- 規定文面や基礎説明の部品に加え、merge 競合解消用 prompt と editor 起動前の案内を組み立てます。

## Read this when
- 複数の呼び出しで共有される prompt の組み立て方や、共通規定の注入方法を変更・調査するとき。
- merge 競合解消用 prompt の共通構成や、生成される規定・案内の構築責務を調べるとき。

## Do not read this when
- 特定の agent call が渡す task、scope、規定の選択、追加入力だけを変更するとき。その call を設定する呼び出し側から確認してください。
- 生成される規定の意味や要件を変更するとき。意味仕様の正本から確認してください。
- 個別の規定文面や基礎説明だけを変更するとき。該当する部品の実装から確認してください。

## hash
- fd6078ac0f4cbd8ba4a0d4291e1bcc4ef5f0656f661551ecfd0faa95f24e2f45

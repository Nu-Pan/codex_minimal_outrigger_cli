# `acp_builder`

## Summary
- AI コーディングエージェント呼び出しに渡す論理パラメータと、各機能向けの prompt・Structured Output schema・ファイルアクセス条件・モデル設定を定義する oracle src 領域。
- 共通の呼び出しパラメータ定義を入口に、差分適用後レビュー、ルーティング文書生成、oracle レビュー、merge conflict 解消、TUI 起動などの用途別 agent call parameter 正本仕様へ進むための分岐点になる。
- サブコマンドや処理段階ごとに、AI へ渡す role、summary、goal、読み取り制約、標準文書の組み込み、出力契約を確認するための下位領域を収める。

## Read this when
- cmoc が AI コーディングエージェントを呼び出す際の論理パラメータ、prompt、Structured Output schema、モデルクラス、reasoning effort、ファイルアクセスモードの正本仕様断片を確認したいとき。
- 差分適用後のレビュー・報告、INDEX.md エントリー生成、oracle file レビュー、merge conflict 解消、TUI 起動のいずれかで使う agent call parameter を確認・変更したいとき。
- 各 agent call に渡す入力情報、読み取り・編集制約、出力互換性、根拠情報の粒度、空でない前提、所見や作業指示の応答契約を用途別にたどりたいとき。
- realization src で agent call parameter の変換・生成・実行接続を実装またはテストする前に、oracle src 側の正本仕様断片を確認したいとき。

## Do not read this when
- 実際の CLI 引数解析、サブコマンドの実行制御、git 操作、状態管理、ファイル書き込み、結果集約、表示処理など realization implementation 側の流れだけを調べたいとき。
- 具体的なバックエンド用モデル名、実行コマンド、サンドボックス設定、path placeholder 解決、prompt builder、構造化 markdown 描画などの共通実装そのものを確認したいとき。
- oracle file 全般の品質基準、realization standard、review oracle standard、index entry standard など、agent call に組み込まれる標準本文自体を読みたいとき。
- 個別ファイルのパッチ内容、diff 生成手順、merge conflict marker 検出、TUI の入力取得、レビュー所見の実行結果処理など、agent call parameter 生成より外側の処理を調べたいとき。

## hash
- b9b0ab444f940b96957409e227822613bbc46a71dda0cd98d7f5de09f036f642

# `other`

## Summary
- cmoc の横断的な基礎概念を定義する oracle src 群を扱うディレクトリ。リポジトリ単位の設定、ルートパスプレースホルダと解決規則、規範文書モデル、構造化 Markdown レンダリング helper への入口になる。
- 個別サブコマンドの仕様ではなく、cmoc 全体で共有される設定・パス・仕様文生成の正本仕様断片を確認するための起点として読む。

## Read this when
- リポジトリ単位の cmoc 設定、Codex CLI 向けモデル・reasoning effort 対応、AI エージェント呼び出し並列数、apply fork や review oracle の上限値を確認したいとき。
- <cmoc-root>、<repo-root>、<run-root>、<work-root> などのルート概念、プレースホルダ付きパスの解決、実パスからプレースホルダ表記への変換、プレースホルダなし相対パスの扱いを確認したいとき。
- 規範文書を構造化して保持するモデル、要求ラベル、背景・要求・判断例の分解、構造化ドキュメントへの変換規則を確認したいとき。
- 階層化された自然言語文書を Markdown としてレンダリングする helper の挙動、見出し生成、本文・コードブロック・インデント正規化・空行圧縮を確認したいとき。

## Do not read this when
- 個別 CLI サブコマンドの利用者向け入出力、実行フロー、状態ファイル仕様そのものを調べたいとき。
- INDEX.md のルーティング規則、oracle file と realization file の管理方針、または実現ファイルに適用される品質基準そのものを確認したいとき。
- Markdown 文書や規範の内容そのものを読みたいだけで、規範モデルやレンダリング helper の構造を確認する必要がないとき。
- Codex CLI の外部仕様、利用可能モデルの最新情報、または設定値を読み書きする実装手順だけを確認したいとき。

## hash
- 3e4fdca0f774d8da44c356816504725851477d92c6a17ab1c07749a7ce2f2aeb

# `prompt_builder`

## Summary
- agent call に渡すプロンプトを構築するための型定義、高水準 builder、完全プロンプト生成処理、標準文書・規則文書パーツを収めるディレクトリ。
- oracle / realization / review / INDEX エントリーなどの標準プロンプト注入、追加プロンプト、プレースホルダ定義、ファイルアクセス規則、ルーティング規則を最終的な StructDoc へ統合する処理への入口。
- 各標準プロンプト本文を確認する場合はパーツ群へ、プロンプト全体の構築順序や注入フラグ間の依存を確認する場合は高水準 builder へ進む。

## Read this when
- agent call 用の完全なプロンプト生成順序、静的プロンプトと動的プロンプトの分離、またはプロンプトキャッシュを意識した構成を確認・変更するとき。
- oracle standard、realization standard、review standard、apply review standard、index entry standard などの注入フラグ間の依存関係を確認・変更するとき。
- role、summary、goal、補助プロンプト、プレースホルダ定義、ファイルアクセス規則、ルーティング規則が最終プロンプトへどう組み込まれるかを確認するとき。
- プレースホルダ置換用 mapping の基本型や、置換先 value として文字列または Path を扱う境界を確認したいとき。
- oracle file、realization file、ルーティング、ファイルアクセス、レビュー判定、INDEX.md エントリー規範など、標準プロンプト本文の内容と判断基準を確認したいとき。

## Do not read this when
- 生成済みプロンプトを受け取った後の agent call 実行処理や結果処理を調べたいときは、呼び出し側の実装を読む。
- StructDoc、FileAccessMode などの汎用データ構造そのものを確認したいだけなら、それぞれの定義元を読む。
- 特定の CLI 機能、入出力 schema、状態ファイル形式、パスモデル、個別コマンド仕様を確認したいときは、対応する仕様または実装を読む。
- 実際の realization implementation や realization test の現在構造を調べて修正したいだけのとき。
- oracle doc、oracle src、oracle test の個別内容を確認したいとき。

## hash
- 5b966331518f3448011aba0c453e4dd722cd48fc700a814a60c238b290605c72

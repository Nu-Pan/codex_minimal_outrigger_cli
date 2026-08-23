# `acp_builder`

## Summary
- `oracle/src/oracle/acp_builder` は、用途別の AgentCallParameter 構築定義をまとめた領域で、モデル・推論・アクセス権限・prompt・Structured Output・作業ディレクトリ・preflight などの起動条件を確認する入口である。配下には共通の型定義、feedback、indexing、oracle、quota probe、realization、session、tui の用途別定義がある。

## Read this when
- Agent call の用途別起動パラメータ、prompt、アクセス範囲、モデル・推論設定、作業ディレクトリ、indexing preflight を変更・調査するとき
- 特定用途の AgentCallParameter 構築定義へ進む入口を選ぶとき
- oracle、realization、feedback、indexing、session、tui、quota probe の agent call 定義を確認するとき

## Do not read this when
- Agent call の実行処理そのもの、CLI サブコマンドの処理、TUI の画面表示、個別の oracle・realization file の内容を直接調査するとき
- 共通 prompt 生成規則や ACP パラメータの型定義だけを確認したいときは、それぞれの下位対象を直接読むとき

## hash
- 718bce87c25820cf87f6408c3ecc1933d3e4a7ed472a02e574ccbe997dbc7664

# `feedback`

## Summary
- 対象ディレクトリは、agent が検出した問題を feedback reporter から collector へ渡すための入力契約を扱う領域です。問題の分類・重要度・影響、人間の対応が必要な理由、原因の確信度、再確認可能な根拠、作業継続状態を表現・検証する下位要素への入口になります。

## Read this when
- feedback reporter の入力形式や、検出した問題を人間向け feedback として構造化する処理を確認するとき。
- 入力契約を構成するスキーマや関連する検証定義を調査・変更するとき。

## Do not read this when
- collector 側の保存、集約、重複判定の仕様だけを確認したいとき。
- feedback の検出方法や、agent が作業を継続するかどうかの判断ロジックだけを確認したいとき。

## hash
- a86d0e0a2687a4eed300cd97383ba6e521f2347418e4446a2bfba702aedcd9ba

# `other`

## Summary
- cmoc の共通基盤となる補助モデルと Markdown レンダリングを扱うディレクトリ。設定モデル、agent call 単位のルートパス解決、構造化文書・cmoc ブロック・ポリシー・コードブロックの GFM レンダリングが主な対象で、各機能の実装モジュールへ進む入口となる。

## Read this when
- cmoc のリポジトリ固有設定、Codex CLI 設定、設定の JSON/TOML 表現を確認するとき
- プレースホルダ付きパスと実パスの変換、Git worktree からの root 導出、agent call のパスコンテキストを確認するとき
- 構造化された文章、cmoc_block／cmoc_ref、SDPolicy、コードフェンス、Markdown の整形処理を確認するとき
- 設定・パスモデル・文章レンダリングの複数領域にまたがる共通処理の入口を探すとき

## Do not read this when
- Codex CLI の呼び出し処理や特定の CLI サブコマンドの責務を確認するとき
- oracle review の所見生成・マージ・検証ロジックを確認するとき
- 参照タグの対応検査、ポリシーの意味的統合、prompt part の選択処理を確認するとき
- 設定ファイルの実際の保存内容や人間による調整結果だけを確認するとき
- Git worktree の一般的な操作や個別の開発規則を確認するとき

## hash
- 7df47add24b2b93f76555233189463416905cf7f79fa3dc229e99eb0854ede58

# `prompt_builder`

## Summary
- prompt builder の構築時型定義、完全 prompt の統合構築、エディタ入力用初期文面、oracle／realization 分類説明、policy 定義群を扱うディレクトリ。agent call に渡す prompt の構成要素と、その用途別の下位実装へ進むための入口を提供する。

## Read this when
- prompt builder における placeholder map、完全 prompt の構成順、policy block の組み込み、エディタ入力文面、oracle／realization 分類説明の生成を確認・変更するとき
- 共通 policy や用途別 instruction、アクセス制約、feedback 報告、INDEX.md エントリー生成規定の構築元を調べるとき

## Do not read this when
- 個別 policy の文面や、それが参照する正本規定だけを確認したいときは対応する policy builder を直接読む
- prompt の構造化データ型や header/tag block の汎用仕様、path context・file access mode の定義、個別 oracle・realization ファイルの責務を確認したいときは、それぞれの正本または定義対象を直接読む
- 生成済み INDEX.md エントリーや INDEX.md 全体の処理だけを確認したいとき

## hash
- dcdc79ecabe6050ba092dff63e1eae675ecfb2db0f11c39fa9af3a6af8ff2f85

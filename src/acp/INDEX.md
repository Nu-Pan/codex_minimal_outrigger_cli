# `builder`

## Summary
- AI エージェント呼び出し用パラメータを組み立てる builder 群への入口。フォーク適用、目次エントリー生成、oracle レビュー、session 処理、TUI パラメータ解決など、各機能が下流エージェントへ渡す役割・目的・補助文脈・権限・モデル設定・Structured Output schema の接続を扱う。
- 実際の業務処理、差分解析、レビュー判定そのもの、ファイル更新、CLI 制御フローを直接担う領域ではなく、AI に依頼する作業内容と返却契約を機能別に構成するための入口である。

## Read this when
- 各コマンドや処理フェーズから AI エージェントへ渡す complete prompt、role、summary、goal、補助プロンプト、モデル選択、推論量、ファイルアクセス権限を確認または変更したいとき。
- フォーク適用、INDEX.md 用エントリー生成、oracle file レビュー、session 関連の conflict 解消、TUI 入力からの実行パラメータ解決のどの呼び出し設定へ進むべきかを判断したいとき。
- AI 呼び出しの入力文脈と Structured Output schema の対応、または schema による返却形の制約を、機能別の builder 実装から確認したいとき。
- raw diff、対象本文、oracle file、既存所見、対象ファイル一覧、利用者入力などが、どのような補助文脈として prompt に埋め込まれ、どの権限でエージェントに渡されるかを追いたいとき。

## Do not read this when
- フォーク適用、目次更新、レビュー、session、TUI などのコマンド全体の制御フロー、保存、表示、状態管理、CLI 入出力を調べたいとき。
- git 操作、差分解析、所見の統合・重複排除、修正結果の検証、merge 実行や conflict 検出など、AI 呼び出しパラメータ構築の外側にある実処理を探しているとき。
- complete prompt の共通構築、Markdown レンダリング、パスモデル、ACP の基礎型など、複数領域で共有される汎用部品だけを確認したいとき。
- 個別の Structured Output 項目の意味や詳細だけを確認したいときは、該当する schema 本文へ直接進めばよい。

## hash
- db3debc81c0ddff3d09773cf623d66c945face4a1e7eafc5954e8b9fea4f9953

# `prompt_parts`

## Summary
- AI agent に渡す各種 prompt part を構築する実装群を収める領域。ファイルアクセス規則、INDEX.md ルーティング規則、oracle/realization の基本概念、oracle・realization・review・index entry の各標準、agent call 用の完全な prompt 組み立てを扱う。
- 各 prompt part は、標準文書や作業規則を StructDoc などの構造化文書として生成し、上位の agent 呼び出し処理へ渡すための入口になる。
- 個別の規範本文を確認する対象と、複数の規範を統合して agent 向け prompt list を作る対象が同じ階層に並ぶため、prompt に含めたい規則の種類から読む先を選ぶための入口になる。

## Read this when
- AI agent に渡す prompt part の種類、責務分担、または生成箇所を調べたいとき。
- file access rule、routing rule、oracle/realization の基本説明、oracle standard、realization standard、review standard、index entry standard など、標準 prompt の本文を確認または変更したいとき。
- agent call 用 prompt の全体構成、標準 prompt の注入順、標準 prompt flag 間の依存関係、root token 置換や呼び出し先向けの文面 sanitization を追いたいとき。
- oracle file や realization file のレビュー、実装、案内文作成で、AI にどの判断基準を提示しているかを確認したいとき。
- 新しい標準 prompt part を追加する前に、既存の prompt part が担う規範領域や共通の構造化文書生成方針を把握したいとき。

## Do not read this when
- 個別 CLI コマンドの実行処理、状態ファイル、入出力 schema、パス解決、サンドボックス enforcement など、prompt 文面生成以外のプロダクト挙動を調べたいとき。
- Standard、Requirement、StructDoc、code block などの汎用データ構造やレンダリング helper そのものを変更したいとき。
- oracle file や realization file の特定本文、または実際の差分レビュー対象を読みたいだけで、AI に渡す標準 prompt の生成処理は関係しないとき。
- ファイルアクセスやルーティングの実際の実行制御を調べたいとき。ここでは agent に提示する規則文の構築だけを扱う。
- path token の定義、実 path 解決規則、work/root 概念の基礎実装を確認したいとき。

## hash
- c59d029bfba0ae4cba28d81ecd3ea35719efa92e8e5738c3f733bfb5bf5355d0

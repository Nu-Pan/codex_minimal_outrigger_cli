# `acp_builder`

## Summary
- 対象ディレクトリ内の Agent Call 構築定義と、用途別の下位領域への入口を提供する。
- oracle・realization・feedback・indexing・session・TUI・quota probe など、各用途に固有の prompt・出力契約・起動条件を扱う。

## Read this when
- 各用途の agent call について、prompt、Structured Output 契約、ファイルアクセス範囲、作業ディレクトリ、preflight、起動条件を確認・変更するとき。
- oracle file の編集・調査・レビュー、realization 差分追従、feedback issue 判定、INDEX エントリー生成、quota probe、session join の conflict 解消、または TUI 起動の構成を調べるとき。

## Do not read this when
- agent call の共通パラメータ型、ファイルアクセスモードの正本上の意味、共通 prompt 構築、またはパス解決の一般規則だけを確認したいとき。
- oracle file の具体的な編集内容、レビュー規則、realization の実装・テスト、feedback issue の内容生成、または session join の conflict 処理そのものを確認したいとき。
- 既存の INDEX.md のルーティング内容を確認したいとき。

## hash
- ee8f7053060282eacdf8ebe2fa7e231c27b17992d1fa3a4b6eadd66cc40d4b9c

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
- cmoc のリポジトリ固有設定をデータクラスとして定義する。並列数、Codex CLI の provider・agent call 設定、ファイルアクセス違反時のリカバリ回数、oracle review の各ループ上限を扱う設定モデルの入口。
- cmoc で使用する root path placeholder と、agent call ごとの cwd・worktree・repository の対応を定義する。placeholder と実パスの相互変換、Git worktree を基準とした root 解決、パス境界の挙動を扱う実装の入口。
- 構造化された文書要素を Markdown にレンダリングする。見出し階層、参照可能な cmoc ブロック、コードフェンス、規定文、空行および三重引用文字列の整形を扱う文書生成ヘルパーの入口。

## Read this when
- cmoc の設定項目、既定値、Codex CLI の provider-local 設定、agent call 設定、または oracle review のループ上限を確認・変更するとき。
- root placeholder の定義・解決、agent call の cwd から導出される work root と repository root、Git worktree に基づくパス境界、または placeholder 付きパスの変換を確認・変更するとき。
- 構造化文書を Markdown 化する処理、見出し深度、cmoc ブロック参照、コードフェンス、規定文、空行圧縮、または三重引用文字列の正規化を確認・変更するとき。

## Do not read this when
- 設定ファイルの実際の JSON 内容、設定の生成・同期や doctor の挙動、Codex CLI 呼び出しまたは oracle review の具体的な処理を確認するとき。
- 特定の CLI 機能や oracle 文書の内容だけを調べ、root placeholder、worktree 境界、agent call のパスコンテキストに関係しないとき。
- Markdown 以外の出力形式、文書要素の具体的な内容、正本仕様、またはこのヘルパーの利用側の処理を直接確認するとき。

## hash
- 53e4e839f09195842b67ca2dbd261218f8f8944948dc6227a5745c791d4f4adf

# `prompt_builder`

## Summary
- プロンプト生成を担う `prompt_builder` の実装群。共通プレースホルダ型、完全 prompt の統合、エディタ初期入力、oracle／realization 概念の説明、各種 agent call policy の構築を扱う。個別ファイルの役割や、prompt の構成・policy・routing・分類規則を確認するための入口である。

## Read this when
- agent call 用 prompt の統合順序、placeholder 競合、固定部分と変動部分の配置を確認・変更するとき。
- prompt builder の個別 policy、oracle／realization の分類説明、INDEX.md routing 規定、feedback reporting、file access 規定を調べるとき。
- エディタへ注入する初期入力や、完全 prompt・oracle／realization 説明の埋め込み構造を確認するとき。
- placeholder 対応表や prompt 構築に関わる共通型・構造化文書ヘッダーの利用箇所を追うとき。

## Do not read this when
- oracle や realization の意味仕様、INDEX.md routing の正本仕様、feedback 報告の意味仕様を確認する場合は、それぞれの対応する oracle doc や app specification を直接読む。
- 実際の agent call 実行処理、path context や placeholder の具体的生成規則、struct_doc の一般仕様を調べる場合は、該当する呼び出し側・生成処理・struct_doc 実装を直接読む。
- 実装・テストの具体的な配置や挙動、個別 policy の根拠となる仕様だけを確認する場合は、このディレクトリ全体ではなく対応する対象を直接読む。

## hash
- ec13f0af44d3903c1576d695397b33cf8d29c2bcee9bfe6392a8d5e00e15975b

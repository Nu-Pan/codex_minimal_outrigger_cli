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
- cmoc のリポジトリ固有設定をデータクラスで集約し、Codex CLI、agent call、oracle review の設定値と永続化対象を定義する。
- agent call の cwd から Git worktree と main repository のルートを導出し、ルートプレースホルダーと実パスを相互変換する。
- 構造化文書の要素を保持し、見出し、参照タグ、コードブロック、規定文を Markdown へ整形する。

## Read this when
- CmocConfig とネストした設定データクラスの責務や既定値、Codex CLI と oracle review の設定項目を確認するとき。
- agent call の cwd、Git worktree、main repository の関係や、{{repo-root}}・{{work-root}}・{{run-root}}・{{cmoc-root}} の解決と変換を調べるとき。
- 構造化文書を Markdown にレンダリングする処理、見出し深度、cmoc_block、コードフェンス、規定文、空行や三重引用文字列の整形を調べるとき。

## Do not read this when
- 設定値を利用して agent call や CLI の具体的な動作を確認したいときは、設定利用側の実装を直接読むべきです。
- パス解決やプレースホルダー変換に関係しない CLI 機能、oracle 文書、agent call 生成規則だけを調べるときは、別の対象を直接読むべきです。
- Markdown レンダリングではなく、構造化文書の具体的な内容や利用側の処理を確認したいときは、呼び出し元や正本仕様を直接読むべきです。

## hash
- 10e79dd2742bb3cc7b0c58b64f7aeddd9264cf041c18f5f5b9e6eb357ac9efff

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

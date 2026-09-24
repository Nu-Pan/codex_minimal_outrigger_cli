# `cmoc_config.py`

## Summary
- リポジトリごとに変わりうる cmoc の設定データ構造と既定値を定義し、Codex provider・呼び出し別設定、並列数、回復試行数をまとめる。
- 永続化され人が調整する設定のモデルについて、正確な項目と既定値を確認する入口。

## Read this when
- 設定項目、型、既定値、またはシリアライズ時の順序を確認・変更するとき。
- Codex の provider-local 設定や agent call ごとの provider・model・reasoning effort の既定選択を調べるとき。
- 最大並列数やファイルアクセス違反時の回復試行数を調べるとき。

## Do not read this when
- 設定の読み込み、検証、ディスクへの保存処理を調べるときは、設定処理の実装へ直接進む。
- Codex CLI への引数反映や障害回復 probe の動作を調べるときは、呼び出し実行の仕様へ直接進む。
- doctor による設定の生成・同期・追跡保証を調べるときは、そのライフサイクルを定める仕様へ直接進む。

## hash
- 8c0ecd1e5dea641a4d4d1e287fbac588f7ab51589b25c897978890649d185afa

# `doc_ref_model.py`

## Summary
- editor input handoff で使う文書参照のデータモデルと Markdown 表記変換を担う。

## Read this when
- handoff の参照値や受け入れ条件を調べる・変更するとき。
- 単一参照や参照一覧の Markdown 表記を調べる・変更するとき。

## Do not read this when
- 参照情報の意味、入力形式、記入条件が目的なら、それらを定める正本仕様や入力 schema を読む。
- handoff 本文の構成や送信元情報が目的なら、本文 builder を読む。

## hash
- 0bff83f413a89dcc2a3f881293a595221ea1012097880bf4661a7af14c949ca5

# `path_model.py`

## Summary
- root placeholder と絶対・相対パスの表記、実パスとの相互変換を担うパスモデル。agent call の cwd と Git worktree 情報から得るパス文脈も定義し、prompt builder が共有する値の正本となる。
- 同階層の設定値・文書参照・構造化文章のモデルとは異なり、パスの表記と解決を扱う。

## Read this when
- root placeholder の表記規則や定義、Git worktree からの解決、実パスとの変換を調べる・変更するとき。
- agent call の cwd から repo/work root を導出し、call-scoped path context として共有する仕組みを確認するとき。

## Do not read this when
- 特定の builder や runtime が cwd を選ぶ手順、agent call の起動順、prompt に含める規定の内容を調べるときは、その処理を担う箇所を直接読む。この対象はパスのモデルと解決を担う。
- cmoc の実行設定、文書参照データ、構造化文章の生成を調べるときは、それぞれのモデルを読む。

## hash
- 7172c36b342a5b115ebddf8f4731b459a305d57195f24b2e2af448f2caabb628

# `struct_doc.py`

## Summary
- 階層化した文章ノードを Markdown に変換し、見出しの深さや参照ブロック、コードブロック、規定文の表現を担う。

## Read this when
- 構造化ノードの Markdown 化、見出しの深さ、コードフェンス、または SDPolicy の表示規則を確認・変更するとき。
- 複数の prompt や文書生成箇所で共有されるレンダリングや文字列整形の結果を追うとき。

## Do not read this when
- 文書参照の保持やインライン・一覧表記が主題なら、参照モデル側から確認するとき。
- 設定値やルートパスの保持・解決が主題なら、設定モデルやパスモデル側から確認するとき。
- 個別の prompt の内容や workflow 固有の要求を変更するときは、その prompt や workflow の組み立て元から確認するとき。

## hash
- 82108c5a2e45e6a12ccd0fad2e797635f574d6aadbf65031d920a3e3872857f8

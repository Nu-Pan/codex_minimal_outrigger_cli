# `cmoc_config.py`

## Summary
- リポジトリごとに変わりうる cmoc 設定のデータ構造と既定値を定義する。並列数、Codex の provider-local 設定、agent call 種別ごとの provider・model・reasoning effort、文書検索設定を扱う。
- 人間が調整する設定データの形と既定の Codex call 選択を確認する入口。

## Read this when
- 設定項目の追加・変更や既定値の見直しで、CmocConfig の構成と値を確認するとき。
- agent call 種別ごとの既定 provider・model・reasoning effort、または provider-local 設定の形を確認するとき。

## Do not read this when
- 設定 JSON の読み書き、構文・値の検証、doctor による生成・同期の処理だけを変更するときは、その処理を担う実装を読む。
- Codex CLI の argv 構築や agent call の実行方法だけを変更するときは、その呼び出し処理や仕様を直接読む。

## hash
- 1bb6c428f273ad7b8dbc1aa00acee4af9cee6e40efc077a6da14b254277f9718

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

# `document_search.py`

## Summary
- 文書検索で共用する推論資材の識別情報、モデル入力条件、再ランキング互換確認の対象を定義する。
- 検索設定の型と stdio MCP の検索 tool、入力、結果、失敗の実装契約を定義する。

## Read this when
- 推論資材やモデル入力、raw 採点の互換確認対象を変更・照合するとき。
- 検索設定の項目や検索 MCP の公開形式を変更・照合するとき。

## Do not read this when
- 検索の意味仕様、アクセス範囲、同期、cache、排他、期限や取消の動作を確認するときは、正本の文書検索仕様を読む。
- caller が渡す閲覧範囲、agent 向け routing 文面、MCP の起動・接続規則を確認するときは、それぞれの担当定義を読む。

## hash
- c85c970a5815d1075e5ee938d52bc931d958d4e01af74897851607c9b10cd555

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

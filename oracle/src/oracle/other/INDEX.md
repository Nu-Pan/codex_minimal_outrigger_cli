# `cmoc_config.py`

## Summary
- リポジトリごとに変わる cmoc 設定のデータ型と既定値を定義し、並列実行数、Codex CLI のプロバイダー設定と呼び出し種別ごとのモデル選択、アクセス規定違反後の再試行回数を扱う。
- プロバイダー固有の設定値を JSON と TOML の両方で表現する。

## Read this when
- リポジトリ固有の設定値や既定値、とくに並列実行数やアクセス規定違反後の再試行回数を確認・変更するとき。
- Codex CLI のプロバイダー設定や、呼び出し種別ごとのモデルと推論強度の選択を確認・変更するとき。

## Do not read this when
- 保存済み設定の読み込み・書き込み、シリアライズ、doctor による生成・同期の処理を調べるときは、その処理を実装する箇所へ進む。
- 個別の agent call の指示文作成や実行フローを調べており、設定値の選択を確認する必要がないときは、その call の実装箇所へ進む。

## hash
- 2dae89b5f70856e073d156dc1f9ae521ff7b2741104498f02efe863f673ffc7f

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

# `acp_builder`

## Summary
- ACP 関連 agent call の正本ソースを機能別に整理するディレクトリ。共通パラメータ型、各サブコマンドの prompt builder、Structured Output schema を扱う。
- indexing、oracle、realization、session、tui の agent call 設定を確認するための入口であり、必要に応じて各機能の下位ディレクトリへ進む。

## Read this when
- ACP の共通パラメータ、モデル・推論強度・ファイルアクセスモードの定義を確認するとき。
- `cmoc indexing`、`cmoc oracle`、`cmoc realization`、`cmoc session join`、`cmoc tui` の agent call prompt、起動設定、Structured Output schema を調査・変更するとき。

## Do not read this when
- 各サブコマンドの通常処理や TUI の画面表示を確認したいとき。
- 正本仕様そのもの、共通 prompt 構築の詳細、個別 builder の実装内容だけを確認したいときは、対応する下位ディレクトリまたはファイルを直接読む。

## hash
- 39168796a24c8670c5274d00103600b1945bc02ba6c3097c724c146b436a221f

# `other`

## Summary
- cmoc の設定・パスモデル・規範構造・Markdown 構造化文書レンダリングを担う oracle 実装群への入口。設定値、パス解決、Standard/Requirement の構造化、StructDoc の生成を扱う。

## Read this when
- cmoc 固有設定や Codex／oracle review 設定を変更・参照するとき
- ルートプレースホルダ、agent call のパスコンテキスト、実パス変換を調査するとき
- Standard・Requirement の構造や StructDoc への変換を調査するとき
- 階層文書の Markdown レンダリング、cmoc_ref 検証、コードブロックやインデント処理を変更するとき

## Do not read this when
- CLI コマンドの実行フローや設定ファイルの生成・同期処理だけを調査するとき
- ModelClass や ReasoningEffort 自体の定義・意味を調べるとき
- 個別の規範本文や StructDoc を通らない文書仕様だけを確認するとき
- これらのモデルやレンダラーと無関係な CLI・realization 実装を変更するとき

## hash
- df8356b3a0a17668fd7be473e0f22f2a7a0975d83ed74c1a1e882c50d33943de

# `prompt_builder`

## Summary
- cmoc が agent call 用プロンプトを構築するための部品群を収めるディレクトリ。プレースホルダ型、完全プロンプト、エディター初期文、oracle／realization 規則や INDEX ルーティング規則の生成を扱う。個別の prompt builder 部品を調査・変更するときの入口。

## Read this when
- プロンプト生成部品の責務や構造を確認するとき。
- oracle／realization の定義・規範、ファイルアクセス制約、INDEX.md ルーティング規則の生成処理を変更・検証するとき。
- レビュー基準や INDEX.md エントリー規範など、生成される標準文書の内容を調査するとき。

## Do not read this when
- 特定の oracle 文書や realization 実装・テストの挙動を調査するとき。
- Python 実行環境やテスト実行方法を確認するとき。
- prompt builder 以外の CLI 機能や共通 StructDoc 実装を直接調査するとき。

## hash
- c897ba3d1b2f37cfdb8b6993335b646b4137e028f19d9f270cf0cc32b5f85e03

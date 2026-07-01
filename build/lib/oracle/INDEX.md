# `acp_builder`

## Summary
- AI エージェント呼び出しパラメータの正本定義と、用途別の prompt・Structured Output schema への入口となる領域。
- 共通の論理モデルクラス、reasoning effort、ファイルアクセスモードに加え、apply fork、目次生成、oracle file レビュー、session join conflict 解消、TUI 起動、アクセス規則違反復旧の呼び出し設定を扱う下位領域へ進むために読む。
- 出力契約や agent call parameter の構成を、目的別にどの下位領域で確認すべきか判断する起点となる。

## Read this when
- AI エージェント呼び出しパラメータの正本側定義、論理モデルクラス、reasoning effort、ファイルアクセスモードを確認したいとき。
- apply fork、目次エントリー生成、oracle file レビュー、session join の conflict marker 解消、TUI 起動、アクセス規則違反復旧の prompt 構成や出力 schema の読む先を選びたいとき。
- Structured Output schema path を含む呼び出しと含まない呼び出しの扱い、または目的別 agent call の role、goal、制約、placeholder、file access mode の正本を確認または変更したいとき。

## Do not read this when
- agent call の実行手順、プロセス起動、結果処理、永続状態管理、git 操作、fork 作成、branch 操作などの実行制御を調べたいとき。
- complete prompt の共通組み立て規則、Structured markdown 描画、path placeholder 解決、ファイルアクセス規則本文生成などの汎用処理だけを調べたいとき。
- oracle file 本体の仕様内容、レビュー基準本文、INDEX.md エントリーの品質基準、TUI 画面制御、または特定 realization file の実装内容そのものを確認したいとき。

## hash
- 32589477c587efce779198231df8be862dc9ea0ddc1903d6529d9a17a13cf9a5

# `other`

## Summary
- cmoc の設定モデル、パスモデル、規範文書生成、構造化 Markdown レンダリングに関する正本由来の補助実装群を扱う。
- リポジトリ別設定、ルートパスプレースホルダ、規範フォーマット、構造化文章の出力変換など、複数の基礎モデルへ進む入口になる。

## Read this when
- cmoc の設定項目、既定値、永続化形式、またはサブコマンド別の設定値を確認したいとき。
- cmoc 内のパス表記、ルートプレースホルダ、実パス解決、プレースホルダ表記への変換を確認したいとき。
- 規範文書の構造化、要求ラベル、入力検証、構造化文書への変換を確認したいとき。
- 階層構造を持つ自然言語文章を Markdown 見出し・本文・コードブロックへレンダリングする処理を確認したいとき。

## Do not read this when
- 個別サブコマンドの処理手順、入出力仕様、状態管理そのものを確認したいとき。
- 設定の読み書き処理、JSON 変換処理、CLI コマンド実装の詳細を確認したいとき。
- 正本仕様断片と実装成果物の責務境界など、設定・パス・規範生成・Markdown レンダリング以外の開発ルールを確認したいとき。
- 既存 Markdown の解析 parser や汎用 Markdown 処理を探しているとき。

## hash
- 6dfafbfed1f6ecf5d7abdbca6784b9c309101e8119593a761ff0adcbed99f3c1

# `prompt_builder`

## Summary
- agent call に渡すプロンプトを構築する領域。完全なプロンプトの組み立て、静的・動的パーツの配置、プレースホルダ定義の合成、oracle/realization/review/index entry/file access/routing rule などの標準プロンプト片の注入を扱う。
- 配下には、プレースホルダ対応表の基礎型、完全プロンプト構築の入口、標準プロンプト部品群が含まれる。

## Read this when
- agent call 用の完全なプロンプトがどの順序で組み立てられるか、静的プロンプトと動的プロンプトがどう分けられるかを確認・変更したいとき。
- oracle standard、realization standard、review standard、index entry standard、file access rule、routing rule などの標準プロンプト片が、どのフラグや依存関係で注入されるかを確認・変更したいとき。
- プロンプト内のプレースホルダ対応表の型、プレースホルダ定義の合成、または置換先として扱える値の範囲を確認したいとき。
- AI エージェント向け規範プロンプトの文面や、INDEX.md エントリー作成・レビュー・読み書き規則に関するプロンプト部品を調整したいとき。

## Do not read this when
- agent call の実行、送信、結果処理、永続状態、CLI 入出力など、プロンプトを利用する側の制御を調べたいとき。
- 個別サブコマンドの実行経路、path model、実際のファイルシステム権限、sandbox 制御を調べたいとき。
- 具体的なプレースホルダ置換処理や文字列展開処理そのものを確認したいとき。
- oracle file や realization file の定義済み規範を読むだけで、プロンプト部品としての組み立て箇所を確認する必要がないとき。

## hash
- 846358bc4bf7afe93b8f24cdbe95b2bc6e1cccdf3ec121a3a47df82e78ff33a0

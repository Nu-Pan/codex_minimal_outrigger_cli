# `oracle`

## Summary
- cmoc の oracle src 全体への入口。AI 呼び出し仕様、プロンプト構築、設定・パス・構造化文書など、プログラミング言語で書かれた正本仕様断片の下位領域を扱う。
- agent call のパラメータ・Structured Output schema、共通プロンプト部品、リポジトリ設定、パスプレースホルダ、規範文書モデル、Markdown レンダリング helper の正本定義へ進むための分岐点。
- CLI 実行制御や realization 側実装ではなく、AI に渡す情報、共通規範、設定・パス・文書構造の正本値を確認するための領域。

## Read this when
- cmoc の oracle src にある実装形式の正本仕様断片から、どの下位領域を読むべきか切り分けたいとき。
- AI エージェント呼び出しの基本パラメータ、個別機能の prompt、応答 JSON、Structured Output schema の正本定義を探すとき。
- agent call 用プロンプトの構成順、共通規範の注入、ファイルアクセス制限、ルーティング規則、プレースホルダ定義の扱いを確認したいとき。
- リポジトリ別設定、モデル・推論努力対応、並列数やリカバリ回数、パスプレースホルダ、規範文書モデル、構造化 Markdown レンダリングの正本定義を探すとき。

## Do not read this when
- 自然言語で書かれた oracle doc や、oracle test にあるテスト形式の正本仕様断片を確認したいとき。
- CLI サブコマンドの実行制御、branch 操作、diff 取得、保存処理、表示整形、対象ファイル探索など realization 側の実装詳細を調べたいとき。
- oracle standard、realization standard、apply review standard、index entry standard などの規範本文だけを確認したいときは、該当するプロンプト部品や文書を直接読む方が適切。
- バックエンド固有のプロセス起動、モデル名変換、結果処理、エラー処理、生成済み設定ファイルの読み書きなど、正本仕様断片ではなく具体的な実装経路を追いたいとき。

## hash
- a72554c39a3ec3558594094fb2a315f5d34768078c7bf66276f327b896f8357a

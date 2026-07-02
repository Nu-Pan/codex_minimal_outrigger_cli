# `oracle`

## Summary
- cmoc の正本実装断片のうち、AI エージェント呼び出しパラメータ、完全プロンプト構築、設定・パス表記・規範文書・Markdown 整形などの基礎モデルを束ねる領域。
- サブコマンド別の agent call parameter、Structured Output schema、prompt 注入規則、ルートプレースホルダ付きパス、設定境界、構造化文書モデルへ進むための入口になる。

## Read this when
- cmoc が AI エージェントへ渡す prompt、role、goal、モデル設定、reasoning effort、ファイルアクセス方針、Structured Output schema の正本仕様断片を探すとき。
- agent call 用の完全なプロンプトが、標準プロンプト、補助プロンプト、ファイルアクセス規則、ルーティング規則、プレースホルダ定義からどう組み立てられるかを確認したいとき。
- cmoc の設定項目、既定値、リポジトリ別挙動設定、設定ファイルの永続化境界を確認したいとき。
- <cmoc-root>、<repo-root>、<run-root>、<work-root> などのルート概念、プレースホルダ付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を構造化して保持するモデルや、階層化された文章を Markdown へ整形する helper の正本実装断片を確認したいとき。

## Do not read this when
- CLI 引数解析、git 操作、branch 操作、実行フロー、保存処理、結果集約、表示処理など、正本実装断片を利用する realization implementation 側の制御を調べたいとき。
- oracle file、realization file、index entry、各 standard の定義本文や品質基準そのものを確認したいだけのとき。
- 設定の読み書き処理、JSON 変換処理、状態ファイル操作、レビュー所見の生成・検証ロジック自体を探しているとき。
- 生成済みプロンプトをどこで agent call へ渡すか、または realization implementation や realization test の現在構造を追いたいとき。
- 特定の下位領域が対象だと分かっており、用途別 agent call parameter、プロンプト構築、または基礎補助モデルへ直接進めるとき。

## hash
- 1ffd1dde8f1fee4e9db889c38ded5a0c4d37d57b6fa3a4e7109bbf18253514ef

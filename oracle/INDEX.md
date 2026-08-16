# `doc`

## Summary
- cmoc の正本文書群を分野別に案内する入口。アプリケーション挙動、branch・commit・worktree のモデル、採用しなかった代替案、開発ルールを扱い、個別の調査や変更では該当する下位文書へ進むために読む。
- 現行仕様、設計・実装配置、開発環境、テスト要件・実行手順、または不採用案の背景を確認する際の領域横断的なルーティング起点。ただし各文書の詳細な契約や手順は下位文書に委譲する。

## Read this when
- cmoc の正本文書を調査・実装・レビューする際に、対象分野に対応する文書群の入口を選ぶとき
- アプリケーション挙動、branch・commit・worktree、開発ルール、テスト、開発環境、または採用しなかった代替案の背景を確認するとき
- 仕様、設計、実装、テスト、環境構築のどの正本文書へ進むべきか判断するとき

## Do not read this when
- 対象となる個別の仕様・設計規約・開発環境文書・テスト文書が既に特定できており、その本文を直接読む方が適切なとき
- 具体的な CLI 挙動や実装配置、テスト実行手順など、下位文書が直接の確認先となるとき
- INDEX.md の生成規約や、対象文書に含まれない一般的な開発情報だけを確認するとき

## hash
- c86afb8faf011430f8c4943924ad416b3e469745de41b2289d99c6673877fe25

# `src`

## Summary
- cmoc の agent call 構築、完全 prompt の組み立て、共通モデル、パス解決、構造化 Markdown、設定、feedback 入力契約を扱う oracle 定義群の入口です。
- agent call のパラメータ、処理別の起動定義、レビューや適用などの作業別構成を調べるときは acp_builder へ進みます。
- prompt の統合、アクセス制御、各種 policy、エディタ入力を調べるときは prompt_builder へ進みます。
- 設定値、root placeholder と worktree のパス解決、構造化文書の変換を調べるときは other へ進みます。
- feedback reporter が受け取る問題入力の分類・根拠・継続状態の契約を調べるときは feedback へ進みます。

## Read this when
- cmoc の agent call 構築責務と、モデル・推論強度・ファイルアクセス・cwd の共通定義を確認するとき
- 完全 prompt の構成、policy の組み込み、placeholder の統合、Structured Document の Markdown 変換を確認するとき
- repository root、work root、run root などの call-scoped なパス解決規則を確認するとき
- feedback reporter へ渡す問題入力の形式と、人間対応が必要な問題の根拠項目を確認するとき

## Do not read this when
- agent call の実行制御、終了結果の処理、または個別 CLI サブコマンドの実装だけを調査するとき
- 特定の作業に固有の prompt、policy、Structured Output schema を直接確認したいとき
- 実際のリポジトリ設定値や、人間が行った設定調整の結果だけを確認したいとき

## hash
- 29777675f1eda92f9bc53995782f25af0680897d3e7bc139c3c50a3c1c713d41

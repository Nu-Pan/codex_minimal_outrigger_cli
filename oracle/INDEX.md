# `doc`

## Summary
- cmoc のアプリケーション仕様を定義する oracle 文書群への入口。CLI 補完、Codex／Ollama 実行、ログ、doctor preprocess、prompt、run・session lifecycle、サブコマンドなどの個別仕様を扱う。
- branch・commit・worktree の用語と関係、session／run の分岐、run 用 linked worktree などの正本仕様への入口。
- cmoc realization refactor で採用しなかった作業方式・検査方式・状態管理方式の検討記録への入口。
- Python コーディング、CLI 設計・配置、開発環境、pytest によるテスト方針をまとめた開発規約への入口。

## Read this when
- cmoc の利用者向け機能やサブコマンドの正本仕様を調査・実装・検証するとき。
- 複数のアプリケーション仕様にまたがる実行順序、状態管理、出力、エラー処理の関係を確認するとき。
- 対象機能に対応する個別仕様文書を特定したいとき。
- session fork、run の隔離、branch／commit／worktree の命名・責務・ライフサイクルを確認するとき。
- run report、差分検査、apply、session join などで基準 commit や merge 先を確認するとき。
- cmoc realization refactor の作業フローや調査・修正単位の設計理由を確認するとき。
- 事前計画方式、並列所見調査、事後差分検査、gitignore 連携、AI-generated memory などの採否理由を調べるとき。
- Python 実装規約、CLI のエントリーポイントや責務配置、Python／venv、依存関係、pytest の実装・実行方針を確認するとき。

## Do not read this when
- 開発環境、設計ルール、テストルールなど開発手順だけを確認したい場合は、対応する開発規約文書を直接読む。
- 個別仕様が明確で、対象文書を直接読む方が適切な場合。
- 対象機能に対応する realization code や realization test の内部実装だけを調査する場合。
- 現在の realization refactor state、investigation_required、file access rule、差分検査、agent 呼び出し経路の現行仕様を確認・変更する場合。
- 具体的な realization file の修正方法や実装責務を調べる場合。
- 採用済みの現行仕様や実装の直接の参照先を探している場合は、検討記録ではなく対応する現行文書や実装を読む。
- oracle の一般原則や INDEX.md の読み方・ルーティング方針自体を確認したい場合。

## hash
- b46bb3f10c022bed6cc4b09d2df4a14ba2c12c7ff8426f6e8205ba2bad0df703

# `src`

## Summary
- oracle/src/oracle 配下の正本ソースをまとめるディレクトリ。ACP 呼び出しパラメータ、TUI・レビュー・refactor/apply 処理、設定・パスモデル・構造化文書、完全プロンプトと標準ルール部品を扱う。各サブディレクトリの個別実装へ進む前の入口。

## Read this when
- cmoc の ACP 呼び出し条件、モデル・推論設定、ファイルアクセスモードを調査するとき。
- 設定値、リポジトリや作業ルートの解決、構造化文書の Markdown 化を調査するとき。
- 完全なエージェントプロンプトの構築や、oracle・realization・レビュー・ルーティング標準の組み込みを調査するとき。
- indexing、oracle review、TUI、session join、realization refactor/apply の正本プロンプトを探索するとき。

## Do not read this when
- 具体的な CLI の入出力処理や realization 実装そのものだけを調査するとき。
- 個別の prompt builder 部品、レビュー schema、設定クラス、パス操作の詳細だけを確認したいときは、該当する配下ファイルを直接読む。

## hash
- 56193f22c9ecb0f8836c1162c1e22b0c5c1d8cee1afdfeafdb2276cfeb2687c3

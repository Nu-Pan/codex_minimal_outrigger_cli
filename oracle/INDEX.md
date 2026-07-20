# `doc`

## Summary
- cmoc のアプリケーション仕様と開発規約をまとめた oracle 文書群への入口。CLI の利用者向け挙動、状態管理、ログ、プロンプト、run/session lifecycle、branch model、Python 実装、設計、開発環境、テスト方針を扱う。採用しなかった設計案の検討記録にも進める。

## Read this when
- cmoc の共通仕様、CLI 呼び出し、状態管理、ログ、プロンプト、run/session lifecycle を実装・検証するとき
- session fork、run の隔離、branch・commit・worktree の関係や基準 commit を確認するとき
- Python の実装規約、CLI の責務配置、開発環境、pytest によるテスト方針を確認するとき
- realization refactor の作業方式や不採用案の理由を調査するとき

## Do not read this when
- 特定の realization code または realization test の内部実装だけを調査するとき
- 個別機能の具体的な挙動・出力仕様を確認するときは、app_spec 配下の対応する文書を直接読むとき
- 一般的な INDEX.md の読み方やルーティング方針を確認するとき

## hash
- 8ff6bbffa83a828e6c2c92603b5597c6e4a398744360d0175962a12753c56184

# `src`

## Summary
- cmoc の正本ソースを格納するディレクトリ。ACP builder の呼び出しパラメータ、TUI、oracle review、realization 操作、session 処理を扱う。
- 設定・ルートパスモデル・構造化文書・標準ルールを定義し、構造化 Markdown と完全なエージェントプロンプトを生成する。
- 配下の `acp_builder`、`prompt_builder`、`other` が、それぞれ ACP 呼び出し定義、プロンプト構築、共通モデル・設定・文書化処理への入口となる。

## Read this when
- ACP builder の呼び出しパラメータ、レビュー処理、TUI 起動、oracle・realization 操作を調査・変更するとき。
- cmoc の設定、モデルやアクセスモード、ルート探索、プレースホルダ変換を確認するとき。
- 標準ルールの構造化、プロンプト部品の組み立て、完全なプロンプト生成、Markdown レンダリングを調査・変更するとき。
- oracle/src 配下で該当する責務の実装ファイルを特定し、下位ディレクトリへ進む必要があるとき。

## Do not read this when
- 具体的な CLI 実行経路や設定読み書きなど、realization 側の利用処理を確認したい場合。
- 個別の標準文書、単一のプロンプト部品、特定の ACP 呼び出しパラメータだけを調べたい場合は、対応する下位ファイルを直接読む。
- oracle/src 以外の oracle 文書やテストの正本仕様だけを確認したい場合。

## hash
- 4577217c5a3a3fac35059cd7c355d14134c3b3fdcb4e2952fef57da38d49b3e4

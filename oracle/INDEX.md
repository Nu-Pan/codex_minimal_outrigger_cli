# `doc`

## Summary
- cmoc の主要なアプリケーション仕様をまとめた oracle 文書ディレクトリ。CLI の共通挙動、branch・session・run の lifecycle、開発ルール、不採用案の検討記録への入口を提供する。

## Read this when
- cmoc の CLI 挙動、共通規約、session・run・branch・worktree の仕様を確認するとき
- Python 実装、CLI 配置、開発環境、realization test のルールを確認するとき
- realization refactor における採用・不採用の設計判断を調べるとき
- 複数の oracle 文書にまたがる仕様の入口や、詳細文書の所在を特定するとき

## Do not read this when
- 特定の仕様文書の詳細だけを確認したいときは、その文書へ直接進む
- 個別モジュールの実装詳細やテスト実装を確認したいときは、対応する realization code または realization test を読む
- 一般的な利用方法だけを確認したいときは、利用者向け文書を優先する

## hash
- 30c57196877a9510c5a30dc81def3558d97755b842bbb17eca515e228ff9f744

# `src`

## Summary
- cmoc の正本ソース群への入口。AI エージェント呼び出しパラメータと実行作業単位、設定・パス解決・構造化文書・規範表現、エージェントプロンプトの組み立てを扱う。
- 下位では、エージェント呼び出し関連を acp_builder、共通モデルと構造化文書を other、プロンプト部品と完全なプロンプト生成を prompt_builder が担当する。

## Read this when
- 正本ソースの責務分担や下位モジュールへの入口を確認するとき
- AI エージェント呼び出しの抽象パラメータ、設定・パス表現、構造化 Markdown、プロンプト構成を調べるとき

## Do not read this when
- 個別のプロンプト規範や ModelClass、ReasoningEffort、StructDoc の定義元を直接確認したいとき
- CLI の実行フローや設定ファイルの生成・同期処理を調べるとき

## hash
- b191ce07b20539bc25977f115e5998bec913eafe1199653f2ec755a640ddf4fd

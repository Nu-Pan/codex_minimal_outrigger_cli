# `doc`

## Summary
- cmoc の正本仕様ドキュメントを収録するディレクトリ。アプリケーション仕様、branch・commit・worktree のモデル、開発ルール、不採用案の検討記録など、実装やテストの判断根拠となる文書への入口。

## Read this when
- cmoc の利用者向け挙動や CLI、Codex 連携、run・session lifecycle の正本仕様を調査するとき
- branch・commit・worktree の関係や session・run の分岐モデルを確認するとき
- Python 実装、CLI 配置、開発環境、realization test の共通ルールを確認するとき
- realization refactor で採用しなかった方式の背景や不採用理由を確認するとき

## Do not read this when
- 具体的な実装やテストの詳細だけを確認したいときは、対応する realization file を直接読む
- 対象が特定の oracle 文書に限定され、該当文書を直接特定できるとき
- INDEX.md の読み方やリポジトリ共通のルーティング方針だけを確認したいとき

## hash
- 957b4769611d19d1d13f77222cafd821b9598f8ea96bfcf1605d216edccee32b

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

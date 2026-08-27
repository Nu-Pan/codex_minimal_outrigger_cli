# `doc`

## Summary
- cmoc の正本ドキュメント群を機能・設計・開発ルールごとに参照する入口。アプリケーション仕様、session／run の branch model、不採用案、Python 開発ルールへの導線を提供する。
- 各下位文書の責務境界と、実装・テスト・CLI 契約・環境構築など個別の確認先を示す。

## Read this when
- cmoc の仕様・設計・開発ルールを横断して、最初に読むべき正本文書を探すとき。
- CLI やアプリケーション挙動、session／run の git 隔離モデル、Python 実装規則、テスト要件・実行手順の参照先を判断するとき。
- 現行設計で採用されなかった代替案と、その不採用理由を調査するとき。

## Do not read this when
- 確認対象の機能、設計要素、開発規則に対応する下位文書が明確で、その文書を直接読むべきとき。
- 具体的な CLI 入出力契約、実装コード、テストコード、外部契約、環境操作手順など、正本文書群の概観を必要としないとき。
- 採用済み workflow の具体的な操作方法や現在の実行結果だけを確認したいときは、該当する仕様・実装・テスト文書へ直接進むとき。

## hash
- 918be1efa91d612e344dfe3027b1018ad6a7e51d4d1fe695a8f0147231889227

# `src`

## Summary
- cmoc の oracle 関連実装を集約するソースルート。agent call のパラメータ構築、prompt と各種 policy、oracle／realization／feedback／indexing／session／TUI 向けの起動定義、共通設定・パス解決・構造化文書レンダリングを扱う。
- 配下の `oracle` パッケージが、これらの機能別実装と Structured Output schema への入口になる。

## Read this when
- oracle 関連 agent call の prompt、モデル・推論設定、ファイルアクセス、cwd、indexing preflight、Structured Output schema の定義を調査または変更するとき。
- oracle、realization、feedback、indexing、session、TUI、quota probe の起動パラメータ構築を確認するとき。
- 共通 prompt の組み立て、oracle／realization policy、placeholder、設定値、パス解決、構造化 Markdown レンダリングの実装箇所を確認するとき。

## Do not read this when
- Codex CLI の実行処理やサブコマンドの外部インターフェースそのものを確認したいとき。
- oracle 文書や realization 文書の正本仕様、または個別の oracle／realization ファイルの内容を確認したいとき。
- feedback issue の検出・保存・集約や、既存 INDEX.md のルーティング内容だけを確認したいとき。

## hash
- 4f08936a9e83290b0b20960b8f32b944dcfe9b9d086b473ee8de47481f5adfb2

# `doc`

## Summary
- cmoc の正本ドキュメントをまとめたディレクトリ。アプリケーション挙動、branch・commit・worktree のモデル、採用しなかった設計案、Python 開発規則を扱い、各仕様領域の文書へ進むための入口となる。

## Read this when
- cmoc の挙動仕様や共通実行規約の参照先を特定するとき
- session・run の分岐、branch、commit、worktree の関係を確認するとき
- realization refactor で採用しなかった方式の背景や理由を調べるとき
- Python の実装、CLI 設計、開発環境、テスト規則・実行手順を確認するとき

## Do not read this when
- 対象が特定のアプリケーション機能、開発規則、または branch model に限定され、対応する個別文書を直接読む方が適切なとき
- 実装やテストの具体的なソース内容だけを確認するとき
- 現行仕様ではなく、不採用案の検討理由も不要な単純な作業を行うとき

## hash
- fb3da5bbd16011cbc444eb2988d1727ef6399539dcbcaa9941596408b67293fc

# `src`

## Summary
- cmoc の AI Agent 呼び出しを構成する正本ソース群です。Agent Call パラメータ、用途別の呼び出し設定、prompt builder、Structured Output schema、feedback 契約、パス・設定・構造化 Markdown の基盤を扱います。
- 用途別の Agent call 設定、prompt 構築、基礎モデル、oracle review・realization・session・TUI・indexing・feedback の定義へ進むための入口です。

## Read this when
- AI Agent 呼び出しのモデル種別、推論強度、ファイルアクセスモード、作業ディレクトリ、indexing preflight などの共通パラメータを確認するとき。
- oracle review、realization、session、TUI、indexing、feedback などの特定フローの呼び出し設定や Structured Output schema を調査・変更するとき。
- prompt の組み立て、静的・動的 prompt、placeholder、oracle／realization 規則、feedback reporting 規則を確認するとき。
- cmoc の設定モデル、パスコンテキスト、Standard、構造化 Markdown、Agent Call の基礎モデルを確認するとき。

## Do not read this when
- 通常の CLI／TUI 実行フローや realization 実装・テストの挙動を調査するときは、呼び出し側または realization 側を直接読む。
- oracle の正本仕様や Codex CLI の一般的な sandbox・permission 規則を確認するときは、対応する仕様文書を直接読む。
- 特定用途の prompt 本文や schema の詳細だけを確認したいときは、該当する下位領域へ直接進む。
- feedback の collector による保存・集約・重複判定だけを確認したいときは、collector 側の実装を直接読む。

## hash
- 3f3fb949de4b7a4f52d2963f9f65ac136e990d18daafdd45f2443945cf9e6f41

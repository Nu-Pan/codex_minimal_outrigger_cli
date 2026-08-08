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
- `oracle/src` は、AI Agent 呼び出しに必要な正本ソースを収録する領域です。共通パラメータ、用途別設定、prompt 構築、Structured Output 契約、基礎モデルを扱い、下位要素の定義へ進む入口になります。

## Read this when
- AI Agent 呼び出しのモデル、推論設定、ファイルアクセス、cwd、Structured Output schema を調査・変更するとき。
- feedback、indexing、TUI など用途別の agent call 設定や prompt 構築部品の所在を確認するとき。
- CmocConfig、call-scoped なパス解決、Standard、Requirement、構造化 Markdown の基盤定義を調査するとき。

## Do not read this when
- 通常の realization 実装・テストや、CLI・TUI の実行フロー自体を調査するとき。
- 特定の prompt builder 部品、用途別 schema、個別モデルの詳細だけを確認したいときは、該当する下位要素へ直接進む。

## hash
- 5a7d4b04247230ccef52fddbf8177d285c20a2196e5cf068a099921493697562

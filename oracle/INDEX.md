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
- cmoc の Agent call に渡すパラメータ、Structured Output schema、用途別 prompt、共通 prompt 部品、oracle／realization／feedback／INDEX の各規範を定義する正本ソース領域。Agent call 構築、prompt の共通化、出力契約、対象領域ごとの下位実装を確認する入口となる。

## Read this when
- Agent call のモデルクラス、推論強度、ファイルアクセス、作業ディレクトリ、Structured Output の設定を調査・変更するとき。
- 特定用途の prompt 構築、TUI 起動、feedback 処理、レビュー処理、indexing 処理の正本実装を確認するとき。
- prompt に注入される oracle／realization の規範、ファイルアクセス規則、ルーティング規則、共通構造化文書の生成を調査するとき。

## Do not read this when
- 通常の realization 実装やテスト、CLI／TUI の実行処理そのものを調査するとき。
- 正本仕様の本文だけを確認したい場合は oracle/doc を直接読む。
- 特定用途の詳細だけが必要な場合は、この領域全体ではなく該当する下位ディレクトリの実装や schema を直接読む。

## hash
- aea66956da08bbe87b23f04952d65365530416dca9a4a5060fe613f80ac9fc7d

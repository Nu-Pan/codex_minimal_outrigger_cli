# `doc`

## Summary
- cmoc の正本文書を領域別に案内する上位入口。アプリケーション挙動、branch・commit・worktree、採用しなかった代替案、開発ルールを扱う下位文書群へのルーティングを提供する。

## Read this when
- cmoc の仕様・設計・開発ルールに関する正本文書を探すとき
- CLI の挙動、session・run の分岐、採用しなかった設計案、Python 開発やテスト手順のいずれかを調査・変更・レビューするとき

## Do not read this when
- 対象となる下位文書が明確で、その本文だけを直接確認すれば足りるとき
- 具体的な CLI 実装、個別のテスト、または個別の oracle・realization の内容だけを調べるとき

## hash
- d047f74262b69e21b1e96d6268734595af827083fa1fab429e39a3e75b125a7d

# `src`

## Summary
- AI コーディングエージェント呼び出しの構築定義を集約する領域。共通の呼び出しパラメータ、モデル・推論設定、ファイルアクセス、パスコンテキスト、Structured Output を基盤として、prompt の構成規則と用途別の agent call 定義を提供する。
- agent call の用途別定義は、セッション競合解消、TUI、oracle 調査・編集・レビュー、feedback 検証、realization の apply・refactor、indexing などに分かれる。対象の呼び出し条件や起動設定を調べる際の上位入口として機能する。
- prompt_builder 配下では完全 prompt の組み立て、プレースホルダ展開、oracle・realization・アクセス権限・routing・feedback などのポリシーを扱い、other 配下では設定、パス解決、構造化 Markdown の共通基盤を扱う。feedback 配下には reporter 入力契約も含まれる。

## Read this when
- agent call の共通パラメータ契約、モデルクラス、推論強度、ファイルアクセスモード、作業ディレクトリ、Structured Output の構築方法を確認するとき
- 特定用途の agent call 定義を探し、oracle、realization、feedback、session、TUI、indexing の下位領域へ進む入口を判断するとき
- 完全 prompt の生成順序、プレースホルダ、ポリシー統合、oracle・realization の扱い、routing や feedback reporting の規則を調査するとき
- cmoc の設定モデル、パス表現・root 解決、構造化 Markdown の共通実装を確認するとき

## Do not read this when
- 実際の agent call の実行制御、CLI サブコマンドの業務フロー、Git 操作そのものを調査するとき
- 個別の oracle file や realization file の正本仕様、実装内容、テスト内容を確認するときは、対応する対象を直接読む
- agent call 構築と無関係な一般 CLI 機能や、collector 側の feedback 保存・集約処理だけを調査するとき

## hash
- b8e2e117062fddd45308530df0f7afed72740878e99e4b7ce9fc0ce12086cba9

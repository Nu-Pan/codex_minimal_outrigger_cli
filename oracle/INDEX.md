# `doc`

## Summary
- cmoc のアプリケーション仕様、開発規約、branch・commit・worktree model、設計上の代替案を扱う正本文書群への入口。機能仕様と開発・運用上の共通判断を、担当文書ごとに切り分けて参照するための文書群。

## Read this when
- cmoc の仕様調査で、アプリケーション機能、開発規約、session・run の branch model、または過去の設計判断のどの文書から確認を始めるか判断するとき。
- 現行仕様の責務分担、実装・テスト規約、run の分離と統合、採用・不採用となった設計案の背景を確認するとき。

## Do not read this when
- 単一機能の詳細な実行手順、入力 schema、実装挙動、テスト固有要件だけを確認したいときは、対応する個別の正本仕様や実装を直接読む。
- INDEX.md の自動生成規則、oracle・feedback・ログなど個別領域の正式な定義だけを確認したいときは、該当する正本仕様を直接読む。
- ファイル列挙やハッシュ計算など、文書の意味や責務分担を必要としない機械的処理だけを行うとき。

## hash
- 8ef4acfec44388ae113e9bf3d2ff76eb468f6785e10b83792f66da167868e7ad

# `src`

## Summary
- oracle 機能を構成する実装・設定・入力契約の定義群への入口。agent call の構築、prompt と policy の組み立て、パスや構造化文書の共通処理、feedback・indexing・editor input の schema を扱う。
- 用途別の agent call builder と、oracle／realization の調査・編集・レビュー・反映、session・TUI・feedback に関する呼び出し定義へ進むための上位入口。

## Read this when
- oracle 機能の agent call、prompt、アクセス制御、起動設定、用途別 policy、または Structured Output 入力契約を確認・変更するとき。
- oracle／realization の操作経路、INDEX エントリー生成、feedback 報告、editor input handoff、共通のパス・設定・構造化文書処理の実装箇所を探すとき。

## Do not read this when
- oracle や realization の正本仕様、個別 prompt policy の意味仕様、または生成済み oracle・realization file の内容を確認したいとき。
- agent call の実行処理、CLI・TUI の実行結果、Git 操作、設定の永続化など、ここで定義される構築要素を利用する処理だけを調べたいとき。
- 特定の Structured Output schema の必須項目や受理条件だけを確認したいときは、該当する schema を直接読むとき。

## hash
- 9e5021ab4cd9ba7996bb911f04c65f9ceb6a05fa67da4af2d181ce16f1e39ec7

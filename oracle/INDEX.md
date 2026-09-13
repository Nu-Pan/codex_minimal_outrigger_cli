# `doc`

## Summary
- cmoc の正本仕様、開発規約、branch model、設計上の代替案をまとめた文書群への入口。アプリケーション横断機能の仕様、session／run と Git の関係、Python・CLI・テストの開発規約、過去の設計判断を目的に応じて案内する。

## Read this when
- cmoc のアプリケーション機能や複数機能にまたがる実行条件・状態管理・出力契約の正本仕様を確認するとき
- session／run の fork・join、branch・commit・worktree の役割や関係を扱うとき
- Python 実装、CLI 構成、開発環境、依存関係、pytest・Ruff・mypy・統合テストの規約を確認するとき
- 権限管理、feedback・oracle、realization refactor、作業計画などの設計判断について、代替案と採否理由を確認するとき

## Do not read this when
- 個別機能の詳細要求、run state や report の状態遷移、oracle の変更手順、テスト固有の意味要件を直接確認したいときは、該当する正本仕様や規約の対象を読む
- 実装モジュールの具体的な構成・内部 API、実際の不具合や記録内容を調査するときは、対応する realization・oracle source・実装・記録を直接読む
- 一般的な workflow、個別の Git 操作手順、cmoc と無関係な設計判断だけを確認したいとき

## hash
- 94ee87634d44cfa251bfca47da5b9dd579668335f84f608a421368d8a62b860c

# `src`

## Summary
- oracle の agent call 構築、prompt 構築、入力受け渡し、feedback 処理、realization・session・TUI・indexing 向けの機能群をまとめる実装ルート。
- agent call のパラメータ、ファイルアクセスモード、quota probe、共通 prompt と policy の組み立てを確認する入口。
- agent call 間で共有する Git worktree・root placeholder、cmoc 設定、構造化文書モデルなどの共通基盤を提供する。
- oracle 編集・調査・レビュー、realization 適用・リファクタリング、session join、feedback、INDEX エントリー生成の個別処理へ進む上位入口。

## Read this when
- oracle 層の agent call 構成や prompt・policy の組み合わせを横断して調べるとき。
- agent call の cwd、worktree root、placeholder、設定値、または構造化文書の扱いを確認するとき。
- oracle、realization、feedback、session join、TUI、quota probe、indexing のどの下位機能から調査を始めるべきか判断するとき。
- editor input handoff や Structured Output を含む呼び出しの共通構築経路を確認するとき。

## Do not read this when
- 特定の agent call の prompt、schema、結果処理、または個別 workflow の詳細だけを確認したいときは、対応する下位ディレクトリや builder を直接読む。
- Codex CLI の実行そのもの、設定ファイルの永続化処理、Git 操作、TUI の画面処理など、oracle の共通モデルを利用する下流処理だけを調べたいとき。
- 実際の oracle file・realization file・feedback 入力の内容や、正本仕様・既存 INDEX エントリーそのものを確認したいとき。

## hash
- 21671c2a92b27891900b46015901b439b6d063ae05786891b33314756b3c60b5

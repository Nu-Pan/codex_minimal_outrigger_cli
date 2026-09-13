# `doc`

## Summary
- cmoc のアプリケーション仕様、開発規約、branch・session・run のモデル、設計上の代替案をまとめた正本文書群への入口。各仕様領域の責務と参照境界を把握し、実装・変更・レビューで読むべき下位文書を選ぶための階層。

## Read this when
- cmoc のアプリケーション仕様全体、開発規約、branch・commit・worktree の関係、または過去の設計判断を横断して確認したいとき。
- CLI 実行、session・run lifecycle、feedback、ログ、通知、自動補完、テスト、環境構築など複数の仕様領域にまたがる作業の参照先を判断するとき。
- 現行仕様へ進む前に、関連する用語、責務分担、採用・不採用の設計背景を把握したいとき。

## Do not read this when
- 特定機能の詳細要求、field・型・prompt・schema、処理手順、実装 API、個別のテスト規則を確認したいときは、該当する下位仕様や正本実装を直接読む。
- 特定の不具合、ログ、feedback、oracle、成果物の内容を調査するときは、該当する実装や記録を直接読む。
- INDEX.md の生成手順、一般的な開発環境、または cmoc と無関係な設計・運用だけを確認したいとき。

## hash
- d68ff989029e810c3ec2ff7698297c5052c2a4de763bcf376394b5f93d4116a0

# `src`

## Summary
- cmoc の agent 呼び出しを構築する実装群のルート。共通の呼び出しパラメータ、アクセスモード、作業パス、設定、構造化文書、prompt 組み立てを扱う。
- 用途別の agent call builder、prompt policy、oracle・realization・feedback・indexing・session・TUI・editor input 関連の下位実装へ進むための入口。

## Read this when
- agent 呼び出しの設定、cwd や作業パスの決定、ファイルアクセスモード、Structured Output の指定を横断して確認するとき。
- 完全な prompt の構成、policy の組み込み、placeholder の統合、構造化 Markdown の生成経路を調べるとき。
- 特定用途の agent call builder や oracle・realization・feedback・indexing などの関連実装へ進む起点を判断するとき。

## Do not read this when
- 特定用途の起動条件、prompt、出力契約だけを調べる場合は、該当する下位 builder や schema を直接読む。
- 共通設定、パス解決、構造化文書の個別仕様だけを確認する場合は、対応する共通実装を直接読む。
- agent call の実行処理、各用途の意味仕様、oracle・realization・feedback の正本や収集処理、INDEX エントリー生成規則だけを確認する場合は、それぞれの専用対象を直接読む。

## hash
- 1519bd56d565fdb65504cef34649b17da96be11a609e7b9829b568e9d508ada7

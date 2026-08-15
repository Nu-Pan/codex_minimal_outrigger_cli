# `doc`

## Summary
- cmoc の正本文書を領域別に案内するルート。アプリケーション挙動、branch・commit・worktree のモデル、不採用案の検討記録、開発ルールへの入口を提供する。

## Read this when
- cmoc の仕様・設計・開発ルールを横断して、読むべき下位文書の領域を選ぶとき
- CLI 挙動、session/run の分岐、refactor 方針、Python 実装・環境・テスト手順のいずれかを確認するとき

## Do not read this when
- 特定機能の実装詳細やテスト実行手順が明確な場合は、対応する下位の realization file、oracle src、または専用手順を直接読む
- INDEX.md の生成・更新仕様を確認する場合は、インデクシング仕様を直接読む

## hash
- e2e53ad1862929e3cd900085223f495084dfd85b21685085749abbfd80b7468b

# `src`

## Summary
- cmoc の agent call を構築する共通実装群。モデル、reasoning effort、ファイルアクセス、cwd などの呼び出しパラメータを定義し、用途別の agent call builder へつなぐ。
- prompt_builder では共通 prompt、routing、ファイルアクセス規則、oracle・realization 規範、Structured Output 前提の文面を組み立てる。
- other では agent call 用パス解決、構造化文書の Markdown 化、Standard の統合、cmoc 設定モデルを提供する。
- 下位には、feedback、oracle review・edit・investigation、realization の apply・refactor、session join、indexing、TUI など用途別の構築定義がある。用途を特定できる場合は、対応する下位ディレクトリへ進む。

## Read this when
- agent call の共通パラメータ、用途別 builder、実行条件を調査または変更するとき
- 共通 prompt、routing、ファイルアクセス規則、oracle・realization 規範、Structured Output 用文面を調査または変更するとき
- agent call の cwd、oracle・repository・run path、構造化文書、Standard、cmoc 設定の共通実装を調査または変更するとき
- 用途別の下位実装へ進む前に、共通の構築責務と依存関係を確認するとき

## Do not read this when
- 実際の agent call 実行処理や、個別 CLI 機能の業務ロジックを調査するとき
- 特定用途の prompt や Structured Output の詳細が明らかな場合は、対応する下位ディレクトリを直接読むとき
- 特定の oracle file、realization file、feedback collector の保存・集約処理を直接調査するとき

## hash
- e39bcb54e21668a12d33bc41695756a0303f8a034cdd14f3ffe4c3a4d543dca4

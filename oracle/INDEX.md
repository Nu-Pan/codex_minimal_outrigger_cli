# `doc`

## Summary
- cmoc の正本文書群を領域別に案内するドキュメント階層。アプリケーション仕様、branch・commit・worktree のモデル、不採用案の検討記録、開発ルールを扱い、具体的な仕様・設計・実装・テスト手順へ進むための入口となる。

## Read this when
- cmoc の正本文書を探しており、アプリケーション挙動、branch model、refactor の設計判断、Python 開発・CLI 設計・テスト・環境構築のいずれかを確認するとき
- 複数の仕様領域にまたがる責務境界や、適切な下位文書へのルーティングを確認するとき

## Do not read this when
- 特定の実装コード、テスト、realization file の具体的な挙動だけを調査するとき
- INDEX.md の自動生成方法や、個別文書が指定する下位仕様の内容だけを確認したいときは、対応する専用文書を直接読む

## hash
- ed3ca68f46d0fe38b3f312c5637cdc7eaf29ea7fc20e05eeec47ba06d32dbb52

# `src`

## Summary
- oracle 共通実装の設定、パス解決、agent call の prompt 構成、Structured Output、実行パラメータ、feedback reporter の入力契約を扱う領域。複数の oracle 機能にまたがる共通責務を確認し、該当する下位モジュールへ進むための入口。

## Read this when
- cmoc の oracle 共通実装における設定値、root placeholder、agent call のパスコンテキスト、標準定義、構造化 Markdown 文書生成を確認・変更するとき。
- agent call のモデル種別、推論強度、ファイルアクセス、作業ディレクトリ、Structured Output、起動条件、実行権限などの共通定義を調査するとき。
- feedback reporter から collector へ渡す入力形式や、問題を人間向け feedback として構造化・検証する処理を調査・変更するとき。
- agent call に渡す prompt の部品、統合順序、placeholder、エディタ入力初期化、oracle・realization・routing・file access・feedback の共通規則を調査・変更するとき。

## Do not read this when
- 特定の CLI 機能、realization、oracle file、realization file、issue 状態などの具体的な挙動を確認するとき。
- 実際の agent call 実行処理や Codex CLI sandbox の正本仕様を確認するとき。
- collector 側の feedback 保存・集約・重複判定、feedback の検出方法や継続判断だけを確認するとき。
- 共通 prompt builder やパス解決の一般実装、または個別 builder の実装だけを確認するとき。
- 永続化設定の同期、doctor、列挙型の定義、標準値の個別利用箇所だけを確認するとき。
- INDEX.md のルーティング情報だけを確認・変更するとき。

## hash
- c6e16de93db2b1703cdc0f6464adab7ddf2f3b7ac57489f1756a4b4c885e94d9

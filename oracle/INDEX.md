# `doc`

## Summary
- cmoc の正本ドキュメントを集約するディレクトリ。アプリケーション仕様、branch・commit・worktree のモデル、不採用案の検討記録、Python 開発ルールを扱い、各仕様文書へ進むための入口となる。

## Read this when
- cmoc のアプリケーション挙動、branch・worktree の関係、不採用設計の背景、Python 開発ルールの正本文書を特定するとき
- 複数の正本ドキュメントにまたがる責務境界や参照先を判断するとき

## Do not read this when
- 読むべき個別文書がすでに特定されており、その本文へ直接進めるとき
- 実装配置やテスト実行など、特定の開発ルール文書だけを確認すればよいとき
- INDEX.md のルーティング情報だけを確認するとき

## hash
- fa5811512be861b1792d08fadba76f188af336e1efc708f8132af83de01170fc

# `src`

## Summary
- AI コーディングエージェント呼び出しに使う oracle src の実装領域。共通の agent call パラメータ、prompt の構成・規範・Structured Doc、パスや設定の基盤、TUI・indexing・feedback・oracle review・realization・session join 用の個別 builder を扱う。用途別の実装を調査する際の入口。

## Read this when
- agent call の共通パラメータ、モデル・推論・ファイルアクセス設定を確認するとき。
- prompt の完全な組み立て、入力テンプレート、placeholder、oracle・realization・routing・feedback の共通規則を確認するとき。
- TUI、indexing、feedback、oracle review、realization、session join の prompt builder を探すとき。
- cmoc の設定、パス導出、Structured Doc の構造化・Markdown 化を確認するとき。

## Do not read this when
- 実際の cmoc サブコマンド実行や agent call 起動処理を確認するときは、呼び出し側・実行基盤を直接読む。
- 個別 builder の詳細な prompt 契約や Structured Output 定義を確認するときは、該当する下位ファイルを直接読む。
- collector 側の feedback 保存・集約や Git 操作の仕様を確認するときは、それぞれの担当領域を直接読む。

## hash
- f6a778a13fcec972aacf75aa5620b79ea60a6a6c48a79ae30e7d184780373cc0

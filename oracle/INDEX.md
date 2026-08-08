# `doc`

## Summary
- cmoc の正本ドキュメントを集約するディレクトリ。アプリケーション仕様、開発規則、不採用案の検討記録を扱い、それぞれの詳細文書へ進むための入口となる。

## Read this when
- cmoc のアプリケーション挙動や開発規則に関する正本文書の所在を確認するとき
- CLI、実装、テスト、開発環境など複数の仕様領域にまたがる調査・変更対象を特定するとき
- 採用しなかった設計案やリファクタ方針の背景を確認するとき

## Do not read this when
- 確認対象の個別仕様文書がすでに特定できており、その本文だけを読めばよいとき
- 実装コード、テストコード、開発成果物そのものを確認するとき
- INDEX.md のルーティング情報だけを確認するとき

## hash
- 4e0ff981deb0b9327b0f0e4fddc21c26074c20a8d2c00d1f4ee2689ec88392ac

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

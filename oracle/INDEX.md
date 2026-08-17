# `doc`

## Summary
- cmoc の正本文書を領域別に案内する入口。アプリケーション仕様、branch・commit・worktree のモデル、採用しなかった代替案、開発ルールを扱い、対象に応じて各下位文書へ進むためのルーティングを提供する。

## Read this when
- cmoc の正本仕様・設計資料・開発規約の入口を特定するとき
- アプリケーション挙動、branch model、設計上の代替案、Python・CLI・環境・テスト規約のいずれかを調査するとき
- 個別文書へ進む前に、対象領域の文書群を選びたいとき

## Do not read this when
- 対象の個別仕様や設計・テスト文書が既に特定できており、上位の文書群一覧を確認する必要がないとき
- 具体的な実装配置やCLI実装の責務だけを確認するとき
- テストの実行手順だけを確認するとき

## hash
- d3a45a15649b4ef42e8e396b06429e61af3b733a0a83bad0571cbe8c5f3ad94c

# `src`

## Summary
- oracle の実装本体です。agent call の共通パラメータ、モデル・アクセスモード、設定、root placeholder を含むパス解決、Structured Markdown の構築、完全 prompt と各種 policy の組み立てを扱います。
- `acp_builder` は feedback、indexing、oracle review、realization など用途別の agent call 起動パラメータを構築します。`prompt_builder` は共通 prompt と policy の構成要素を組み立てます。`other` は設定・パスモデル・構造化文書の共通基盤を提供します。

## Read this when
- oracle の agent call パラメータや prompt の実装を調査・変更するとき
- モデル、reasoning effort、ファイルアクセスモード、作業ディレクトリ、root placeholder の解決を調査・変更するとき
- feedback 検証、index entry 生成、oracle review、realization fork など用途別 agent call の入力契約を調査・変更するとき
- Structured Markdown、完全 prompt、oracle・realization・feedback・routing policy の組み立てを調査・変更するとき

## Do not read this when
- CLI の通常の実行制御やサブコマンドの呼び出し順だけを調査するときは、呼び出し側の実装を直接読む
- 個別の oracle file や realization file の正本仕様を確認するときは、対応する oracle または realization 文書を直接読む
- feedback の保存・集約・重複判定だけを確認するときは、collector 側の実装を直接読む
- oracle 全体の責務や下位ディレクトリの選択だけを確認するときは、上位の案内を読む

## hash
- 79a5a6ba0ca5912137d66ddf402fe250b1a724e293741f7a4423b262adeb225e

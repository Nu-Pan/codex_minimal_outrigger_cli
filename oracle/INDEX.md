# `doc`

## Summary
- cmoc の正本文書を、CLI・workflow の挙動仕様、branch／commit／worktree のモデル、開発・テスト規則、採用しなかった設計案に分類して案内する最上位の入口。
- アプリケーション仕様には共通契約と各サブコマンド仕様、開発ルールには実装・環境・テストの規則、branch model には session／run の分岐関係、検討資料群には不採用案の理由が収録されている。

## Read this when
- cmoc の正本文書を探しており、アプリケーション仕様、branch model、開発ルール、検討資料のどの領域から確認すべきか判断するとき
- CLI や workflow の挙動、実装・環境・テストの開発規則、session／run の Git 構造、または不採用案の背景を調査するとき

## Do not read this when
- 確認対象の個別仕様、開発規則、branch model、または検討資料が明確で、その文書へ直接進めるとき
- realization の具体的な実装・テストや、構築済み環境でのテスト実行手順だけを確認するとき

## hash
- 3c27b89cc0385cee73e0673fe1904341e95ffa10b72a1929719b4d72cf5a3024

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

# `doc`

## Summary
- cmoc の正本文書を、アプリケーション仕様、branch・worktree 管理、採用しなかった代替案、開発ルールへ分類して案内する文書群。機能仕様、git による隔離モデル、設計判断の背景、実装・環境・テスト規約を確認する入口となる。

## Read this when
- cmoc の正本文書を探しており、アプリケーション挙動、session／run の branch 管理、設計上の不採用理由、または開発・テスト規約のどこから確認すべきか判断するとき。
- 複数の文書群にまたがる責務分担や、現行仕様と開発ルール・設計背景の適用範囲を確認するとき。

## Do not read this when
- 特定の仕様書、実装、テスト、設定データ、外部契約の詳細だけを確認したいときは、該当する正本文書や対象ファイルを直接読む。
- INDEX.md の生成規則や目次更新処理だけを確認したいときは、インデクシング仕様を直接読む。

## hash
- 212cba3ac95f420ec2ace98e5b10b66709f1f80387c7f10feb30a055ada1d25b

# `src`

## Summary
- `oracle/src` は、cmoc の設定・共有基盤と agent call 定義を束ねる上位入口です。
- agent call の prompt、policy、アクセス制約、routing、cwd、Structured Output、preflight などの起動契約を用途別に構成します。
- oracle review、investigation／edit、realization、feedback、session、TUI、indexing、quota probe などの個別処理へ進むための下位要素を含みます。

## Read this when
- cmoc の共通設定、worktree／root 解決、Markdown レンダリング、または agent call の共通 prompt・policy・アクセス規則を確認するとき。
- 特定用途の agent call における起動パラメータ、入出力契約、Structured Output、preflight、または prompt の入口を探すとき。
- oracle review、realization、feedback、session、TUI、indexing などの処理群を横断して入口や責務分担を把握するとき。

## Do not read this when
- 特定の agent call の詳細な prompt、出力契約、または個別処理の実装だけを確認したいときは、対応する下位対象を直接読む。
- 実際の CLI 実行、引数解析、実行後処理、feedback の保存・集約・重複判定だけを調べるときは、対応する実装本体を直接読む。
- 設定値の具体的な既定値、個別のパス変換、または Markdown ノードの詳細なレンダリング挙動だけを確認したいときは、該当する共通基盤ファイルを直接読む。

## hash
- 0b0749ae02b1c8d33283a4d7817ad9355135a1aad7924794359b1b06e90bc034

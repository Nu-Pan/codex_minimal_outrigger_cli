# `oracle`

## Summary
- AI agent 呼び出し仕様、共通基盤概念、プロンプト構築仕様を扱う oracle src 領域。AI に渡す論理パラメータ、Structured Output schema、モデル設定、file access profile、パス表記、設定、規範文書モデル、プロンプト標準部品の正本仕様断片へ進む入口になる。
- 機能別の agent call 契約を確認する対象、cmoc 全体で共有される設定・パス・アクセス制御を確認する対象、agent call 用プロンプトの構築順序や注入される標準文書部品を確認する対象に分かれる。

## Read this when
- cmoc が AI agent を呼び出す際の role、goal、prompt、file access profile、モデル設定、reasoning effort、出力契約を確認したいとき。
- apply fork、INDEX.md エントリー生成、oracle review、session join の conflict 解消、tui 起動など、機能別の AI 呼び出し仕様を探したいとき。
- cmoc 全体で共有される設定、パス表記、ファイルアクセス権限、規範文書表現、構造化 Markdown レンダリングの正本仕様断片を確認したいとき。
- agent call 用プロンプトの構築順序、静的・動的プロンプトの配置、標準文書注入フラグ、追加プロンプト、プレースホルダ置換の扱いを確認したいとき。

## Do not read this when
- AI agent 呼び出しの実行手順、プロセス起動、結果取得、エラー処理だけを確認したいとき。
- git 操作、branch 操作、fork 作成・適用、session join 通常処理、CLI 表示など、AI 呼び出し契約の外側にある実行フロー本体を確認したいとき。
- 個別 CLI サブコマンドの利用者向け入出力、状態ファイル仕様、実行フローを探しているとき。
- oracle file と realization file の管理方針そのものや、INDEX.md のルーティング規則を自然言語の規範として確認したいとき。
- Codex CLI の外部仕様、利用可能モデル、最新のモデル情報を調べたいとき。

## hash
- e25f63182b56162ad3be0bab05576e25e0958883dc5a421d836ef24c89f51dcf

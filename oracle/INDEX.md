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
- cmoc の agent call に関する正本実装をまとめる領域。agent call パラメータ、モデル・推論・ファイルアクセス設定、prompt 構築、Structured Output schema、パス・設定・構造化 Markdown、feedback・indexing・oracle review・realization などの入口を扱う。
- agent call の起動単位や用途別 prompt/schema を調査・変更するときは `acp_builder` 配下、完全 prompt と共通 policy を確認するときは `prompt_builder` 配下、設定・パス解決・Structured Markdown の共通モデルを確認するときは `other` 配下へ進む。feedback 入力契約そのものは `feedback` 配下を読む。

## Read this when
- cmoc の agent call に渡すモデルクラス、推論強度、ファイルアクセス、cwd、Structured Output schema、indexing preflight の契約を調査・変更するとき
- prompt の組み立て、共通 instruction、file access・routing・oracle・realization・feedback・index entry などの policy を調査・変更するとき
- work root・repository root・run root のパス解決、cmoc 設定、構造化 Markdown のデータモデルやレンダリングを調査・変更するとき
- feedback reporter の入力契約、index entry 生成、oracle review、realization 追従、session join などの agent call builder の入口を特定するとき

## Do not read this when
- Codex CLI の通常の実行制御、サブコマンドのフロー、または agent call 終了結果の処理だけを調査するときは、対応する呼び出し側・実行処理を直接読む
- 特定の prompt policy、Structured Output schema、feedback reporter の保存・集約処理、または用途別 builder の詳細だけを確認するときは、この領域全体ではなく対応する下位要素を直接読む
- cmoc の正本仕様、開発手順、テスト手順だけを確認するときは、対応する oracle 文書を直接読む

## hash
- c18ff8a26b092f6031480c496fbefd8bc4204a3ce8b64bd60ce55d6677e2bdc9

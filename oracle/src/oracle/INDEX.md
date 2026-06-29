# `acp_builder`

## Summary
- AI agent call parameter と Structured Output schema に関する oracle src を集める領域。cmoc の各機能が AI へ渡す role、goal、prompt、file access profile、モデル設定、reasoning effort、出力契約を確認する入口になる。
- 汎用の agent call 入力構造に加え、apply fork、INDEX.md エントリー生成、oracle review、session join の conflict 解消、tui 起動など、機能別の AI 呼び出し仕様を下位要素に分けて扱う。

## Read this when
- cmoc が AI agent を呼び出す際の論理パラメータ、モデル選択意図、reasoning effort、Structured Output schema の有無を確認したいとき。
- apply fork、indexing、review oracle、session join conflict 解消、tui 起動のいずれかで、AI に渡す prompt、file access profile、出力 schema、呼び出し設定の正本仕様断片を探したいとき。
- agent call parameter を組み立てる実装やテストで、機能別に期待される入力構造・出力契約・アクセス制御を確認したいとき。

## Do not read this when
- AI agent 呼び出しそのものの実行手順、プロセス起動、結果取得、エラー処理だけを確認したいとき。
- file access profile、path placeholder、complete prompt rendering、モデル名解決などの共通部品そのものの定義を確認したいとき。
- git 操作、branch 操作、fork 作成・適用、session join 通常処理、CLI 表示など、AI 呼び出し契約の外側にある実行フロー本体を確認したいとき。

## hash
- c569df9c5819eddfd73d1beab18328e784127a660e2234e5d79ea2e8ea2c5f94

# `other`

## Summary
- cmoc の横断的な正本仕様断片を支える oracle src 群を置くディレクトリ。リポジトリ単位の設定、論理ファイルアクセスプロファイル、ルートパスプレースホルダと解決規則、規範文書モデル、構造化 Markdown レンダリング helper を扱う。
- 個別サブコマンドよりも広い基盤概念や、oracle file から realization file を導く際に参照される設定・パス・アクセス・文書構造の入口になる。

## Read this when
- cmoc 全体で共有される設定、パス表記、ファイルアクセス権限、規範文書表現、構造化文書レンダリングの正本仕様断片を探すとき。
- リポジトリごとの永続設定、Codex CLI へ渡すモデル名・reasoning effort 名、agent call 並列数、apply fork や review oracle の上限を確認するとき。
- <cmoc-root>、<repo-root>、<run-root>、<work-root> の意味や、プレースホルダ付きパスと実パスの変換規則を確認するとき。
- oracle、realization、INDEX、memo に対する論理的な読み書き可否や、agent call 用アクセスプロファイルの基本構成を確認するとき。
- 規範文書や階層化された自然言語文書をプログラム上で構造化し、Markdown として出力する helper の仕様を確認するとき。

## Do not read this when
- 個別 CLI サブコマンドの利用者向け入出力、実行フロー、状態ファイル仕様を探しているとき。
- oracle file と realization file の管理方針そのものや、INDEX.md のルーティング規則を自然言語の規範として確認したいとき。
- 実際の OS サンドボックスやファイルシステム権限の実装を確認したいだけのとき。
- Codex CLI の外部仕様、利用可能モデル、最新のモデル情報を調べたいとき。
- 生成済み Markdown 文書の内容や配置先だけを確認したいとき。

## hash
- 199b8b3b25f899c00e12f5cdf7ef6de9726a8fead230b47dbaefce4e9e07bc82

# `prompt_builder`

## Summary
- agent call に渡すプロンプトを構築するための基本型、完全プロンプト組み立て処理、標準文書部品を扱う領域。
- 役割・概要・ゴール、ファイルアクセス制限、ルーティング規則、oracle/realization/review/INDEX エントリー関連の標準、任意の静的/動的プロンプト、プレースホルダ定義をどの責務で扱うかを選ぶ入口。
- プロンプト全体の構築順序を確認する対象と、個別の規範文書部品を確認する対象と、プレースホルダ mapping の基本型を確認する対象へ分かれる。

## Read this when
- agent call 用プロンプトの構築順序、静的プロンプトと動的プロンプトの配置、プロンプトキャッシュを意識した並びを確認・変更したいとき。
- oracle standard、realization standard、review standard、index entry standard などの標準注入フラグの依存関係や、必要な前提プロンプトが自動的に含まれる経路を確認したいとき。
- ファイルアクセス制限、ルーティング規則、各種標準文書など、プロンプト本文へ差し込む規範部品の生成責務から読む先を選びたいとき。
- 追加プロンプト、追加プレースホルダ定義、プレースホルダ名から文字列または Path へ置換する mapping の扱いを確認したいとき。

## Do not read this when
- 個別の CLI 機能、状態ファイル、パス解決、テスト方針など、プロンプト構築ではないプロダクト仕様を調べたいとき。
- oracle file や realization file の実体そのものを確認したいとき。ここではそれらをプロンプトへ注入するための標準文書部品や構築処理を扱う。
- cmoc のパス概念そのもの、または `<cmoc-root>` や `<work-root>` などの意味を調べたいとき。パスモデルの定義を直接読む方が適切。
- ルーティング文書の既存エントリー内容や機械的なファイル一覧・ハッシュだけを確認したいとき。

## hash
- be26c3eb91aa94fc591318ffc0cbca25d118c7732323345c50a32b684564e939

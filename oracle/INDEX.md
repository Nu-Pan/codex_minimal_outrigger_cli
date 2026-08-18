# `doc`

## Summary
- cmoc の正本文書を、アプリケーション仕様と開発ルールの領域に分けて案内する入口。CLI や session/run などの挙動仕様は app_spec、実装・環境・テストの規約は dev_rule へ進む。

## Read this when
- cmoc の正本仕様、開発ルール、実装規約、テスト要件の所在を横断的に確認するとき
- 対象文書が app_spec と dev_rule のどちらに属するか判断するとき

## Do not read this when
- アプリケーション挙動の具体的な仕様が明確で、app_spec 配下の個別文書へ直接進めるとき
- 実装配置、開発環境、テスト要件、テスト実行手順のいずれかが明確で、dev_rule 配下の個別文書へ直接進めるとき
- considered_alternative、branch_model など特定領域の資料だけを調査するとき

## hash
- 6a3131cafc07825e70191d23065036a1e688919b452850fff55aa111ca8c0229

# `src`

## Summary
- oracle/src は、cmoc の agent 呼び出しを構成する oracle 実装のルートである。agent call のパラメータ定義、feedback 入力契約、共有設定・パス・構造化文書処理、完全 prompt の構築を下位領域へ分担している。

## Read this when
- agent call のモデル、reasoning effort、ファイルアクセスモード、cwd、Structured Output などの呼び出しパラメータを調査・変更するときは acp_builder から確認を始めるとよい。
- feedback reporter が受け取る問題分類、重要度、影響、根拠、継続状態などの入力契約を確認するときは feedback から確認を始めるとよい。
- 設定値、モデルプロバイダ設定、root placeholder を含むパス解決、構造化 Markdown の生成を確認するときは other から確認を始めるとよい。
- agent call に渡す完全 prompt の構成、共通規範、各種 policy、placeholder、エディタ入力の組み込みを確認するときは prompt_builder から確認を始めるとよい。

## Do not read this when
- 特定の agent call 種別の詳細実装だけを確認したい場合は、acp_builder 配下の該当実装を直接読む方が適切である。
- prompt の個別 policy や prompt 部品だけを確認したい場合は、prompt_builder 配下の該当ファイルを直接読む方が適切である。
- realization の実装・テスト、oracle 文書そのものの仕様、または既存の INDEX.md のナビゲーションだけを確認したい場合は、このディレクトリを入口にする必要はない。

## hash
- 2d740efeff2629b76a0ce26abd663ada4e4cdb3cbdf0f9a3dbc08d466967022c

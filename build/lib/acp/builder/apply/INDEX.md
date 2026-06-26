# `fork`

## Summary
- fork 適用後の作業レポートと修正サイクルで使う、差分要約・所見列挙・所見対応の AI 呼び出し条件と、それらの structured output 契約を扱う領域。
- 生の差分や起点ファイル、所見リストを complete prompt に組み込み、モデル種別、reasoning effort、file access mode、出力 schema 参照を決める実装と、要約・所見出力の構造定義への入口となる。

## Read this when
- fork 適用後の変更内容を人間向けにカテゴリ単位で要約する処理や、その出力契約を確認・変更したいとき。
- oracle と realization の乖離や要修正点を、根拠位置・要求・観測実装・問題理由・修正方針つきで列挙する AI 調査の呼び出し条件を確認したいとき。
- 列挙された所見を AI エージェントへ渡して realization file を修正させる prompt 構成、権限、モデル、reasoning effort を確認・調整したいとき。
- apply fork 系のレビュー、要約、所見対応で使う structured output schema と prompt builder の対応関係を追いたいとき。

## Do not read this when
- fork の生成、適用、ブランチ操作、差分取得、サブコマンド引数解析など、apply fork 全体の実行制御を調べたいだけのとき。
- oracle standard、realization standard、apply review standard の本文や判定基準そのものを確認したいとき。
- complete prompt の共通組み立て、markdown レンダリング、パス解決、AgentCallParameter 型定義などの汎用 helper の内部実装を調べたいとき。
- 個々の実際の差分内容や変更ファイル本文を直接レビューしたいだけのとき。

## hash
- 5217e8170d226d99751a088680db2a69463a2e4b8e8689f210a92d10924627b2

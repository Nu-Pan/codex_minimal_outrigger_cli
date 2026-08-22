# `oracle`

## Summary
- cmoc の agent 呼び出しと prompt 生成を支える実装群をまとめたソースディレクトリ。AgentCallParameter、論理モデル・推論強度・ファイルアクセスモード、パスと設定のモデル、構造化 Markdown、feedback 入力、用途別 builder、prompt policy を扱う下位要素への入口である。

## Read this when
- AI コーディングエージェント呼び出しの共通パラメータ契約や、用途別 builder の責務分担を確認するとき。
- prompt の組み立て、placeholder、アクセス制約、routing、feedback、oracle・realization 関連 policy の構築方法を横断して調査するとき。
- cmoc の設定・パス解決・構造化 Markdown ノードや、feedback issue 入力契約の実装入口を判断するとき。

## Do not read this when
- 特定用途の agent call prompt や Structured Output の詳細だけを確認したいときは、対応する acp_builder の下位ディレクトリを直接読むとき。
- Codex CLI の実行、モデル名の解決、oracle・realization の正本仕様を確認したいときは、対応する realization 実装または oracle 文書を直接読むとき。
- prompt を生成した後の agent call の実行制御や、feedback の保存・集約を確認したいときは、対応する実行側・collector 側の対象を読むとき。

## hash
- 50f96ed9c8428918201e1d8f121673f06fffbbb42c445ebc3e89ff1139d192b7

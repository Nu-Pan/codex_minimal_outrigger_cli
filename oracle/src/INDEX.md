# `oracle`

## Summary
- AI コーディングエージェント呼び出し用の oracle src をまとめる領域。共通パラメータ、各種 agent call builder、prompt 構成、Structured Output 契約を扱う下位領域への入口。
- feedback、共通基盤、prompt 構築など、agent call に関連する用途別の実装を選択して調査できる。

## Read this when
- agent call の共通パラメータや実行条件を確認するとき。
- TUI、indexing、feedback、oracle、realization、session join などの agent call builder を調査・変更するとき。
- prompt の共通規則、oracle・realization 制約、ルーティング、feedback 報告の構築箇所を探すとき。
- cmoc の設定、root/worktree のパス導出、Standard/Requirement、StructDoc などの共通基盤を確認するとき。

## Do not read this when
- 実際の cmoc サブコマンドの実行フローや agent call の起動処理を調査するときは、呼び出し側や実行基盤を直接読む。
- 個別の oracle file、realization file、Git 操作、レビュー基準、collector 側の feedback 保存・集約仕様を確認するときは、それぞれの対象を直接読む。
- prompt 全体の組み立て順序や初期入力テンプレートなど、共通部品以外の構成を確認するときは、対応する中核ビルダーや入力生成側を直接読む。

## hash
- 375c3f69ae160ff30885c2db8254f736a9dc2c52ae39a25842213149d93caa74

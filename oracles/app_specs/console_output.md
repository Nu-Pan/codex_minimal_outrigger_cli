
# cmoc コンソール出力仕様

## 基本

- 各サブコマンドは進捗状況を標準出力に流す
- 動いているかどうかの確認が目的なので、詳細なログを流す必要はない

## 具体的な出力情報例

- サブコマンド内のステップ名・ステップ数
    - e.g. `cmoc apply` なら `implementation loop (1/3) investigate oracle-implements difference`
- `codex exec` に渡したプロンプト・実行結果から回収した出力
- サブコマンド実行時間レポート
    - ステップ別の経過時間
    - サブコマンド全体の経過時間

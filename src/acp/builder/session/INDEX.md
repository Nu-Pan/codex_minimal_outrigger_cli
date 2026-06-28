# `join`

## Summary
- `cmoc session join` で検出された merge conflict marker の解消を AI エージェントへ依頼するための呼び出しパラメータを組み立てる領域。対象パスを worktree 上の実パスへ解決し、対象ファイル一覧、作業範囲、禁止事項、oracle file の限定的な編集例外を含む complete prompt を生成して返す。

## Read this when
- `cmoc session join` の conflict marker 解消を依頼する AI 呼び出しのプロンプト内容、制約、モデル設定を確認または変更したいとき。
- merge conflict marker の解消対象ファイルがどのようにパス解決され、プロンプト内の対象一覧へ渡されるかを確認したいとき。
- conflict marker 解消時だけ oracle file の編集を許す例外や、git add・git commit 禁止などの作業境界を調整したいとき。

## Do not read this when
- 通常の session join 全体の流れ、merge 実行、conflict 検出、join 後の状態管理を調べたいとき。
- complete prompt の共通構築、構造化 markdown レンダリング、path model、AgentCallParameter 型そのものを調べたいとき。
- conflict marker 解消後の検証、テスト、CLI 入出力の外部仕様を確認したいとき。

## hash
- ddf1a682fce24e7e57c43782ad04d10695e94121970e4c1d25c56af8310e7797

# `oracle`

## Summary
- AIエージェント呼び出しのパラメータ、設定・パスモデル、構造化文書、プロンプト生成に関する正本ソースを扱うディレクトリ。agent call の契約や起動条件、設定・root解決、StructDoc、prompt builder の実装を調査する入口。

## Read this when
- Agent Call Parameter、Structured Output、agent call の起動条件やパラメータを変更・調査するとき
- CmocConfig、root解決、Standard・Requirement・StructDoc の定義や Markdown レンダリングを調査するとき
- prompt builder、プレースホルダ、入力エディタ初期文、oracle・realization・INDEX.md 関連のプロンプト生成規則を調査するとき

## Do not read this when
- CLI サブコマンドの実際の処理や画面操作の挙動を調査するとき
- 共通の prompt 構築・実行フローやバックエンド固有のモデル解決を調査するとき
- 個別の oracle 文書や realization 実装の内容だけを調査するとき

## hash
- 3520457b1aadbdf81640f707c5b7130667da572f2814185f7948e594079ebd02

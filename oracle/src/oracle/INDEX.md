# `acp_builder`

## Summary
- AIエージェント呼び出し用パラメータを構築する正本ソースを扱うディレクトリ。基本パラメータ、INDEX.mdエントリー生成、oracle・realization・session・TUI向けの起動条件やStructured Output契約を確認する入口。

## Read this when
- Agent Call Parameter のモデル、推論強度、アクセス権限、Structured Output、作業ディレクトリを変更・調査するとき
- INDEX.mdエントリー生成の出力形式や生成用agent callを変更・調査するとき
- oracle、realization、session join、cmoc tui のagent call起動条件やパラメータを変更・調査するとき

## Do not read this when
- 対象サブコマンドの実際の処理や画面操作の挙動を調査するときは、各サブコマンドの実装を直接読む
- 共通のprompt構築・実行フローを調査するときは、共通実装を直接読む
- バックエンド固有のモデル名・推論強度への解決方法を調査するときは、realization srcを読む

## hash
- e7b5cdc214c2dece98cc88bef0f4d7cbc29cd68c4e62a5ac2fe35f7d484278a1

# `other`

## Summary
- cmoc の設定、パスモデル、規範定義、構造化 Markdown 文書生成を担う補助モジュール群。リポジトリ固有設定や root 解決、Standard/Requirement、StructDoc の実装を調査する際の入口。

## Read this when
- CmocConfig の設定項目・既定値・シリアライズ対象・Codex および oracle review 設定を確認するとき
- agent call の cwd や repository/work/run root、root placeholder、実パス変換の規則を確認するとき
- Standard や Requirement の定義・検証、Standard から StructDoc への変換を確認するとき
- StructDoc による階層文書の Markdown レンダリング、cmoc_ref 検証、コードブロックやインデント処理を確認するとき

## Do not read this when
- CLI のサブコマンド実行フロー、設定ファイルの生成・同期、agent call prompt 生成だけを調査するとき
- ModelClass や ReasoningEffort の定義、または StructDoc 自体と無関係な oracle 文書の内容だけを確認するとき

## hash
- b62e9df5e183aa361d13b2d8ad4fea5f429768cdbdc76240453b7b9ce61275c1

# `prompt_builder`

## Summary
- プロンプト生成機能の構成要素を収めるディレクトリ。プレースホルダ型、完全な agent call 用プロンプトの構築、入力エディタ初期文、各種規則・定義部品を扱い、prompt builder の個別実装や生成規則を確認する際の入口となる。

## Read this when
- prompt builder の構成や生成部品を変更・確認するとき
- agent call 用プロンプトの組み立て、プレースホルダ、入力エディタ、oracle・realization・INDEX.md 関連規則を調べるとき

## Do not read this when
- 個別の oracle 文書や realization 実装の内容だけを調べるとき
- prompt builder と無関係な CLI、パスモデル、構造化文書の処理を調べるとき

## hash
- 583efd55e167dc7d8971f73ab5e929532590206f2e2d540989f758d4ef4cb396

# `doc`

## Summary
- cmoc の正本仕様文書を集約するディレクトリ。CLI 自動補完、Codex CLI 呼び出し、ログ、doctor preprocess、プロンプト、run・session lifecycle、サブコマンドなどの仕様を横断的に確認する入口で、詳細は各文書または下位ディレクトリへ進む。

## Read this when
- cmoc の正本仕様を横断的に探すとき
- CLI 起動、Codex CLI 呼び出し、ログ、プロンプト、run・session、サブコマンドの仕様上の入口を確認するとき
- 複数機能に共通する仕様文書の所在を判断するとき

## Do not read this when
- 特定機能の詳細仕様が明らかな場合は、対応する個別文書または下位ディレクトリを直接読むとき
- realization の実装・テスト詳細だけを調査するとき
- cmoc の一般的な利用手順だけを確認するとき

## hash
- 6d6060b0bb507d1d9e461a10f290ce69491c4105e87c19cc57608d412756cec4

# `src`

## Summary
- cmoc の正本ソース群への入口。AI エージェント呼び出しパラメータと実行作業単位、設定・パス解決・構造化文書・規範表現、エージェントプロンプトの組み立てを扱う。
- 下位では、エージェント呼び出し関連を acp_builder、共通モデルと構造化文書を other、プロンプト部品と完全なプロンプト生成を prompt_builder が担当する。

## Read this when
- 正本ソースの責務分担や下位モジュールへの入口を確認するとき
- AI エージェント呼び出しの抽象パラメータ、設定・パス表現、構造化 Markdown、プロンプト構成を調べるとき

## Do not read this when
- 個別のプロンプト規範や ModelClass、ReasoningEffort、StructDoc の定義元を直接確認したいとき
- CLI の実行フローや設定ファイルの生成・同期処理を調べるとき

## hash
- b191ce07b20539bc25977f115e5998bec913eafe1199653f2ec755a640ddf4fd

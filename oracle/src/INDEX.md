# `oracle`

## Summary
- AI コーディングエージェント呼び出しの AgentCallParameter と、その完全 prompt・アクセス制御・モデル設定・Structured Output・作業ディレクトリ・indexing preflight を構築する定義を集約する領域です。
- 共通のパラメータ型と論理モデル設定を直下で扱い、indexing、feedback、oracle、realization、session、tui などの処理別 builder と schema へ進むための入口になります。

## Read this when
- 特定の cmoc 処理がどの agent call パラメータ、prompt、Structured Output schema、ファイルアクセスモード、モデル・推論設定で起動されるかを調査・変更するとき。
- AgentCallParameter、ModelClass、ReasoningEffort、FileAccessMode などの共通契約や、agent call の cwd と indexing preflight の設定責務を確認するとき。
- indexing、feedback、oracle、realization、session、tui の agent call builder を横断して、処理別の起動設定の分担を確認するとき。

## Do not read this when
- agent call の実行、Codex CLI への変換、終了結果の処理を調査するときは、対応する realization 実装や呼び出し側を直接読む。
- モデル名や Codex CLI sandbox への具体的な解決規則を確認するときは、realization 実装または指定された oracle 文書を読む。
- 特定処理の prompt 文面、Structured Output schema、通常フローだけを確認したいときは、対応する下位ディレクトリの builder や schema を直接読む。

## hash
- 0c28130aeef7aee4ee0e6b40d13c898e1dae364c4ff8a0cbb26bbbe6391acf66

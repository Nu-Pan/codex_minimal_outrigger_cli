# `launch_tui.py`

## Summary
- `cmoc tui` のプロンプト文面と TUI 起動パラメータを構築する入口。
- オリジナルプロンプトを完全プロンプトへ組み込み、リポジトリ書き込み権限・リポジトリルート・起動前インデックス確認を含む Codex CLI 用パラメータにまとめる。

## Read this when
- `cmoc tui` の起動パラメータや完全プロンプトへのオリジナルプロンプトの埋め込み方を確認・変更するとき。
- TUI 起動時の作業ディレクトリ、ファイルアクセスモード、プロンプト生成におけるルーティング設定、起動前インデックス確認を調べるとき。

## Do not read this when
- 完全プロンプトの構成規則そのものを確認・変更する場合は、`build_complete_prompt` 側を読むとき。
- エージェント呼び出しパラメータやファイルアクセスモードの型定義を確認する場合は、`AgentCallParameter` と `FileAccessMode` 側を読むとき。
- パス解決の一般規則を確認する場合は、`AgentCallPathContext` と `resolve_repo_root` 側を読むとき。

## hash
- 5c6dc20daab60491d3816594695c051776ccc8c0064644b99a462396fd5db2b4

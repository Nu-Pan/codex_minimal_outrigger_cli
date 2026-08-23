# `launch_tui.py`

## Summary
- `cmoc oracle investigation` 用の TUI 起動パラメータを構築する関数。ユーザーの調査指示を埋め込んだ完全プロンプトを、oracle 限定・読み取り専用の作業範囲で生成する。
- oracle 調査のパス、分類、アクセスモード、モデル品質設定、indexing preflight を固定した `AgentCallParameter` を返す。oracle 調査起動の構成と、エディタに提示する prompt skeleton の構築経路を確認する入口になる。

## Read this when
- `cmoc oracle investigation` の TUI 起動パラメータ、完全プロンプト、oracle 限定のファイルアクセス範囲を変更または調査するとき。
- oracle 調査起動時のモデル、推論設定、indexing preflight、agent call の作業ディレクトリを確認するとき。

## Do not read this when
- 通常の prompt 生成規則や共通の構造化文書レンダリングを確認したい場合は、`build_complete_prompt` や構造化文書関連の定義を直接読む。
- oracle 調査以外の agent call や TUI 起動パラメータを変更する場合は、その用途に対応する起動パラメータ定義を直接読む。

## hash
- cb40d24c51a6089fc40aed909bc58f1f0c2ddc6626ce47044321a22c640ab0d3

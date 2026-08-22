# `launch_tui.py`

## Summary
- `cmoc tui` のプロンプト文面と TUI 起動用 `AgentCallParameter` を構築する定義。プロンプト生成、リポジトリルートの作業パス確定、モデル・推論設定、アクセスモード、インデックス事前実行など、TUI 起動時の固定パラメータをまとめる入口。

## Read this when
- `cmoc tui` の起動パラメータ、完全プロンプトの構築、または TUI 起動時のモデル・推論・ファイルアクセス設定を確認・変更するとき。

## Do not read this when
- TUI の画面表示や対話ループそのものを調べるとき。プロンプト構造の詳細は `build_complete_prompt` や構造化文書の定義を直接確認するとき。

## hash
- 7505640da98b83392a2291346e08ea01f27f8dd64f8aa88403ded419962f7b2d

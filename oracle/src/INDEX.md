# `oracle`

## Summary
- cmoc の oracle source を構成する実装・設定・agent call 定義の領域。`acp_builder`、`feedback`、`other`、`prompt_builder` の各下位領域へ進むための入口であり、agent 呼び出しパラメータ、feedback 入力契約、設定・パス・構造化文書モデル、完全 prompt と各種 policy の実装を扱う。

## Read this when
- cmoc の oracle source 内で調査・変更すべき責務が `acp_builder`、`feedback`、`other`、`prompt_builder` のどれに属するか判断するとき
- agent call 構築、feedback reporter 入力契約、設定・パス・文書モデル、prompt policy の実装群を横断して確認するとき

## Do not read this when
- 対象の下位ディレクトリが特定できており、その具体的な実装・スキーマ・prompt 定義を直接確認すればよいとき
- oracle の正本仕様、realization 実装、通常の CLI 実行や TUI 表示の挙動を確認するとき
- 下位要素の具体的な責務や Structured Output の詳細を確認したいときは、対応する `acp_builder`、`feedback`、`other`、`prompt_builder` の下位対象を直接読む

## hash
- bb11747435a736e8240bc22385a414d3c1f10657d767f9781b1ee9ab5a7a271c

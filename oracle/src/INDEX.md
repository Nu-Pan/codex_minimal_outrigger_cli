# `oracle`

## Summary
- cmoc の oracle src 群のうち、AI エージェント呼び出し仕様と横断的な基礎モデルを扱う領域への入口。agent call parameter、prompt、Structured Output schema、パス表記、設定、規範文書モデル、Markdown helper などの正本仕様断片を下位領域へ振り分ける。
- プロンプト構築や共通規範注入、サブコマンド向け agent 呼び出し契約、複数領域から参照される補助モデルのどれを確認すべきか判断するためのルーティング対象。

## Read this when
- cmoc の oracle src にある正本仕様断片のうち、AI エージェント呼び出し、prompt、Structured Output schema、またはそれらを支える横断モデルを探すとき。
- agent call 用の共通 parameter、機能別 builder、完全プロンプトの構築順序、共通規範プロンプト、ファイルアクセス制限やルーティング規則の注入位置を切り分けたいとき。
- cmoc の設定値、ルートパスプレースホルダ、パス解決、規範文書の構造化、仕様文生成用 Markdown helper など、複数領域から参照される基礎概念の oracle src を確認したいとき。

## Do not read this when
- CLI 実行制御、branch 操作、diff 取得、レポート保存、対象ファイル探索、表示整形など、AI エージェント呼び出し仕様や横断モデルではない実装を調べたいとき。
- 特定サブコマンドの利用者向け入出力、実行手順、状態ファイル仕様だけを確認したいとき。
- realization code 側の prompt builder 実装、外部コマンド起動、バックエンド固有モデル名への変換、またはテスト構成を確認したいとき。

## hash
- 0c23d06673deb2af31e4f14e81a46914955e314e08a516d37c75426143903307

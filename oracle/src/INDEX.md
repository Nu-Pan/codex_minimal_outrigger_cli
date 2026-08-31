# `oracle`

## Summary
- cmoc の oracle 実装・入力契約を構成する最上位の入口。AI エージェント呼び出し構築、prompt 生成、設定・パス・構造化文書の基盤、feedback／editor input の契約へ進むためのルーティングを担う。
- agent call の用途別 builder や prompt の構築規則を調べる場合は `acp_builder` または `prompt_builder` へ進む。設定・パス解決・Markdown 構造化文書の実装を調べる場合は `other` へ進む。
- feedback reporter や editor input handoff の入力契約を調べる場合は、それぞれ `feedback` または `editor_input_handoff` へ進む。

## Read this when
- oracle 配下の機能領域を特定し、どの下位ディレクトリから調査を始めるか判断するとき。
- agent call、prompt、設定・パスモデル、構造化文書、feedback、editor input のいずれかに関係する oracle 実装の入口を選ぶとき。

## Do not read this when
- 特定の agent call builder、prompt policy、schema、設定モデル、パスモデル、または構造化文書の具体的な実装を確認したいときは、対応する下位対象を直接読む。
- feedback の保存・集約処理や、editor input の実行処理など、ここで扱う入力契約以外の処理を調べるとき。

## hash
- 7e705a9a8fc125db1c7cb6bf769425b95f557f9e288cfe252dfe248a693d273c

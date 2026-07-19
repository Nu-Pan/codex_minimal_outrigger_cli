# `doc`

## Summary
- cmoc の開発・アプリケーション仕様を定義する oracle doc 群を収めるディレクトリ。branch、session/run、CLI、Codex、ログ、prompt、Ollama、doctor、サブコマンドなどの個別仕様と、開発環境・設計・テスト規約への入口を提供する。

## Read this when
- cmoc の機能仕様、branch・session・run のモデル、CLI の挙動、または開発規約を実装・変更・レビュー・検証するとき。
- 対象機能の個別 oracle 文書や、複数機能にまたがる共通仕様の所在を探すとき。
- 不採用案の背景や realization refactor の検討記録を確認するとき。

## Do not read this when
- 対象の個別仕様文書が特定できており、その本文だけを直接確認すれば足りるとき。
- 実装内部の具体的な関数・テスト詳細だけを調査するとき。
- 一般的な仕様と無関係に、既存 realization code の実装内容だけを確認するとき。

## hash
- bd61a89a3e98df140343cc9c3ebf38c394b9c861638eab63b79f3616e80d2b14

# `src`

## Summary
- oracle の設定、パス解決、規範データ構造、Markdown レンダリング、cmoc_ref 検証を担う実装群への入口。ACP builder や prompt builder など、エージェント呼び出し条件とプロンプト構築を支える下位実装も含む。

## Read this when
- cmoc の設定値や既定値、Codex・Ollama・oracle review の制御を確認・変更するとき。
- プレースホルダを含むパス解決や、cmoc・repo・run・work ルートの探索を調査するとき。
- 規範文書の構造化、Markdown 変換、cmoc_ref 検証を調査するとき。
- ACP builder、prompt builder、agent call 構築条件の担当箇所を特定するとき。

## Do not read this when
- CLI 機能の具体的な実装や入出力処理だけを調査するとき。
- エージェント呼び出しの実行本体や、生成済み文書などの成果物を確認するとき。
- 個別ファイルや schema の所在が既に特定でき、その本文だけを確認すればよいとき。

## hash
- 4d4b2e90612f2ff769bbc13f144b5f1f13b4f98efdc51047728006458d7524b6

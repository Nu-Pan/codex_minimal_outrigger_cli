# `cmoc_config.py`

## Summary
- 開発対象リポジトリごとに変わりうる cmoc の挙動設定を集約し、Codex CLI の provider・agent call 設定や並列数、アクセス規定違反時の復旧試行回数を定義する設定モデル。設定の永続化先と JSON シリアライズ時のメンバー順序も説明する。

## Read this when
- cmoc の設定項目、既定値、Codex CLI 呼び出しごとのモデル設定、provider-local 設定、または設定の永続化・編集方針を確認するとき。

## Do not read this when
- agent call のプロンプト生成や実際の CLI 呼び出し処理を調べるとき。設定値を保存・同期する具体的な処理だけを調べる場合は、その処理を実装する対象を直接読む。

## hash
- d6ce4046ae9484f0eebdbb1e9bbc9e0ff6d7243038f8dcf18550fe038f1a67a5

# `path_model.py`

## Summary
- cmoc のパス表記とルートプレースホルダを定義する基盤モデルです。
- agent call の cwd から worktree root と main repository root を導出し、呼び出し全体で共有するパスコンテキストを提供します。
- プレースホルダを絶対パスへ解決する処理と、絶対パスをプレースホルダ表記へ変換する処理を扱います。
- Git metadata や cmoc の配置を探索して、repository・worktree・run の各ルートを特定します。

## Read this when
- agent call のパスコンテキスト、worktree root、main repository root の導出規則を確認するとき。
- {{cmoc-root}}、{{repo-root}}、{{run-root}}、{{work-root}} の解決または変換処理を変更・調査するとき。
- プレースホルダ付き相対パスの入力制約や、Git worktree metadata に基づくルート探索の挙動を確認するとき。

## Do not read this when
- 個別の CLI 機能や realization の実装責務だけを確認したいとき。
- パスモデルを介さない一般的なファイル操作や、対象モジュール以外の仕様を直接調べるとき。

## hash
- 7172c36b342a5b115ebddf8f4731b459a305d57195f24b2e2af448f2caabb628

# `struct_doc.py`

## Summary
- 構造化された文書ノード（見出し、参照可能ブロック、コードブロック、規定、文字列）を Markdown へレンダリングするヘルパーと、三重引用文字列の正規化を提供する。
- Markdown 見出しの深さを階層から自動計算し、cmoc_block や可変長フェンスを含む自然言語文書を生成するための下位実装。

## Read this when
- プログラム上の階層構造から Markdown 文書を生成する処理を確認するとき。
- SDHeader、SDTagBlock、SDCodeBlock、SDPolicy のレンダリング仕様や、ntqs による本文整形を調べるとき。

## Do not read this when
- INDEX.md の構造やルーティング規則そのものを確認したいとき。
- Markdown 以外の文書形式のレンダリング実装、またはこのファイルを直接利用しない CLI の処理を調べるとき。

## hash
- 6df4567a0a45f47b0e22c6def77446eb9b083ca9d26d65634bbdb2aecb24f7d5

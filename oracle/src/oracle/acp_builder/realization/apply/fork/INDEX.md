# `launch_exec.py`

## Summary
- `cmoc realization apply fork` 実行用の AgentCallParameter を構築する定義で、差分追従のための prompt、対象 commit 範囲、oracle file の raw diff、linked worktree をまとめて起動設定へ変換する。
- `realization_apply_change` タグ付きの構造化情報を prompt に埋め込み、リポジトリ全体の realization file を oracle file の変更へ追従させる方針、完了条件、ファイルアクセス方針、oracle/realization/routing の各ポリシーを指定する。
- 同階層の別ファイルではなくこの対象へ進むべきなのは、`realization apply fork` の一回の Agent call に必要な prompt 文面と起動パラメータ（モデル、推論強度、作業モード、作業ディレクトリ、preflight）を一体で定義・変更・確認するときである。

## Read this when
- `realization apply fork` が oracle file の差分を realization file 全体へ反映する Agent call を起動する仕組みを調査・変更するとき。
- 差分の始点・終点 commit、raw oracle diff、linked worktree を prompt へ渡す方法を確認するとき。
- 起動時のモデル品質、推論強度、realization write 権限、indexing preflight などの AgentCallParameter 設定を確認するとき。

## Do not read this when
- 個別の prompt 生成部品や構造化ドキュメントの一般的な仕様だけを調べるときは、`build_complete_prompt` や `struct_doc` の定義を直接読む。
- `realization apply fork` 以外の apply 経路、または実際の realization implementation・test の挙動を調べるときは、それぞれの対象ファイルを直接読む。
- oracle file の変更内容そのものや repository 共通の開発ルールだけを確認する場合は、この起動定義ではなく該当する oracle file・開発規約を読む。

## hash
- e8e5e281b9bbaffaa4af9331ff3e9980e415786efda7ee035639c8b822b016ef

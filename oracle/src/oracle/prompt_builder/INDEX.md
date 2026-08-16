# `basic.py`

## Summary
- プレースホルダ名を実パスや文字列へ対応付ける型定義を置く。プロンプト組み立てで、置換対象の名前と置換先を共通の表現で扱いたいときに読む。

## Read this when
- プレースホルダ展開に使う型の意味を確認したいとき。
- 文字列と `Path` を混在させる置換対象の表現を統一したいとき。

## Do not read this when
- プロンプト本文の生成手順や置換ロジックの詳細を知りたいときは、実装側を読む。
- プレースホルダを使わない処理や、別の設定値の表現を確認したいだけのとき。

## hash
- 526fb2d3d3f5fd312f3f1cc48c630d59e91568f38d6ac0d09bc5241792eb1e18

# `complete_prompt.py`

## Summary
- cmoc の agent 向け完全プロンプトを構築する中核モジュール。概要・完了条件・各種ポリシー・ファイルアクセス規則・ルーティング規則・プレースホルダ定義を、選択された構成に応じて決定論的に統合する。
- ポリシー間の依存関係を自動的に有効化し、重複するポリシーやプレースホルダ定義を統合しながら、agent call に渡す構造化文書列を生成する。
- agent prompt の構成、ポリシー注入、プレースホルダ統合、または特定の作業種別に必要な規定の有効化条件を変更・調査するときの入口。個別ポリシーの具体的内容は同階層の各 policy builder を直接確認する。

## Read this when
- agent 向け完全プロンプトの生成順序や構造を確認するとき
- 各種ポリシーの依存関係、自動有効化、重複統合の挙動を変更・調査するとき
- プレースホルダ定義の統合や動的・静的プロンプトの組み立てを変更するとき

## Do not read this when
- 個別ポリシーの本文や規則だけを確認したいときは、対応する policy モジュールを直接読む
- プロンプト生成とは無関係な CLI 実装や oracle・realization の個別仕様を調査するとき

## hash
- 13790db92ca3b83f1368a45ae45af37eaf652006aa16bce87800ab5af5cfec97

# `editor_input.py`

## Summary
- エディタ経由で後続の AI エージェントへ渡すユーザー入力ファイルの初期テキストを構築する定義。使い方・記入方針・完全プロンプトのテンプレートを HTML コメント内にまとめる入口であり、プロンプト入力用ファイルの初期内容やコメント除去前の構造化レンダリングを確認したい場合に読む。

## Read this when
- エディタ経由のプロンプト入力ファイルにどの初期案内やテンプレートを注入するかを変更・確認するとき
- 完全プロンプト中のユーザー入力差し込み位置を、初期テキスト生成側から調査するとき

## Do not read this when
- 後続エージェントへ渡す完全プロンプト全体の構築規則を調べるとき
- StructDoc、StructBlock、Markdown レンダリング自体の仕様を調べるとき
- エディタ経由ではないユーザー入力経路や、保存記録としてのプロンプト管理を調べるとき

## hash
- ef8b185c6711e48c549cd12fc63e19d1412a834885495065bc4b0eabef94017f

# `parts`

## Summary
- oracle と realization の基本的な分類境界・役割・下位概念を説明する prompt_builder の構成要素。call-scoped context の work-root を説明文へ反映する処理も含む。oracle/realization の基本説明文の生成経路を確認・変更するときの入口。
- oracle と realization の扱い、仕様レビュー・検証、conflict 解消、editor handoff、INDEX.md ルーティングに関する共通ポリシー定義。これらの規範や判断境界を確認するときの入口。

## Read this when
- oracle と realization の分類規則、責務、下位概念を確認するとき
- oracle/realization の基本説明文の生成経路を調査・変更するとき
- oracle の権威性や仕様解釈、realization の実装・テスト・検証方針を確認するとき
- conflict marker の解消、editor handoff、INDEX.md エントリー作成の規範を確認するとき

## Do not read this when
- 個別の oracle file または realization file の具体的な要求・挙動だけを確認する場合
- 具体的な分類アルゴリズムやテスト実装を確認する場合
- 共通ポリシーや oracle/realization の基本概念を扱わず、通常の実装詳細や単一のテストケースだけを確認する場合

## hash
- 8728ceea1236d95e4bd71601ea783e8d101fa0ecdeb8f27489706b7125ef64e4

# `policy`

## Summary
- agent 向け instruction policy の構築定義を集約するディレクトリ。共通の Policy／PolicyGroup 合成、oracle・realization の権威規則、review・conflict resolution・handoff・feedback reporting・file access・routing など、用途別の policy collection builder への入口を提供する。個別 policy の具体的な判定規則は各定義元へ、PolicyCollection の構造や合成動作は基本実装へ進むための上位ルーティング対象。

## Read this when
- oracle・realization file に関する agent call の instruction policy 構成を確認または変更するとき
- review、conflict resolution、editor handoff、feedback reporting、file access、INDEX.md entry 生成など、用途別 policy collection の選択規則を調べるとき
- PolicyGroup の共有構成や、policy の決定的な合成・instruction 文面化の入口を特定するとき

## Do not read this when
- 個別 policy の具体的な判定内容だけを確認したいときは、対応する policy 定義へ直接進む
- PolicyCollection・PolicyGroup のデータ構造や衝突検査・render 動作だけを確認したいときは、基本実装を直接読む
- 実際の CLI 処理、oracle／realization file の本文、または prompt policy と無関係な仕様を調査するとき

## hash
- 09a6d4255c491b59ed32e11a92223c2c24f05f4ab5a0eb446143bc7ef19995bf

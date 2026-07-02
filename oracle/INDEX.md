# `doc`

## Summary
- cmoc の正本仕様ドキュメント群を置く領域であり、アプリケーション仕様、branch/worktree モデル、採用しなかった代替案、開発規則など、自然言語で書かれた oracle doc への入口になる。
- 利用者向け外部挙動、git branch / worktree の概念、設計判断の背景、realization code の開発基準などを、下位領域や個別文書ごとに分けて扱う。

## Read this when
- cmoc の仕様を自然言語の正本仕様断片から確認したいとき。
- CLI 挙動、サブコマンド仕様、Codex CLI 呼び出し、ログ、エラー、セッション状態、INDEX.md 自動生成、run 隔離などのアプリケーション仕様文書へ進む入口を探すとき。
- session fork / join、cmoc-managed branch、run branch、linked worktree、fork / join commit などの git branch / worktree モデルを確認したいとき。
- 採用されなかった設計案の背景や、不採用理由を確認して、自然に見える代替案を再導入してよいか判断したいとき。
- Python 実装、CLI 構成、開発環境、pytest 方針など、realization code を追加・変更する前の横断的な開発規則を確認したいとき。

## Do not read this when
- oracle file と realization file の一般的な責務分担、編集権限、品質基準、INDEX.md エントリー生成基準そのものを確認したいだけのとき。
- パスキーワードやルートディレクトリ概念そのものの定義だけを確認したいとき。
- 現在の実装ファイル、テストファイル、既存関数、内部 helper、依存関係など realization code の具体構造を調べたいとき。
- 既に読むべき個別の正本仕様文書や下位領域が特定できており、その本文を直接読む方が早いとき。

## hash
- 70d66840404497d3494dcf52385a33c7ce77c82bd116110b178b148893699d30

# `src`

## Summary
- cmoc の正本実装断片のうち、AI エージェント呼び出しパラメータ、完全プロンプト構築、設定・パス表記・規範文書・Markdown 整形などの基礎モデルを束ねる領域。
- サブコマンド別の agent call parameter、Structured Output schema、prompt 注入規則、ルートプレースホルダ付きパス、設定境界、構造化文書モデルへ進むための入口になる。

## Read this when
- cmoc が AI エージェントへ渡す prompt、role、goal、モデル設定、reasoning effort、ファイルアクセス方針、Structured Output schema の正本仕様断片を探すとき。
- agent call 用の完全なプロンプトが、標準プロンプト、補助プロンプト、ファイルアクセス規則、ルーティング規則、プレースホルダ定義からどう組み立てられるかを確認したいとき。
- cmoc の設定項目、既定値、リポジトリ別挙動設定、設定ファイルの永続化境界を確認したいとき。
- ルート概念、プレースホルダ付きパス、絶対パス、git worktree との関係を確認したいとき。
- 規範文書を構造化して保持するモデルや、階層化された文章を Markdown へ整形する helper の正本実装断片を確認したいとき。

## Do not read this when
- CLI 引数解析、git 操作、branch 操作、実行フロー、保存処理、結果集約、表示処理など、正本実装断片を利用する realization implementation 側の制御を調べたいとき。
- oracle file、realization file、index entry、各 standard の定義本文や品質基準そのものを確認したいだけのとき。
- 設定の読み書き処理、JSON 変換処理、状態ファイル操作、レビュー所見の生成・検証ロジック自体を探しているとき。
- 生成済みプロンプトをどこで agent call へ渡すか、または realization implementation や realization test の現在構造を追いたいとき。
- 特定の下位領域が対象だと分かっており、用途別 agent call parameter、プロンプト構築、または基礎補助モデルへ直接進めるとき。

## hash
- beb99b12591d3dcede0d9bf49ab078e3b0e0e7ce5374d7b9e2435a949731a51f

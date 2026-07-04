# `cmoc_config.py`

## Summary
- cmoc のリポジトリ別設定を集約する `CmocConfig` と、その配下の Codex CLI、apply fork、review oracle 向け設定クラスを定義する oracle src。設定の永続化先、人間編集対象であること、Enum 系値の JSON 保存時の扱い、各サブコマンドの実行予算やモデル指定の正本断片を扱う。

## Read this when
- cmoc の設定項目、既定値、永続化先、人間編集可能な設定ファイルの扱いを確認したいとき。
- Codex CLI に渡すモデル、reasoning effort、model provider、ファイルアクセス規則違反時のリカバリ回数に関する仕様断片を確認したいとき。
- `cmoc apply fork` や `cmoc review oracle` のループ回数・処理件数など、リポジトリごとに変わりうる実行予算設定を扱うとき。
- Enum 系の設定値を JSON へ保存する際の value 化など、設定のシリアライズ方針を確認したいとき。

## Do not read this when
- 設定値を読み書きする実装コードや JSON 変換処理そのものを探しているだけで、正本仕様断片の確認が不要なとき。
- パス概念一般、work-root や repo-root の定義を確認したいとき。
- Codex CLI 呼び出し全体のプロンプト構築、agent call orchestration、モデルクラスや reasoning effort 自体の定義を確認したいとき。

## hash
- 273608bef07480763b0eaf32bd644b1ec2901f3430f15a9453edf4bb90c6d2b4

# `cmoc_managed_ollama.py`

## Summary
- cmoc 設定で model_provider が cmoc のモデルがある場合に、cmoc 管理の Ollama を利用可能にするための手順を置く実装断片。
- Ollama の取得・展開、ユーザー systemd service の定義、サービス起動確認、API 疎通確認、対象モデルの pull までの流れを扱う。

## Read this when
- cmoc 管理の Ollama を準備する処理、起動方式、systemd user service、OLLAMA_HOST・OLLAMA_MODELS の扱いを確認したいとき。
- cmoc 設定内のモデル指定から Ollama を必要とするか判定する処理を確認したいとき。
- cmoc provider のモデルをローカル Ollama へインストールする流れを実装・検討するとき。

## Do not read this when
- Codex や cmoc 設定構造そのものを確認したいだけのとき。
- Ollama 以外の model_provider や外部 API provider の接続処理を調べたいとき。
- パス表記や struct doc の文字列整形 helper の定義を確認したいとき。

## hash
- e545328ae1911e5803298068794f35bd0a134c34a762894dcf8e352d2a3e3849

# `path_model.py`

## Summary
- cmoc で用いるルートパスプレースホルダと、プレースホルダ付きパス・絶対パスを実パスへ解決する処理を定義する。
- `<cmoc-root>`、`<repo-root>`、`<run-root>`、`<work-root>` 相当の概念について、各ルートの探索条件、git worktree との関係、実パスからプレースホルダ表記へ戻す変換を扱う。
- プレースホルダなし相対パスを禁止し、絶対パスまたはルートプレースホルダ起点の相対パスだけを受け付けるというパス表記規則の実装根拠になる。

## Read this when
- cmoc 上でパスをどの形式で表記してよいか、プレースホルダなし相対パスをどう扱うかを確認したいとき。
- cmoc 自体のルート、対象 git リポジトリの main worktree、run 用 linked worktree、呼び出し cwd から見た worktree root の違いを確認したいとき。
- プレースホルダ表記から実際の絶対パスへ解決する挙動、または実パスを特定のルートプレースホルダ起点の表記へ変換する挙動を実装・検証するとき。
- `.git` ディレクトリ、`.git` ファイル、`bin/cmoc` の有無を使ったルート探索条件を確認したいとき。

## Do not read this when
- INDEX.md のルーティング規則や oracle file と realization file の管理方針だけを確認したいとき。
- CLI サブコマンドの利用者向け入出力、実行フロー、状態ファイルの仕様を探しているとき。
- 特定の作業ディレクトリ内でどのファイルを読むべきかを知りたいだけで、パス表記モデルやルート解決規則を確認する必要がないとき。

## hash
- b9d00168670dbd5dc0c11ba2bede21d8ee226aa0f3c1552223c0ad11f3a24ffe

# `standard.py`

## Summary
- 規範文書を構造化して表現するためのモデルを定義する。規範の見出し、背景、要求、判断例を保持するクラス、要求ラベル付きの要求要素、構造化ドキュメントへの変換処理を扱う。
- 規範そのものの内容ではなく、規範を記述・生成するためのデータ構造と整形規則を確認する入口になる。

## Read this when
- 規範をプログラム上でどのフィールドに分けて保持するかを確認したいとき。
- 規範の背景、要求、判断例がどのような必須性や検証条件を持つかを確認したいとき。
- 要求ラベルとして扱える値や、要求本文に求められる書き方を確認したいとき。
- 規範オブジェクトを構造化ドキュメントへ変換する出力構成を確認したいとき。

## Do not read this when
- 個別の規範本文や、各規範が実際に要求する内容を知りたいとき。
- 構造化ドキュメント一般の表現形式や出力レンダリング仕様を確認したいとき。
- 実装対象ツリー内の実現ファイルに適用される品質基準そのものを確認したいとき。
- パス概念、正本仕様断片、実現ファイルの定義を確認したいとき。

## hash
- eba22392c2c74b41ab3baffc5683aad11b33b5e641e96e3388c545ac180abb4d

# `struct_doc.py`

## Summary
- 階層構造を持つ自然言語文書を Markdown にレンダリングするための小さなヘルパーを定義する。
- 見出し深さの自動計算、本文テキスト、コードブロック、triple quoted string 由来のインデント正規化、連続空行の圧縮を扱う。
- 構造化された仕様文や説明文をプログラム側で組み立て、Markdown 文字列として出力する処理の入口になる。

## Read this when
- 階層化された文章データから Markdown 見出しを自動生成する挙動を確認したいとき。
- StructDoc や StructCodeBlock の受け付ける子要素、保持する情報、型エラー条件を確認したいとき。
- render_as_markdown の出力形式、見出しの深さ、本文やコードブロックのレンダリング規則を確認したいとき。
- triple quoted string として書いた本文の前後空行除去、共通インデント解除、連続空行圧縮の仕様を確認したいとき。

## Do not read this when
- Markdown 文書の内容そのものや、生成される仕様文の意味を知りたいだけのとき。
- CLI の入出力、実行状態、パスモデル、設定、永続状態など、構造化文書レンダリング以外の挙動を調べているとき。
- 既に生成済みの Markdown の読み方や配置先を調べたいだけで、レンダリング helper の挙動を変更・確認しないとき。

## hash
- 3d1268dd3af1ee28e8fb218543d1dd4c9aaf69c39324e05c48316d6992da7613

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
- agent 向け完全プロンプトを、基礎規定・個別ポリシー・追加文面・目的・placeholder 定義の順に構築する関数を扱う。
- 選択されたポリシービルダーの文面と定義を統合し、同名 placeholder の異値上書きを拒否する。
- プロンプト冒頭の参照地図、fundamental_policy と objective の構造化、変動の少ない要素を先に配置する構成を担う。
- agent call 用プロンプトの全体構成や注入順序を確認・変更するときの入口であり、個別ポリシーの内容や placeholder の定義元を調べる場合は各下位モジュールへ進む。

## Read this when
- agent 向け完全プロンプトの構築順序や全体構成を確認するとき
- summary、goal、path_context、追加プロンプト、ポリシー選択の反映方法を変更するとき
- 複数のポリシー文面と placeholder 定義の統合規則を確認するとき
- プロンプトのキャッシュを意識した固定要素・可変要素の配置を確認するとき

## Do not read this when
- 特定のポリシー本文の内容や生成規則だけを調べるとき
- 個別の placeholder の値や定義元だけを調べるとき
- SDHeader や SDTagBlock のデータ構造そのものを調べるとき
- agent call の呼び出し側で summary、goal、各フラグを決める規則を調べるとき

## hash
- 73011939d0ed825b3ea37627375451a7ea0194542a3a9b13b724527cfade9118

# `editor_input.py`

## Summary
- 対象ファイルは、エディタ経由で後続 AI エージェントへ渡すユーザー入力ファイルの初期表示文面を構築する関数を定義する。使い方・記入上の目安・完全プロンプトのテンプレートを HTML コメント内にまとめ、入力本文が所定のプレースホルダーへ注入される前提を扱う。

## Read this when
- エディタ経由のプロンプト入力ファイルに表示する初期文面の構成や、ユーザーへの記入案内、テンプレート埋め込みの挙動を確認・変更するとき。
- 初期テキストに含める構造化見出し・タグブロックの組み立てと、HTML コメントとしてのレンダリング範囲を確認するとき。

## Do not read this when
- エディタ入力の初期文面ではなく、完全プロンプト全体の生成規則や別経路のプロンプト入力処理を確認するときは、それぞれの担当実装・仕様を直接読む。
- 構造化ドキュメント要素の定義や Markdown レンダリング仕様そのものを確認したい場合は、インポート元の構造化ドキュメント実装を読む。

## hash
- 801c5e31f4bbfc2b036f94ce9ef77536f12136fe02cba369a4f477b5b6150d35

# `parts`

## Summary
- oracle と realization の基本概念を prompt-builder の説明文として構築する部品。両者の役割、正本関係、下位分類、分類条件をまとめ、call-scoped context の work-root を各パス説明へ埋め込む。
- uncategorised file の分類対象として、特定ディレクトリ・ファイル名・git ignore・実際の git metadata に基づく規則を説明文へ含める。対象ディレクトリ内で oracle/realization の分類ルール全体へ進む入口となる。

## Read this when
- oracle file と realization file の責務境界、編集主体、正本関係を確認するとき
- oracle doc・oracle src・oracle test、または realization code・realization implementation・realization test・realization ancillary の分類を確認するとき
- work-root を使った oracle/realization の配置場所や分類条件を確認するとき
- uncategorised file のパス、ファイル名、git ignore、git repository metadata による分類規則を確認するとき
- work-root の call-scoped context から説明文用プレースホルダーへ値を渡す処理を変更・調査するとき

## Do not read this when
- 個別の oracle 文書・実装・テストの内容そのものを確認したいとき
- realization の具体的な実装責務やテスト実行方法だけを確認したいとき
- INDEX.md や AGENTS.md 自体の分類対象外規則だけを確認したいとき

## hash
- 81e086274e3b84b3f847a1b3cf05f5016357bec748a19d77d50bcb84cafb0189

# `policy`

## Summary
- oracle file に対する realization file の追従要否、所見、修正対象を判断する policy の構築入口。oracle を人間が所有する正本仕様断片として扱い、oracle の具体的要求と realization の具体的挙動の明確な不整合、または realization 単独で説明できる実行不能・明白な致命的バグを修正対象とする規定を定義する。
- 所見や修正対象には、用途固有の policy が認める具体的な oracle file または realization file の記述・挙動を示すことを求める。oracle の意味を realization の都合で変更せず、仕様の隙間、複数の妥当解、好み、推測、一般的なベストプラクティスだけを根拠に問題を作らない制約も定める。
- 修正後の realization file が関連する oracle file の明示要求を満たすこと、および調査開始時点で解消済みの問題を所見にしないことを確認するための入口となる。

## Read this when
- oracle file と realization file の適合性を判断するとき
- realization file の追従要否、所見の成立、修正対象を判断するとき
- oracle の明示要求と realization の具体的挙動の不整合を根拠付きで評価するとき
- realization 単独で説明できる実行不能または明白な致命的バグを修正対象とするか判断するとき

## Do not read this when
- oracle・realization file の適合性や修正対象の判断を行わないとき
- 仕様の隙間、好み、推測、一般的なベストプラクティスに基づくコード品質改善を検討するとき
- 具体的な oracle file または realization file の内容・挙動そのものを確認する必要があるとき
- prompt builder の別の policy の構築規定だけを確認するとき

## hash
- 4d351d81b1e1c1b6ef71e5c678cc488f603074910ac3a464fc825b3dc56cc835

# `__init__.py`

## Summary
- oracle src の acp 互換 import 入口を示す。既存の acp.* 参照を保つために、oracle/src/oracle/acp_builder を複製せず参照互換性を維持する役割を持つ。

## Read this when
- acp.* import 互換性のために残されている入口の意図を確認したいとき。
- acp.* 参照を oracle.* または実体 module へ移行する作業で、この入口の削除条件を確認したいとき。

## Do not read this when
- acp_builder の実体や仕様内容を確認したいときは、実体側の module を読む。
- 新規機能の実装詳細や通常の oracle src の構造を調べたいだけで、acp.* 互換 import に関係しないとき。

## hash
- 9376c267fa8194d94f175e9895f353889128d4ce8fff592333bfe1d50f96077f

# `builder`

## Summary
- oracle 側へ移された ACP builder 実装を、既存の acp.builder 名前空間や旧 import 経路から参照し続けるための互換層をまとめる領域。
- apply、common、indexing、review、session、tui などの builder 互換入口と、quota probe 用の最小 AgentCallParameter builder へのルーティング起点になる。
- 正本実装や詳細ロジックを保持する場所ではなく、oracle 側 builder と realization 側公開面・parameter 表現を接続する薄い層として位置づけられる。

## Read this when
- acp.builder.* の旧 import 経路や既存公開面が、oracle 側の canonical 実装へどう接続されているか確認したいとき。
- apply、review、session、tui、indexing、common builder の互換入口、再エクスポート、削除条件を調べるとき。
- oracle 側 builder の出力を realization 側 AgentCallParameter や runtime ACP 型へ適合する境界を確認・変更したいとき。
- Codex quota availability probe 用に、既存 AgentCallParameter から最小確認用 parameter を組み立てる処理を探しているとき。
- builder 互換 package の初期化位置、oracle src import 準備、repository root 解決、schema path fallback などの接続処理を調べるとき。

## Do not read this when
- ACP builder の正本仕様、prompt 内容、parameter 内容、生成規則、本体実装を確認したいときは、oracle 側の対応実装や仕様断片を読む。
- apply fork、review、session、TUI など各機能の実行制御、状態管理、画面、イベント処理、git 操作、finding 判定などの実体ロジックを調べたいとき。
- AgentCallParameter、FileAccessMode、path placeholder、oracle file、INDEX.md 記述基準などの一般定義を確認したいときは、より直接の定義や oracle doc を読む。
- 新しい恒久的な builder 機能や公開 API を追加したいだけで、旧 import 経路の互換維持や oracle 側への接続に関心がないとき。

## hash
- 826534467e59844f954b2d93e0ae937cee3fe333d761e2a9523768a8a7a23344

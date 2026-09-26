# `join`

## Summary
- session branch を home branch へ統合する競合解消用 agent call を組み立て、両 branch の merge 前の HEAD、home worktree、閲覧範囲を共通の prompt 構築処理へ渡す。
- この対象は session join 固有の call 設定を担う。join 間で共通する競合解消の指示や処理方針は、共通 prompt 構築側が担う。

## Read this when
- session join の競合解消 call が、どの commit・worktree・アクセス範囲を使って構築されるかを調べるとき。
- session join の call 設定を変更するとき。

## Do not read this when
- 競合の取得方法、共通の解消指示、検証方針を調べたり変更したりするときは、共通 prompt 構築側を読む。
- run の成果を session に統合する call や、封印済み結果の扱いを調べるときは、run join 固有の call 構築側を読む。

## hash
- aa4f32256acce60526d8dc561d08cbd1d917d6e0c73af1f1f174550e15a030f4

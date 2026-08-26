# タイムスタンプのフォーマット

タイムスタンプ `{{time-stamp}}` は、`{{year}}-{{month}}-{{day}}_{{hour}}-{{minute}}_{{sec}}_{{msec}}` 形式とする。

- year は 4 桁ゼロ埋めとする
- month、day、hour、minute、および sec は 2 桁ゼロ埋めとする
- msec は 9 桁とする
- timezone はそのマシンのローカルとする

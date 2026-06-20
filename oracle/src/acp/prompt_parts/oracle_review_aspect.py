from basic.struct_doc import StructDoc


def build_review_oracle_viewpoint() -> StructDoc:
    """
    TODO `cmoc review oracle` におけるレビュー観点

    - 致命的な問題 (fatal) を対象とする
        - 仕様断片同士に明確な矛盾がある
        - 仕様に従って実装した時に、実装者の裁量では解消不能な問題が発生する
    - 単純な問題 (minor) を対象とする
        - 日本語的な誤り（e.g. 誤字、脱字、助詞の抜け）
        - 用語の不統一・表記揺れ・typo
        - その他ケアレスミスの疑いが濃厚なもの
    - 以下の問題は対象としない
        - oracle file だけからは問題だとは言い切れない
        - 仕様からは実装が一意に定まらない
    - これら定義は `codex exec` のプロンプトに「リポジトリ固有の事情に依存しない汎用的なレビュー観点」として注入する。
    """
    ...

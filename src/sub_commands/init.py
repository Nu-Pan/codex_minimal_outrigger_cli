from commons.runtime_preprocess_command import run_preprocess_command


def cmoc_init_impl() -> None:
    """初回 setup と config 同期を CLI runtime から実行する。"""
    run_preprocess_command("init")

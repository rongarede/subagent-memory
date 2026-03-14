"""pytest 配置：注册自定义标记，避免 PytestUnknownMarkWarning。"""


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    )

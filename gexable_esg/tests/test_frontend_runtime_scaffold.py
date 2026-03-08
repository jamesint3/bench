from pathlib import Path


FRONTEND_ROOT = Path("frontend")


def test_frontend_runtime_files_exist() -> None:
    required = [
        "package.json",
        "tsconfig.json",
        "vite.config.ts",
        "index.html",
        "src/main.tsx",
        "src/styles.css",
    ]
    for path in required:
        assert (FRONTEND_ROOT / path).exists()


def test_frontend_module_component_directories_exist() -> None:
    required_dirs = [
        "src/components/cards",
        "src/components/layout",
        "src/modules/emissions",
        "src/modules/energy",
        "src/modules/suppliers",
        "src/modules/projects",
        "src/modules/audits",
    ]
    for path in required_dirs:
        assert (FRONTEND_ROOT / path).is_dir()

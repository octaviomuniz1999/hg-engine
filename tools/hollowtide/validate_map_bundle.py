#!/usr/bin/env python3
"""Check a Hollowtide asset handoff's integrity without importing or changing it.

The manifest is a project handoff format, not a PDSMS or DSPRE file format.
This does not parse Nintendo DS map binaries or establish ROM compatibility.
"""

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re


ASSET_EXTENSIONS = {
    "map_bin": ".bin",
    "model": ".nsbmd",
    "textures": ".nsbtx",
    "permissions": ".per",
    "terrain": ".bdhc",
    "camera": ".bdhcam",
    "buildings": ".bld",
    "background_sound": ".bgs",
    "editor_project": ".pdsmap",
}


def validate_bundle(manifest_path):
    """Return asset count, or raise ValueError/OSError; never write assets."""
    manifest_path = Path(manifest_path)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise ValueError("O manifesto deve ser um objeto JSON")
    if type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        raise ValueError("schema_version deve ser 1")
    if manifest.get("target_game") != "heartgold-us":
        raise ValueError("target_game deve ser heartgold-us")
    key = manifest.get("map_key")
    if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", key):
        raise ValueError("map_key deve usar palavras em minusculas separadas por hifen")
    exporter = manifest.get("exporter")
    if not isinstance(exporter, dict) or any(
        not isinstance(exporter.get(field), str) or not exporter[field].strip()
        for field in ("name", "version")
    ):
        raise ValueError("exporter deve identificar name e version")
    assets = manifest.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValueError("assets deve conter pelo menos um arquivo")

    root = manifest_path.parent.resolve()
    seen = set()
    for asset in assets:
        if not isinstance(asset, dict):
            raise ValueError("Cada asset deve ser um objeto")
        name = asset.get("path")
        if not isinstance(name, str) or not name or "\\" in name or ":" in name:
            raise ValueError("path deve ser relativo ao manifesto, usando /")
        relative = PurePosixPath(name)
        if relative.is_absolute() or any(part in ("", ".", "..") for part in name.split("/")):
            raise ValueError(f"Caminho nao permitido: {name}")
        if name.casefold() in seen:
            raise ValueError(f"Asset duplicado: {name}")
        seen.add(name.casefold())
        kind = asset.get("kind")
        if not isinstance(kind, str) or kind not in ASSET_EXTENSIONS:
            raise ValueError(f"Tipo desconhecido: {kind}")
        if relative.suffix.lower() != ASSET_EXTENSIONS[kind]:
            raise ValueError(f"Extensao incorreta para {kind}: {name}")
        path = root
        for part in relative.parts:
            path = path / part
            if path.is_symlink():
                raise ValueError(f"Link simbolico nao permitido: {name}")
        if not path.is_file():
            raise ValueError(f"Arquivo ausente: {name}")
        expected_size = asset.get("size")
        if type(expected_size) is not int or expected_size <= 0:
            raise ValueError(f"size deve ser um inteiro positivo: {name}")
        if path.stat().st_size != expected_size:
            raise ValueError(f"Tamanho divergente: {name}")
        expected_hash = asset.get("sha256")
        if not isinstance(expected_hash, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", expected_hash):
            raise ValueError(f"sha256 invalido: {name}")
        with path.open("rb") as stream:
            actual_hash = hashlib.file_digest(stream, "sha256").hexdigest()
        if actual_hash != expected_hash.lower():
            raise ValueError(f"SHA-256 divergente: {name}")
    return len(assets)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        count = validate_bundle(args.manifest)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Falha na integridade do pacote: {error}\n")
    print(f"Integridade conferida: {count} arquivo(s).")
    print("Formato binario, importacao, colisao e funcionamento no jogo NAO validados.")


if __name__ == "__main__":
    main()

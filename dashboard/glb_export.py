#!/usr/bin/env python3
"""Convert a binary PCD (fields x y z rgb ...) into a binary glTF (.glb) point cloud.

The output keeps every point and its colour. It is a POINTS primitive, not a mesh:
there are no triangles and no surface. glTF is Y-up; the PCD is Z-up, so (x, y, z) -> (x, z, -y).
Usage: pcd_to_glb.py in.pcd out.glb
"""
import json
import struct
import sys

import numpy as np


def read_pcd(path):
    with open(path, "rb") as f:
        header = {}
        while True:
            line = f.readline().decode("ascii", "replace").strip()
            if line.startswith("#") or not line:
                continue
            key, *val = line.split()
            header[key] = val
            if key == "DATA":
                break
        data = f.read()
    if header["DATA"] != ["binary"]:
        raise SystemExit("only binary PCD is supported")
    names = header["FIELDS"]
    sizes = [int(s) for s in header["SIZE"]]
    types = header["TYPE"]
    kinds = {("F", 4): "<f4", ("F", 8): "<f8", ("U", 4): "<u4", ("I", 4): "<i4", ("U", 1): "u1", ("U", 2): "<u2"}
    dtype = np.dtype([(n, kinds[(t, s)]) for n, t, s in zip(names, types, sizes)])
    n = int(header["POINTS"][0])
    return np.frombuffer(data, dtype=dtype, count=n)


def build_glb(points):
    xyz = np.stack([points["x"], points["y"], points["z"]], axis=1).astype("<f4")
    ok = np.isfinite(xyz).all(axis=1)
    if not ok.any():
        raise ValueError("no finite points")
    xyz = xyz[ok]
    rgb = np.ascontiguousarray(points["rgb"][ok]).view("<u4")
    colors = np.stack([(rgb >> 16) & 255, (rgb >> 8) & 255, rgb & 255], axis=1).astype("u1")
    # pad each row to 4 bytes for glTF alignment: use RGBA u8
    rgba = np.concatenate([colors, np.full((len(colors), 1), 255, "u1")], axis=1)
    gl = np.stack([xyz[:, 0], xyz[:, 2], -xyz[:, 1]], axis=1).astype("<f4")
    pos_bytes, col_bytes = gl.tobytes(), rgba.tobytes()
    blob = pos_bytes + col_bytes
    blob += b"\0" * (-len(blob) % 4)
    gj = {
        "asset": {"version": "2.0", "generator": "pcd_to_glb.py"},
        "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0, "COLOR_0": 1}, "mode": 0}]}],
        "buffers": [{"byteLength": len(blob)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos_bytes), "target": 34962},
            {"buffer": 0, "byteOffset": len(pos_bytes), "byteLength": len(col_bytes), "target": 34962},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(gl), "type": "VEC3",
             "min": gl.min(axis=0).tolist(), "max": gl.max(axis=0).tolist()},
            {"bufferView": 1, "componentType": 5121, "normalized": True, "count": len(gl), "type": "VEC4"},
        ],
    }
    js = json.dumps(gj, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    total = 12 + 8 + len(js) + 8 + len(blob)
    out = (struct.pack("<4sII", b"glTF", 2, total) + struct.pack("<I4s", len(js), b"JSON") + js
           + struct.pack("<I4s", len(blob), b"BIN\0") + blob)
    return out, len(gl), int((~ok).sum())


def write_glb(points, path):
    out, n, dropped = build_glb(points)
    with open(path, "wb") as f:
        f.write(out)
    return n, dropped


if __name__ == "__main__":
    n, dropped = write_glb(read_pcd(sys.argv[1]), sys.argv[2])
    print(f"{n} points written, {dropped} non-finite points dropped")

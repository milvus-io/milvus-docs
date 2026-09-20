#!/usr/bin/env python3
"""Run the cpp snippets of a user-guide page against a live Milvus server using a
prebuilt milvus-sdk-cpp binary from the `default-conan-local2` Conan repo.

If a prebuilt binary matching the requested version/system is available, it is
installed with `--build=never` and the page's ```cpp blocks are compiled and
run against it. If no prebuilt binary is found, cpp verification is SKIPPED
(reported, not failed).

Usage: python3 run_page_cpp.py <page.md> [<version>]
"""
import os
import re
import shutil
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PROJ = os.path.join(REPO, "sdk-tmp", "snippet-run", "cpp")
DEPLOY = os.path.join(PROJ, "deploy")
REMOTE = "default-conan-local2"
CONAN_HOME = os.environ.get("CONAN_HOME", os.path.join(os.path.expanduser("~"), "work", ".conan2"))


def install_prebuilt(version):
    """Try to fetch a prebuilt milvus-sdk-cpp/<version> binary. Return True on success.
    The published binaries are built with cppstd=14 — match that setting."""
    attempts = [
        ["-s", "compiler.cppstd=14"],
        ["-s", "compiler.version=11", "-s", "compiler.cppstd=14"],
        ["-s", "compiler.version=12", "-s", "compiler.cppstd=14", "-s", "build_type=Release"],
    ]
    for extra in attempts:
        cmd = ["conan", "install", f"--requires=milvus-sdk-cpp/{version}@milvus/dev",
               "--build=never", f"--deployer=full_deploy",
               f"--output-folder={DEPLOY}"] + extra
        r = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, "CONAN_HOME": CONAN_HOME})
        if r.returncode == 0:
            return True
    return False


def latest_remote_version():
    """Query the remote for the newest milvus-sdk-cpp version."""
    r = subprocess.run(["conan", "search", "milvus-sdk-cpp/*", "-r", REMOTE],
                       capture_output=True, text=True, env={**os.environ, "CONAN_HOME": CONAN_HOME})
    vers = re.findall(r"milvus-sdk-cpp/([0-9]+\.[0-9]+\.[0-9]+)@milvus/dev", r.stdout)
    vers.sort(key=lambda v: [int(x) for x in v.split(".")])
    return vers[-1] if vers else None


def _split_top_level_statements(text):
    """Split C++ text into statements: each ends at a top-level ';' or when a
    top-level '{...}' control block closes (if/for/while/switch — i.e. the '{'
    was preceded by ')' or a control keyword, NOT by '=' object/array
    initialization). Strings/comments respected."""
    stmts = []
    paren = 0          # ( ) [ ] depth
    brace = 0          # { } depth
    brace_is_ctrl = []  # per-open-brace: True if it starts a control block
    cur = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == '/' and i + 1 < n and text[i + 1] == '/':
            while i < n and text[i] != '\n':
                i += 1
            continue
        if c == '/' and i + 1 < n and text[i + 1] == '*':
            i += 2
            while i + 1 < n and not (text[i] == '*' and text[i + 1] == '/'):
                i += 1
            i += 2
            continue
        if c == 'R' and i + 2 < n and text[i + 1] == '"' and text[i + 2] == '(':
            # C++ raw string R"(...)" — copy verbatim through the closing )"
            cur.append('R"(')
            i += 3
            while i + 1 < n and not (text[i] == ')' and text[i + 1] == '"'):
                cur.append(text[i])
                i += 1
            if i + 1 < n:
                cur.append(')"')
                i += 2
            continue
        if c == '"':
            cur.append(c)
            i += 1
            while i < n and text[i] != '"':
                if text[i] == '\\':
                    cur.append(text[i])
                    i += 1
                    if i < n:
                        cur.append(text[i])
                        i += 1
                    continue
                cur.append(text[i])
                i += 1
            if i < n:
                cur.append('"')
                i += 1
            continue
        if c == "'" and i + 2 < n and text[i + 1] == '\\':
            cur.append(text[i:i + 4])
            i += 4
            continue
        if c in "([":
            paren += 1
            cur.append(c)
            i += 1
            continue
        if c in ")]":
            paren -= 1
            cur.append(c)
            i += 1
            continue
        if c == '{':
            brace += 1
            # control block if the '{' follows ')' or a control keyword
            prev = "".join(cur).rstrip()
            ctrl = prev.endswith(")") or bool(re.search(r"\b(if|for|while|switch|catch|namespace|class|struct|extern\s+C|else)\s*$", prev))
            brace_is_ctrl.append(ctrl)
            cur.append(c)
            i += 1
            continue
        if c == '}':
            brace -= 1
            cur.append(c)
            i += 1
            if brace == 0 and paren == 0 and brace_is_ctrl and brace_is_ctrl.pop():
                # a top-level control block just closed; end the statement
                stmts.append("".join(cur).strip())
                cur = []
            elif brace_is_ctrl and not brace_is_ctrl[-1] and brace >= 0:
                pass  # object/array init: keep accumulating, terminate at ';'
            continue
        if c == ';' and brace == 0 and paren == 0:
            stmts.append(("".join(cur) + ";").strip())
            cur = []
            i += 1
            continue
        cur.append(c)
        i += 1
    if "".join(cur).strip():
        stmts.append("".join(cur).strip())
    return stmts


def _declared_var(stmt):
    """If stmt declares a variable at top level, return its name; else None.
    Handles `Type name;`, `Type name = ...;`, `Type name(args);` (constructor
    init) and `auto name = ...;` (multi-line builder chains included, they end
    at the trailing ';' already)."""
    s = re.sub(r"\s+", " ", stmt).strip()
    # auto name = ...
    m = re.match(r"^auto\s+([A-Za-z_]\w*)\s*=", s)
    if m:
        return m.group(1)
    # Type name; / Type name = ...; / Type name(args);
    m = re.match(
        r"^(?:milvus::|std::|const\s+)?[\w:<>]+\s+(?:[A-Za-z_]\w*::)*([A-Za-z_]\w*)\s*(?:=|;|\()", s)
    if m:
        name = m.group(1)
        if name in {"for", "while", "if", "return", "switch", "catch", "delete"}:
            return None
        return name
    return None


def _decl_prefix(stmt):
    """If stmt declares a typed variable, return the leading text before the
    variable name (type + whitespace), so a later declaration can be rewritten
    into an assignment; else None. Handles `auto name = ...` too."""
    s = re.sub(r"\s+", " ", stmt).strip()
    m = re.match(r"^auto\s+(?=[A-Za-z_]\w*\s*=)", s)
    if m:
        return "auto "
    m = re.match(r"^(milvus::|std::|const\s+)?[\w:<>]+\s+(?:[A-Za-z_]\w*::)*(?=[A-Za-z_]\w*\s*(?:=|;))", s)
    if m:
        return s[:m.end()]
    return None


def _hoist_shared_declarations(bodies):
    """Hoist declarations of variables used across multiple blocks to the top.

    User-guide cpp blocks form one continuous program split across code fences:
    block N declares `schema`, a later block consumes it. Without hoisting, each
    block re-declares its own locals (create_request, ...) which would clash if
    concatenated, so blocks are isolated by scope instead; only cross-block
    variables must live in the shared scope. Re-declarations of the same name in
    later blocks become assignments, mirroring pymilvus's re-assignment model.

    Returns the list of hoisted declaration statements.
    """
    # variables owned by the runner's shared prelude — never hoist/re-declare
    skip = {"client", "connect_param", "status"}

    blocks_used = []          # per-block set of identifiers referenced
    for b in bodies:
        blocks_used.append(set(re.findall(r"[A-Za-z_]\w*", b)))

    # name -> list of (block_idx, decl_stmt)
    declared = {}
    for bi, b in enumerate(bodies):
        for stmt in _split_top_level_statements(b):
            name = _declared_var(stmt)
            if name and name not in skip:
                declared.setdefault(name, []).append((bi, stmt))

    # a name is shared when it is used in a block other than the one where it is
    # first declared (single or multiple declarations both qualify)
    shared_names = set()
    for name, occ in declared.items():
        first_bi = occ[0][0]
        for later in range(first_bi + 1, len(bodies)):
            if name in blocks_used[later]:
                shared_names.add(name)
                break

    # hoist the first declaration of each shared name; rewrite any later
    # declaration of the same name into an assignment (type removed)
    hoisted = []
    for name in sorted(shared_names, key=lambda x: declared[x][0][0]):
        first_bi, first_stmt = declared[name][0]
        hoisted.append(first_stmt)
        bodies[first_bi] = bodies[first_bi].replace(first_stmt, "", 1)
        for bi, stmt in declared[name][1:]:
            prefix = _decl_prefix(stmt)
            if prefix:
                bodies[bi] = bodies[bi].replace(stmt, stmt[len(prefix):].strip(), 1)
    return hoisted


def main():
    page = sys.argv[1]
    if not shutil.which("conan"):
        print("cpp: conan not installed — SKIPPING cpp verification")
        sys.exit(0)
    version = sys.argv[2] if len(sys.argv) > 2 else latest_remote_version()
    if not version:
        print("cpp: no milvus-sdk-cpp recipe on the remote — skipping cpp verification")
        sys.exit(0)

    if not install_prebuilt(version):
        print(f"cpp: no prebuilt milvus-sdk-cpp/{version} binary for this system on {REMOTE} — SKIPPING cpp verification")
        sys.exit(0)
    print(f"cpp: using prebuilt milvus-sdk-cpp/{version} from {REMOTE}")

    md = open(page).read()
    blocks = re.findall(r"```cpp\n(.*?)```", md, re.S)

    inc = os.path.join(DEPLOY, "include")
    lib = os.path.join(DEPLOY, "lib")
    if not os.path.isdir(inc):
        print("cpp: deployed package has no include/ dir — skipping cpp verification")
        sys.exit(0)

    # assemble: hoist includes, strip per-block client init, wrap block bodies
    # in scoped braces, and create one shared client in main() so blocks that
    # each start with `auto client = MilvusClientV2::Create();` do not clash.
    includes = []
    bodies = []
    for b in blocks:
        kept = []
        for line in b.split("\n"):
            if line.strip().startswith("#include"):
                includes.append(line.strip())
                continue
            kept.append(line)
        bodies.append("\n".join(kept))
    includes = list(dict.fromkeys(includes))

    # Strip the per-block client init + connect so one shared client is created
    # in run_all(). Matches the user-guide cpp style, e.g.:
    #   auto client = milvus::MilvusClientV2::Create();
    #   milvus::ConnectParam connect_param{"http://localhost:19530", "root:Milvus"};
    #   auto status = client->Connect(connect_param);
    #   if (!status.IsOk()) { std::cerr << status.Message() << std::endl; return; }
    # or the throw variant.
    connect_err = (
        r"(?:\s*if\s*\(\s*!status\.IsOk\(\)\s*\)\s*\{\s*"
        r"(?:std::cerr\s*<<\s*status\.Message\(\)\s*<<\s*std::endl\s*;\s*"
        r"|throw\s+std::runtime_error\([^)]*\)\s*;\s*)"
        r"return;\s*\})?"
    )
    cleaned = []
    for b in bodies:
        b = re.sub(
            r"auto\s+client\s*=\s*(?:milvus::)?MilvusClientV2::Create\(\s*\);",
            "", b)
        b = re.sub(
            r"milvus::ConnectParam\s+connect_param\{[^}]*\};\s*",
            "", b)
        b = re.sub(
            r"auto\s+status\s*=\s*client->Connect\(\s*connect_param\s*\);"
            + connect_err + r"\s*",
            "", b, flags=re.S)
        # later blocks that re-declare `auto status = client->X(...)` become an
        # assignment to the shared `status` declared in run_all()
        b = re.sub(r"\bauto\s+status\s*=\s*client->", "status = client->", b)
        cleaned.append(b)
    bodies = cleaned

    # The user-guide cpp blocks are one continuous program split across code
    # fences (mirroring the pymilvus baseline, whose runner execs each block in
    # the same shared env). Mirror that with:
    #   - one shared client + connect in run_all();
    #   - every block body concatenated in the SAME scope so cross-block
    #     variables (schema, index_params, query_vector, ...) stay visible;
    #   - a variable declared again in a later block is rewritten into a plain
    #     assignment (type prefix stripped), matching pymilvus's re-assignment;
    #   - `auto status = client->X(...)` inside a block becomes
    #     `status = client->X(...)` since `status` already exists in run_all().
    declared = {}
    for bi, b in enumerate(bodies):
        for stmt in _split_top_level_statements(b):
            name = _declared_var(stmt)
            if name and name not in {"client", "connect_param"}:
                declared.setdefault(name, []).append((bi, stmt))
    for name, occ in declared.items():
        if len(occ) < 2:
            continue
        # Rewrite later declarations of the same name into plain assignments
        # (type + indentation stripped), mirroring pymilvus's re-assignment.
        # Line-based regex so whitespace differences between the parsed stmt
        # and the raw block text never break the replacement.
        type_pat = r"(?:milvus::|std::|const\s+)?[\w:<>]+\s+(?:[A-Za-z_]\w*::)*"
        for bi, _stmt in occ[1:]:
            # constructor init `Type name(args);` -> `name = Type(args);`
            bodies[bi] = re.sub(
                r"(?m)^([ \t]*)((?:milvus::|std::|const\s+)?[\w:<>]+)\s+"
                + re.escape(name) + r"\s*\(",
                lambda mo: mo.group(1) + name + " = " + mo.group(2) + "(",
                bodies[bi], count=1)
            # plain/initializer decl `Type name;` / `Type name = ...;` -> `name = ...;`
            bodies[bi] = re.sub(
                r"(?m)^([ \t]*)" + type_pat + re.escape(name) + r"\b(?!\s*\()",
                lambda mo: mo.group(1) + name,
                bodies[bi], count=1)

    prog = "\n".join(includes) + "\n\nvoid run_all() {\n"
    prog += '    auto client = milvus::MilvusClientV2::Create();\n'
    prog += '    milvus::ConnectParam connect_param{"http://localhost:19530", "root:Milvus"};\n'
    prog += '    auto status = client->Connect(connect_param);\n'
    prog += '    if (!status.IsOk()) {\n'
    prog += '        std::cerr << status.Message() << std::endl;\n'
    prog += '        return;\n'
    prog += '    }\n'
    for i, b in enumerate(bodies):
        prog += f"    // === block {i} ===\n"
        prog += "\n".join("    " + ln for ln in b.split("\n")) + "\n"
    prog += "}\nint main() { run_all(); return 0; }\n"

    os.makedirs(PROJ, exist_ok=True)
    src = os.path.join(PROJ, "run_page.cpp")
    out = os.path.join(PROJ, "a.out")
    with open(src, "w") as f:
        f.write(prog)

    # link against the deployed library (find the milvus .a/.so)
    if not shutil.which("g++"):
        print("cpp: g++ not installed — SKIPPING cpp verification")
        sys.exit(0)
    libs = [f for f in os.listdir(lib) if f.startswith("libmilvus")] if os.path.isdir(lib) else []
    libname = ""
    if libs:
        base = libs[0][3:]                    # libmilvus_sdk.so -> milvus_sdk
        libname = base.split(".")[0]          # strip trailing .so/.a
    link = f"-L{lib} -l{libname}" if libs else ""
    print(f"cpp blocks: {len(blocks)}")
    c = subprocess.run(["g++", "-std=c++14", "-o", out, src, f"-I{inc}"] + (link.split() if link else []),
                       capture_output=True, text=True, cwd=PROJ)
    if c.returncode != 0:
        sys.stderr.write(c.stderr[-3000:])
        print(f"\n=== {page} === cpp compile FAILED ({len(blocks)} blocks)")
        sys.exit(1)
    run_env = {**os.environ}
    if os.path.isdir(lib):
        run_env["LD_LIBRARY_PATH"] = lib + os.pathsep + run_env.get("LD_LIBRARY_PATH", "")
    r = subprocess.run([out], capture_output=True, text=True, env=run_env)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr[-3000:] if r.returncode else "")
    print(f"\n=== {page} === cpp run {'OK' if r.returncode == 0 else 'FAILED'} ({len(blocks)} blocks)")
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()

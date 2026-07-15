# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **restored Claude Code source tree** — reconstructed from source maps with missing modules replaced by compatibility shims. It is not pristine upstream; some areas contain fallbacks or degraded implementations where original code was unrecoverable.

## Commands

```bash
bun install        # Install dependencies and local shim packages
bun run dev        # Start the restored CLI interactively
bun run start      # Alias for dev
bun run version    # Print version and exit
bun run dev:restore-check  # Run via dev-entry shim
./compile.sh       # Build standalone executable via bun build --compile
```

No first-class `lint` or `test` scripts exist in package.json. Validate changes by running the CLI directly.

## Architecture

### Entry Flow
- `src/bootstrap-entry.ts` → sets up `MACRO` config → imports `src/entrypoints/cli.tsx`
- `src/entrypoints/cli.tsx` → handles fast-paths (--version, --dump-system-prompt) → loads `src/main.tsx`
- `src/main.tsx` → initializes telemetry, auth, MCP, policy limits → renders ink `<App />`

### Core Modules
| Path | Purpose |
|------|---------|
| `src/commands/` | ~100 command implementations (commit, config, mcp, session, etc.) |
| `src/tools/` | Tool implementations (BashTool, FileEditTool, GrepTool, MCPTool, etc.) |
| `src/components/` | React/ink TUI components (Message, PromptInput, StatusLine, etc.) |
| `src/services/` | API clients, MCP server management, analytics, plugins, settings sync |
| `src/coordinator/` | Structured IO, print utilities, transport layers |
| `src/bootstrap/` | Bootstrap state and MACRO configuration |
| `src/ink/` | Ink React reconciler setup and App component |

### Shims
Native bindings and private packages unrecoverable from source maps are in `shims/`. These provide degraded but functional fallbacks (e.g., `shims/color-diff-napi`, `shims/url-handler-napi`).

### Build
The project uses `bun build --compile` to produce a standalone executable. The `compile.sh` script wraps this with documentation.

## Restoration Context

- **Source map reconstruction**: Some type-only files, build-time generated files, and private native bindings are missing
- **Shim behavior**: When original implementation is unrecoverable, shims may have reduced functionality
- **Validation approach**: Run `bun run dev` or `bun run version` to verify affected flows after changes
- **Minimal changes**: Prefer auditable, targeted fixes over broad refactoring given the restoration nature

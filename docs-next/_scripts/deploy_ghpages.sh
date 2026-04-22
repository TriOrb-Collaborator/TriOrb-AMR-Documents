#!/usr/bin/env bash
# Build the docs-next site and publish it to a GitHub Pages branch.
#
# Usage:
#   _scripts/deploy_ghpages.sh [options] [<remote> [<branch>]]
#
# Defaults:
#   remote = fork          (safe, force-push allowed)
#   branch = gh-pages
#
# Options:
#   --skip-stage           Don't run `make deploy-stage-local`; reuse the
#                          existing _build/deploy/ tree as-is.
#   --no-force             Reject the push if fast-forward is not possible.
#                          Required when targeting `origin` (production).
#   --yes                  Skip the interactive confirmation prompt.
#   -h, --help             Print this help.
#
# Examples:
#   # fork deploy test (orphan force push)
#   _scripts/deploy_ghpages.sh fork
#
#   # production deploy (no force, confirms before pushing)
#   _scripts/deploy_ghpages.sh --no-force origin
#
#   # redeploy fork without rebuilding
#   _scripts/deploy_ghpages.sh --skip-stage --yes fork

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_NEXT="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_ROOT="$(cd "$DOCS_NEXT/.." && pwd)"

# Defaults.
REMOTE="fork"
BRANCH="gh-pages"
SKIP_STAGE=0
FORCE_PUSH=1  # force is the safe default for fork; --no-force flips it
ASSUME_YES=0

print_usage() { sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; }

while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-stage)  SKIP_STAGE=1; shift ;;
        --no-force)    FORCE_PUSH=0; shift ;;
        --yes|-y)      ASSUME_YES=1; shift ;;
        -h|--help)     print_usage; exit 0 ;;
        --)            shift; break ;;
        -*)            echo "unknown option: $1" >&2; exit 2 ;;
        *)             break ;;
    esac
done
if [[ $# -gt 0 ]]; then REMOTE="$1"; shift; fi
if [[ $# -gt 0 ]]; then BRANCH="$1"; shift; fi

# Safety: production origin must never be force-pushed from this script.
if [[ "$REMOTE" == "origin" && "$FORCE_PUSH" == "1" ]]; then
    cat >&2 <<MSG
Refusing to force-push to 'origin' (production).
Pass --no-force explicitly to target production — the current gh-pages
history will be preserved and your deploy must be a fast-forward.
MSG
    exit 2
fi

say() { printf '\033[1;34m==>\033[0m %s\n' "$*"; }
warn() { printf '\033[1;33mwarning:\033[0m %s\n' "$*"; }

say "Repo: $REPO_ROOT"
say "Target: $REMOTE / $BRANCH  (force=$FORCE_PUSH, skip-stage=$SKIP_STAGE)"

# Pre-flight checks.
cd "$REPO_ROOT"

if ! git remote get-url "$REMOTE" >/dev/null 2>&1; then
    echo "remote '$REMOTE' is not configured. Run:  git remote add $REMOTE <url>" >&2
    exit 2
fi
REMOTE_URL="$(git remote get-url "$REMOTE")"
say "Remote URL: $REMOTE_URL"

# Make sure the build tree exists (or we're told to generate it).
DEPLOY_DIR="$DOCS_NEXT/_build/deploy"
if [[ "$SKIP_STAGE" == "0" ]]; then
    say "Running make deploy-stage-local …"
    make -C "$DOCS_NEXT" deploy-stage-local
else
    [[ -d "$DEPLOY_DIR" ]] || { echo "$DEPLOY_DIR missing; drop --skip-stage or build first" >&2; exit 2; }
    warn "Skipping stage — using existing $DEPLOY_DIR"
fi

# Jekyll bypass (GitHub Pages would otherwise skip _static/, _images/ etc.).
touch "$DEPLOY_DIR/.nojekyll"

# Sanity: make sure the tree doesn't leak license-auth internals.
leaks="$(find "$DEPLOY_DIR" \( -name '*ct.hpp*' -o -name '*sha256*' -o -name 'ct_8hpp*' \) 2>/dev/null | head -5)"
if [[ -n "$leaks" ]]; then
    cat >&2 <<MSG
Refusing to deploy — the tree still contains license-auth files:
$leaks
Clean them with:  find "$DEPLOY_DIR" -type d -name generated -prune -exec rm -rf {} +
MSG
    exit 2
fi

# Size check + summary.
SIZE="$(du -sh "$DEPLOY_DIR" 2>/dev/null | cut -f1)"
say "Deploy tree size: $SIZE"
say "Top-level entries:"
( cd "$DEPLOY_DIR" && ls -1 ) | sed 's/^/  /'

# Confirm with the user before touching the remote.
if [[ "$ASSUME_YES" == "0" ]]; then
    push_kind="push"
    [[ "$FORCE_PUSH" == "1" ]] && push_kind="force-push"
    read -r -p "$(printf '\033[1;35m?\033[0m %s ' "Proceed to $push_kind to $REMOTE / $BRANCH? [y/N]")" reply
    case "$reply" in
        y|Y|yes|YES) : ;;
        *) echo "aborted"; exit 1 ;;
    esac
fi

# Use a temporary worktree so we don't disturb the primary working tree.
WT="$(mktemp -d -t ghpages-XXXXXX)"
cleanup() {
    git worktree remove --force "$WT" 2>/dev/null || true
    rm -rf "$WT"
    git branch -D "_deploy_tmp_$$" 2>/dev/null || true
}
trap cleanup EXIT

say "Creating temporary worktree at $WT"
git worktree add --detach "$WT" HEAD >/dev/null

cd "$WT"
# Wipe everything tracked, then lay the deploy tree.
git rm -rfq . 2>/dev/null || true
find . -mindepth 1 -not -path './.git*' -exec rm -rf {} + 2>/dev/null || true
cp -a "$DEPLOY_DIR/." .
touch .nojekyll

git checkout --orphan "_deploy_tmp_$$" >/dev/null
git add -A
git -c user.name="TriOrb Docs Deploy" \
    -c user.email="docs-deploy@triorb.co.jp" \
    commit -q -m "deploy: v1.2.4 Sphinx + landing + preserved legacy archives

release    = v1.2.4
source_sha = $(git -C "$REPO_ROOT" rev-parse --short HEAD)
source_branch = $(git -C "$REPO_ROOT" rev-parse --abbrev-ref HEAD)
deploy_ts  = $(date -u +%Y-%m-%dT%H:%M:%SZ)
"

FILE_COUNT="$(git ls-files | wc -l)"
say "Committed $FILE_COUNT files."

PUSH_ARGS=("$REMOTE" "HEAD:$BRANCH")
[[ "$FORCE_PUSH" == "1" ]] && PUSH_ARGS=(--force-with-lease "${PUSH_ARGS[@]}")

say "Pushing → $REMOTE / $BRANCH"
git push "${PUSH_ARGS[@]}"

say "Done."
echo
PAGES_URL=""
if [[ "$REMOTE_URL" =~ github\.com[:/]([^/]+)/([^/.]+) ]]; then
    OWNER="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
    PAGES_URL="https://${OWNER,,}.github.io/$REPO/"
    echo "Pages URL (after GitHub provisions the site):"
    echo "  $PAGES_URL"
    echo
    echo "First-time setup on fork:"
    echo "  https://github.com/$OWNER/$REPO/settings/pages"
    echo "    Source = Deploy from a branch"
    echo "    Branch = $BRANCH / (root)"
fi

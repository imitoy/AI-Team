#!/bin/bash
# setup-git-hook.sh — Install git post-push hook that auto-creates MRs
# Usage: bash scripts/setup-git-hook.sh

HOOK_DIR=".git/hooks"
HOOK_FILE="$HOOK_DIR/post-push"

mkdir -p "$HOOK_DIR"

cat > "$HOOK_FILE" << 'HOOK'
#!/bin/bash
# post-push hook — auto-create MR after pushing to origin
# Installed by scripts/setup-git-hook.sh

# Read git refs from stdin (format: <local_ref> <local_sha> <remote_ref> <remote_sha>)
while read local_ref local_sha remote_ref remote_sha; do
    # Only trigger for branches pushed to origin
    if [[ "$remote_ref" =~ ^refs/heads/(.+)$ ]]; then
        BRANCH="${BASH_REMATCH[1]}"
        # Skip main branch if you want (or enable for all)
        # if [ "$BRANCH" = "main" ]; then continue; fi

        # Get commit message for title
        TITLE=$(git log -1 --format=%s "$local_sha" 2>/dev/null || echo "Update $BRANCH")

        echo ""
        echo "  → Auto-creating MR for branch: $BRANCH"
        python3 scripts/create-mr.py --source "$BRANCH" --title "$TITLE"
    fi
done
HOOK

chmod +x "$HOOK_FILE"
echo "✓ Installed post-push hook at $HOOK_FILE"
echo "  MRs will auto-create on every git push to any branch."
#!/bin/bash
# Trigger README update for KonetiBalaji profile
# Add this script to your other repositories and run it after commits

echo "🚀 Triggering README update for KonetiBalaji profile..."

# Trigger the repository dispatch event
curl -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "User-Agent: README-Update-Trigger" \
  https://api.github.com/repos/KonetiBalaji/KonetiBalaji/dispatches \
  -d '{
    "event_type": "update-readme",
    "client_payload": {
      "message": "Repository activity detected - updating README",
      "triggered_by": "repository_activity",
      "repository": "'$GITHUB_REPOSITORY'",
      "action": "manual_trigger"
    }
  }'

if [ $? -eq 0 ]; then
    echo "✅ README update triggered successfully!"
    echo "Your profile README will be updated within a few minutes."
else
    echo "❌ Failed to trigger README update"
    echo "Make sure GITHUB_TOKEN is set in your environment"
fi

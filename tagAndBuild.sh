#!/usr/bin/env bash

WEZTERM_VERSION=$(curl -s https://api.github.com/repos/wez/wezterm/releases/latest | grep tag_name | cut -d \" -f 4 | tr '-' '_')

echo tagging "${WEZTERM_VERSION}"
tito tag --use-version 0.r"${WEZTERM_VERSION}"
git push --follow-tags origin

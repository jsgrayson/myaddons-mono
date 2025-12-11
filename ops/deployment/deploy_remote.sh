#!/bin/bash
echo 'Deploying Goblin on remote server...'
ssh user@server 'cd goblin-clean && bash ops/deployment/deploy_local.sh'

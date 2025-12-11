#!/bin/bash
echo 'Generating Goblin health report...'
echo 'Disk usage:'
df -h | grep Users
echo ''
echo 'Top processes:'
ps aux | head
